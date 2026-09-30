# SimpleCAD - Fusion-style trackpad gestures for FreeCAD's 3D view
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Required Notice: Copyright Matthew Armstrong (https://github.com/The-Dorkknight)
# Licensed under the PolyForm Noncommercial License 1.0.0. No warranty.
#
#   two-finger drag            -> pan
#   Shift/Option + two-finger  -> orbit (turntable, around the screen centre)
#   pinch                      -> zoom
#   two-finger double-tap      -> fit all
#
# A physical mouse wheel is left alone, so FreeCAD's own zoom still works.
# The camera maths is plain Python (no pivy types), so it can be unit-tested
# outside FreeCAD; only get_cam()/set_cam() touch the Coin camera node.

import math

try:
    from PySide import QtCore
except ImportError:  # pragma: no cover
    QtCore = None


# ───────────────────────── vector / quaternion helpers ─────────────────────────
# Quaternions are (x, y, z, w), the same order Coin's SbRotation uses.

def v_add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def v_sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def v_mul(a, s): return (a[0] * s, a[1] * s, a[2] * s)


def q_axis(axis, angle):
    x, y, z = axis
    n = math.sqrt(x * x + y * y + z * z) or 1.0
    s = math.sin(angle / 2) / n
    return (x * s, y * s, z * s, math.cos(angle / 2))


def q_mul(a, b):
    """Hamilton product a*b: apply b first, then a."""
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz)


def q_rot(q, v):
    x, y, z, w = q
    vx, vy, vz = v
    # v' = v + 2w(q×v) + 2 q×(q×v)
    cx, cy, cz = (y * vz - z * vy, z * vx - x * vz, x * vy - y * vx)
    ccx, ccy, ccz = (y * cz - z * cy, z * cx - x * cz, x * cy - y * cx)
    return (vx + 2 * (w * cx + ccx), vy + 2 * (w * cy + ccy), vz + 2 * (w * cz + ccz))


def q_norm(q):
    n = math.sqrt(sum(c * c for c in q)) or 1.0
    return tuple(c / n for c in q)


# ───────────────────────── pure camera moves ─────────────────────────
# cam is a dict: pos, quat, focal, ortho, height (ortho), angle (perspective)

def world_per_px(cam, view_h):
    h = cam["height"] if cam["ortho"] else 2 * cam["focal"] * math.tan(cam["angle"] / 2)
    return h / max(view_h, 1)


def pan(cam, dx, dy, view_h):
    """Move the view so the model follows the fingers."""
    s = world_per_px(cam, view_h)
    right = q_rot(cam["quat"], (1, 0, 0))
    up = q_rot(cam["quat"], (0, 1, 0))
    cam["pos"] = v_add(cam["pos"], v_add(v_mul(right, -dx * s), v_mul(up, dy * s)))
    return cam


def orbit(cam, yaw, pitch):
    """Turntable orbit around the point at the centre of the screen."""
    look = q_rot(cam["quat"], (0, 0, -1))
    centre = v_add(cam["pos"], v_mul(look, cam["focal"]))
    right = q_rot(cam["quat"], (1, 0, 0))
    r = q_mul(q_axis((0, 0, 1), yaw), q_axis(right, pitch))   # pitch, then yaw
    cam["pos"] = v_add(centre, q_rot(r, v_sub(cam["pos"], centre)))
    cam["quat"] = q_norm(q_mul(r, cam["quat"]))
    return cam


def zoom(cam, amount):
    """amount > 0 zooms in (pinch out), < 0 zooms out."""
    amount = max(-0.5, min(0.5, amount))
    if cam["ortho"]:
        cam["height"] = max(1e-6, cam["height"] * (1 - amount))
    else:
        look = q_rot(cam["quat"], (0, 0, -1))
        step = cam["focal"] * amount
        cam["pos"] = v_add(cam["pos"], v_mul(look, step))
        cam["focal"] = max(1e-6, cam["focal"] - step)
    return cam


# ───────────────────────── Coin camera bridge ─────────────────────────

def _vec(v):
    try:
        return tuple(v.getValue())
    except Exception:
        return (v[0], v[1], v[2])


def get_cam(node):
    name = str(node.getTypeId().getName())
    ortho = "Orthographic" in name
    cam = {"node": node, "ortho": ortho,
           "pos": _vec(node.position.getValue()),
           "quat": tuple(node.orientation.getValue().getValue()),
           "focal": node.focalDistance.getValue()}
    if ortho:
        cam["height"] = node.height.getValue()
    else:
        cam["angle"] = node.heightAngle.getValue()
    return cam


def set_cam(cam):
    node = cam["node"]
    node.position.setValue(*cam["pos"])
    node.orientation.setValue(*cam["quat"])
    node.focalDistance.setValue(cam["focal"])
    if cam["ortho"]:
        node.height.setValue(cam["height"])


# ───────────────────────── Qt event filter ─────────────────────────

def _enum(scope, dotted):
    """Qt5/Qt6-safe enum lookup, e.g. _enum(QtCore.Qt, 'ScrollPhase.NoScrollPhase')."""
    obj = scope
    try:
        for part in dotted.split("."):
            obj = getattr(obj, part)
        return obj
    except AttributeError:
        return getattr(scope, dotted.split(".")[-1], None)


class TrackpadFilter(QtCore.QObject if QtCore else object):
    """Installed on the 3D view; eats trackpad scroll/pinch when enabled()."""

    def __init__(self, enabled, get_view, settings, parent=None):
        super().__init__(parent)
        self.enabled = enabled          # callable -> bool
        self.get_view = get_view        # callable -> active View3DInventor or None
        self.settings = settings        # callable -> dict of speeds / inverts
        self.announced = False
        Q, E = QtCore.Qt, QtCore.QEvent
        self.WHEEL = _enum(E, "Type.Wheel")
        self.GESTURE = _enum(E, "Type.NativeGesture")
        self.NO_PHASE = _enum(Q, "ScrollPhase.NoScrollPhase")
        self.MOMENTUM = _enum(Q, "ScrollPhase.ScrollMomentum")
        self.ZOOM = _enum(Q, "NativeGestureType.ZoomNativeGesture")
        self.SMART = _enum(Q, "NativeGestureType.SmartZoomNativeGesture")
        self.SHIFT = _enum(Q, "KeyboardModifier.ShiftModifier")
        self.ALT = _enum(Q, "KeyboardModifier.AltModifier")

    def eventFilter(self, obj, ev):
        try:
            t = ev.type()
            if t != self.WHEEL and t != self.GESTURE:
                return False             # fast path: this runs for every app event
            if not self.enabled():
                return False
            view_w = self._view_widget(obj)
            if view_w is None:
                return False             # not aimed at a 3D view
            if t == self.WHEEL:
                return self._wheel(view_w, ev)
            return self._gesture(ev)
        except Exception as e:  # never let a gesture break the viewer
            try:
                import FreeCAD
                FreeCAD.Console.PrintError("SimpleCAD trackpad: {}\n".format(e))
            except Exception:
                pass
        return False

    @staticmethod
    def _view_widget(obj):
        """The 3D-view widget obj belongs to, or None (walks up the parents)."""
        w = obj
        for _ in range(8):
            if w is None or not hasattr(w, "metaObject"):
                return None
            try:
                name = w.metaObject().className()
            except Exception:
                return None
            if "Quarter" in name or "View3DInventor" in name or "SoQt" in name:
                return w
            try:
                w = w.parentWidget() if hasattr(w, "parentWidget") else None
            except Exception:
                return None
        return None

    def _node(self):
        view = self.get_view()
        return view.getCameraNode() if view is not None else None

    def _is_trackpad(self, ev):
        """Trackpads report scroll phases; plain mouse wheels don't.

        Some macOS/Qt builds send trackpad scrolls without phases, so on a Mac
        a pixel-precise delta also counts.
        """
        if ev.phase() != self.NO_PHASE:
            return True
        import sys
        return sys.platform == "darwin" and not ev.pixelDelta().isNull()

    def _wheel(self, obj, ev):
        if not self._is_trackpad(ev):
            return False                 # real mouse wheel: let FreeCAD zoom
        if ev.phase() == self.MOMENTUM:
            return True                  # swallow the coast-after-lift
        d = ev.pixelDelta()
        dx, dy = d.x(), d.y()
        if dx == 0 and dy == 0:
            a = ev.angleDelta()
            dx, dy = a.x() / 4.0, a.y() / 4.0
        if dx == 0 and dy == 0:
            return True                  # scroll begin/end markers
        mods = ev.modifiers()
        orbiting = bool(mods & self.SHIFT) or bool(mods & self.ALT)
        node = self._node()
        if node is None:
            return False
        s = self.settings()
        cam = get_cam(node)
        if orbiting:
            k = s["orbit"] / 200.0 * (-1 if s["invert_orbit"] else 1)
            orbit(cam, -dx * k, -dy * k)
        else:
            sign = -1 if s["invert_pan"] else 1
            pan(cam, dx * s["pan"] * sign, dy * s["pan"] * sign, obj.height())
        set_cam(cam)
        if not self.announced:
            self.announced = True
            try:
                import FreeCAD
                FreeCAD.Console.PrintMessage(
                    "SimpleCAD: trackpad gestures active (swipe = pan, "
                    "Shift/Option + swipe = orbit, pinch = zoom)\n")
            except Exception:
                pass
        return True

    def _gesture(self, ev):
        g = ev.gestureType()
        if g == self.ZOOM:
            node = self._node()
            if node is None:
                return False
            cam = get_cam(node)
            zoom(cam, ev.value() * self.settings()["zoom"])
            set_cam(cam)
            return True
        if g == self.SMART:
            try:
                import FreeCADGui
                FreeCADGui.SendMsgToActiveView("ViewFit")
            except Exception:
                pass
            return True
        return False
