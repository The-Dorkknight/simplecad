# SimpleCAD - a decluttered, Fusion-style workbench for FreeCAD
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Required Notice: Copyright Matthew Armstrong (https://github.com/The-Dorkknight)
# Licensed under the PolyForm Noncommercial License 1.0.0. No warranty.
#
# All the logic lives here; InitGui.py only registers the workbench.

import os

import FreeCAD as App
import FreeCADGui as Gui

try:
    from PySide import QtCore, QtGui, QtWidgets
except ImportError:  # very old FreeCAD shim
    from PySide import QtCore, QtGui
    QtWidgets = QtGui

VERSION = "0.9.3"
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

import SimpleCADPanel as Panel  # noqa: E402  (brushed-aluminium panel kit)

# ─────────────────────────── customise here ───────────────────────────
# Global FreeCAD toolbars left visible in normal mode (the nuke hides these too).
KEEP_TOOLBARS = {"File", "Edit", "Workbench", "View"}
# Never hidden, not even by Declutter: the way back to other workbenches.
NEVER_HIDE = {"Workbench"}
# Panels that survive the nuke (the task panel lives in these, so keep them).
KEEP_DOCKS = {"Combo View", "Model", "Tasks", "Tree view", "Property view"}
ICON_SIZE = 32
TEXT_UNDER_ICONS = True
# After FINISH SKETCH, jump straight into Extrude (Pad) with the sketch.
# Off by default so you can pick Revolve/Loft/Pocket instead.
AUTO_EXTRUDE = False
# Keyboard shortcut for the big red button ("" to disable).
TOGGLE_SHORTCUT = "Ctrl+Return"
# Brushed-aluminium plate + machined keys on SimpleCAD's tool rows too.
ALU_TOOLBARS = True
# Rising bubbles in the green "ACTIVE" badge (False = static badge).
ANIMATE_BADGE = True
# Enter/Return presses OK on tool dialogs (Pad, Pocket, Fillet, plane picker...).
ENTER_CONFIRMS = True
# SKETCH with nothing selected: show the planes and let you click one in the
# 3D view (False = FreeCAD's own plane list in the side panel).
PICK_PLANE_IN_VIEW = True
# Animated rainbow swirl on selected faces (toggle in More tools → Look).
SWIRL_SELECTION = True
SWIRL_OPACITY = 0.5                  # 0 = invisible .. 1 = solid paint

# FreeCAD 1.x flips to the Sketcher workbench whenever a sketch is edited,
# which would switch SimpleCAD off. Bounce straight back to SimpleCAD.
STAY_IN_SIMPLECAD = True
# FreeCAD opens in SimpleCAD (toggle in More tools), and a new Part Design
# document (e.g. the Start page's "Parametric Body") opens in SimpleCAD too.
START_IN_SIMPLECAD = True
FOLLOW_NEW_DOCUMENTS = True
BOUNCE_FROM = {"SketcherWorkbench", "PartDesignWorkbench"}

# Put every panel (model tree, task panel, report view, python console...)
# into one tabbed column on the left instead of floating over the 3D view.
TAB_PANELS_LEFT = True
LEFT_PANEL_WIDTH = 330

# Navigation presets cycled by the 🧭 button. Values go into FreeCAD's
# View preferences (originals are backed up once; "Restore" in More tools).
#   RotationMode: 0 = orbit around the centre of the screen
#                 1 = orbit around the point under the mouse
#                 2 = orbit around the object's centre
#   OrbitStyle:   0 = turntable (Z stays up, like Fusion), 1 = trackball
NAV_PRESETS = [
    # TinkerCAD underneath: a two-finger click-drag (= right-drag) orbits,
    # which works on a Mac trackpad; SimpleCAD adds the swipe/pinch gestures.
    ("Fusion Trackpad", {"NavigationStyle": "Gui::TinkerCADNavigationStyle",
                         "OrbitStyle": 0, "RotationMode": 0},
     "Two-finger swipe = pan (any direction) · Shift or Option + two-finger swipe = orbit · "
     "pinch = zoom · two-finger double-tap = fit all · two-finger click-drag also orbits."),
    ("TinkerCAD", {"NavigationStyle": "Gui::TinkerCADNavigationStyle",
                   "OrbitStyle": 0, "RotationMode": 0},
     "Right-drag (two-finger click-drag) = orbit around the screen centre · "
     "middle-drag = pan · wheel = zoom"),
    ("FreeCAD Touchpad", {"NavigationStyle": "Gui::TouchpadNavigationStyle",
                          "OrbitStyle": 0, "RotationMode": 0},
     "FreeCAD's built-in touchpad style. Hover the navigation name bottom-right of the "
     "window for its gestures"),
    ("Fusion Mouse", {"NavigationStyle": "Gui::RevitNavigationStyle",
                      "OrbitStyle": 0, "RotationMode": 0},
     "Needs a mouse with a middle button: middle-drag = pan · Shift + middle-drag = "
     "orbit around the screen centre · wheel = zoom (Fusion 360's buttons)"),
    ("Cursor Mouse", {"NavigationStyle": "Gui::RevitNavigationStyle",
                      "OrbitStyle": 0, "RotationMode": 1},
     "Needs a mouse with a middle button: Fusion buttons, but orbits around whatever is "
     "under the mouse"),
]
# Presets where SimpleCAD handles trackpad gestures itself (FreeCAD can't).
TOUCH_PRESETS = {"Fusion Trackpad"}
# Mouse-only presets are skipped by the 🧭 button on a Mac (still in the menu).
MOUSE_ONLY_PRESETS = {"Fusion Mouse", "Cursor Mouse"}
CYCLE_MOUSE_PRESETS = not __import__("sys").platform.startswith("darwin")
TRACKPAD_PAN_SPEED = 1.0
TRACKPAD_ORBIT_SPEED = 1.0       # radians per 200 px of finger travel
TRACKPAD_ZOOM_SPEED = 1.0

# ── Look & feel ──
# New solids get the active theme's look (existing files keep their colours
# unless you use "Restyle all solids" in More tools).
AUTO_STYLE = True
DISPLAY_MODE = "Flat Lines"          # shaded faces + visible edges
# While sketching, make the solid see-through so it doesn't hide the sketch.
GHOST_WHILE_SKETCHING = True
GHOST_TRANSPARENCY = 70              # percent
# Every face its own bright, see-through colour (toggle in More tools → Look).
RAINBOW_FACES = True
FACE_TRANSPARENCY = 30               # percent, 0 = solid
RAINBOW_SATURATION = 0.75            # 0 = white .. 1 = full colour

# Themes. "solid" styles your bodies; "viewport" is written to FreeCAD's own
# settings (your originals are backed up once and "Restore" puts them back).
# Colours in "viewport" are 0xRRGGBBAA.
THEMES = {
    "clean": {
        "label": "☀ Clean",
        "solid": {"color": (0.74, 0.77, 0.81), "edge": (0.15, 0.15, 0.17),
                  "width": 1.5, "glow": (0.0, 0.0, 0.0)},
        "viewport": {
            "Gradient": True, "Simple": False,
            "BackgroundColor2": 0xF4F6F9FF,       # gradient top
            "BackgroundColor3": 0xC9D0DAFF,       # gradient bottom
            "HighlightColor": 0x5FB4FFFF,         # hover
            "SelectionColor": 0x1E78E6FF,         # selected
            "DefaultShapeColor": 0xBCC4CFFF,
            "DefaultShapeLineColor": 0x26262BFF,
            "DefaultShapeLineWidth": 2,
            "RandomColor": False,                 # no random colour per part
            "EditedEdgeColor": 0x111111FF,        # sketch lines
            "EditedVertexColor": 0xE8731CFF,
            "ConstructionColor": 0x2B7BD6FF,
            "FullyConstrainedColor": 0x00A63EFF,
        },
    },
    "luminous": {
        "label": "🌙 Luminous",
        # Bright cyan with an emissive glow, hard white edges.
        "solid": {"color": (0.10, 0.85, 1.00), "edge": (1.0, 1.0, 1.0),
                  "width": 2.0, "glow": (0.02, 0.22, 0.28), "rainbow_glow": 0.35},
        "viewport": {
            "Gradient": True, "Simple": False,
            "BackgroundColor2": 0x05070BFF,       # almost black
            "BackgroundColor3": 0x141B2BFF,       # deep navy
            "HighlightColor": 0xFFF200FF,         # neon yellow hover
            "SelectionColor": 0xFF2BD6FF,         # hot magenta selection
            "DefaultShapeColor": 0x1AD9FFFF,
            "DefaultShapeLineColor": 0xFFFFFFFF,
            "DefaultShapeLineWidth": 2,
            "RandomColor": False,
            "EditedEdgeColor": 0xFFFFFFFF,        # white sketch lines
            "EditedVertexColor": 0xFFF200FF,      # yellow points
            "ConstructionColor": 0x3FA9FFFF,      # blue construction lines
            "FullyConstrainedColor": 0x39FF14FF,  # neon green when done
        },
    },
}
DEFAULT_THEME = "clean"

# A tuple means "first one that exists" (command names differ between versions).
SOLID_CMDS = [
    "PartDesign_Body",
    "Separator",
    "PartDesign_Pad",
    "PartDesign_Pocket",
    "PartDesign_Revolution",
    "PartDesign_AdditiveLoft",
    "PartDesign_AdditivePipe",
    "PartDesign_Hole",
    "Separator",
    "PartDesign_Fillet",
    "PartDesign_Chamfer",
    "PartDesign_Thickness",
    "Separator",
    "PartDesign_Mirrored",
    "PartDesign_LinearPattern",
    "PartDesign_PolarPattern",
]

SKETCH_CMDS = [
    "Sketcher_CreatePolyline",
    "Sketcher_CreateLine",
    "Sketcher_CreateRectangle",
    "Sketcher_CreateCircle",
    "Sketcher_CreateArc",
    "Sketcher_CreateSlot",
    "Separator",
    "Sketcher_CreateFillet",
    "Sketcher_Trimming",
    "Sketcher_Offset",
    ("Sketcher_Projection", "Sketcher_External"),
    "Sketcher_ToggleConstruction",
    "Separator",
    ("Sketcher_Dimension", "Sketcher_ConstrainDistance"),
    ("Sketcher_ConstrainCoincidentUnified", "Sketcher_ConstrainCoincident"),
    "Sketcher_ConstrainHorizontal",
    "Sketcher_ConstrainVertical",
    "Sketcher_ConstrainParallel",
    "Sketcher_ConstrainPerpendicular",
    "Sketcher_ConstrainTangent",
    "Sketcher_ConstrainEqual",
    "Sketcher_ConstrainSymmetric",
]

# Everything reachable from the "More tools" menu.
PD_ALL = SOLID_CMDS + [
    "PartDesign_SubtractiveLoft", "PartDesign_SubtractivePipe", "PartDesign_Groove",
    "PartDesign_AdditiveHelix", "PartDesign_SubtractiveHelix",
    "PartDesign_CompPrimitiveAdditive", "PartDesign_CompPrimitiveSubtractive",
    "PartDesign_Draft", "PartDesign_MultiTransform", "PartDesign_Boolean",
    "PartDesign_Plane", "PartDesign_Line", "PartDesign_Point", "PartDesign_CoordinateSystem",
    "PartDesign_ShapeBinder", "PartDesign_SubShapeBinder", "PartDesign_Clone",
    "PartDesign_MoveTip", "PartDesign_Migrate",
]
SK_ALL = SKETCH_CMDS + [
    "Sketcher_CreatePoint", "Sketcher_CreateEllipseByCenter", "Sketcher_CreatePolygon",
    "Sketcher_CreateBSpline", "Sketcher_Split", "Sketcher_Extend",
    "Sketcher_ConstrainLock", "Sketcher_ConstrainBlock", "Sketcher_ConstrainRadius",
    "Sketcher_ConstrainDiameter", "Sketcher_ConstrainAngle", "Sketcher_ConstrainPointOnObject",
    "Sketcher_Symmetry", "Sketcher_Clone", "Sketcher_RectangularArray",
    "Sketcher_ValidateSketch", "Sketcher_MapSketch", "Sketcher_ReorientSketch",
    "Sketcher_ViewSketch", "Sketcher_ViewSection",
]
# ──────────────────────────────────────────────────────────────────────

DECK_TB = "SimpleCAD Deck"
SOLID_TB = "SimpleCAD Solid"
SKETCH_TB = "SimpleCAD Sketch"
OURS = {DECK_TB, SOLID_TB, SKETCH_TB}


def available(cands):
    """Filter a command list down to what this FreeCAD actually has."""
    have = set(Gui.listCommands())
    out, seen = [], set()
    for c in cands:
        if c == "Separator":
            if out and out[-1] != "Separator":
                out.append(c)
            continue
        for alt in (c if isinstance(c, (tuple, list)) else (c,)):
            if alt in have:
                if alt not in seen:
                    out.append(alt)
                    seen.add(alt)
                break
    while out and out[-1] == "Separator":
        out.pop()
    return out


class _State:
    deck = None
    deck_tb = None
    timer = None
    hidden = {}      # toolbars we hid: name -> QToolBar
    docks = []       # docks hidden by the nuke
    statusbar = False
    nuked = False
    last_mode = None
    seen = {}        # doc name -> object names already known (for auto-style)
    ghosted = {}     # (doc, obj) -> original transparency
    shortcut = None
    theme = None     # name of the active look
    nav = None       # name of the active navigation preset
    active = False   # SimpleCAD is the current workbench
    sticky = False   # user is "in" SimpleCAD, so bounce back from auto-switches
    left_at = 0.0    # when SimpleCAD was last deactivated
    watch = None     # always-on timer for the bounce
    tabbed = set()   # dock objectNames already moved to the left
    had_task = False
    overlay_tries = 0
    overlay_last = 0.0
    touch = None     # trackpad gesture filter
    keys = None      # Enter = OK filter
    styled = {}      # (doc, obj) -> face count when we last coloured it
    dirty = set()
    flush_pending = False
    observer = None
    selobs = None    # selection observer
    sel_pending = False
    swirl = None     # rainbow swirl overlay
    picking = False  # waiting for a plane click
    pick_vis = []    # (obj, old visibility) to restore
    pick_planes = {}
    bounces = []     # recent automatic bounce-backs (loop guard)
    started = False
    close_guard = None
    docwatch = None
    new_doc_at = 0.0
    torn_down = True


S = _State()


def _mw():
    return Gui.getMainWindow()


def _toolbar(name):
    return _mw().findChild(QtWidgets.QToolBar, name)


def _log(msg):
    App.Console.PrintError("SimpleCAD: {}\n".format(msg))


def in_sketch():
    gd = Gui.ActiveDocument
    if gd is not None:
        try:
            vp = gd.getInEdit()
            obj = getattr(vp, "Object", None) if vp else None
            if obj is not None and "Sketch" in getattr(obj, "TypeId", ""):
                return True
        except Exception:
            pass
    # Fallback: "Leave sketch" is only available while a sketch is open.
    try:
        c = Gui.Command.get("Sketcher_LeaveSketch")
        return bool(c and c.isActive())
    except Exception:
        return False


def current_mode():
    """'sketch', 'task' (tool dialog open), 'pick' (choosing a plane) or 'solid'."""
    if in_sketch():
        return "sketch"
    if _task_open():
        return "task"
    if S.picking:
        return "pick"
    return "solid"


# ───────────────────────── pick a plane in the 3D view ─────────────────────────
# FreeCAD's own "new sketch" with nothing selected opens a list of planes in the
# side panel, which confuses beginners. Instead we show the body's three origin
# planes in the 3D view and wait for a click (or a TOP / FRONT / SIDE button).

PLANE_ROLES = {"XY": "XY_Plane", "XZ": "XZ_Plane", "YZ": "YZ_Plane"}


def _active_body(create=True):
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument()
    view = _active_view()
    body = None
    try:
        body = view.getActiveObject("pdbody") if view is not None else None
    except Exception:
        body = None
    if body is None:
        body = next((o for o in doc.Objects if o.TypeId == "PartDesign::Body"), None)
        if body is None and create:
            body = doc.addObject("PartDesign::Body", "Body")
            doc.recompute()
        if body is not None and view is not None:
            try:
                view.setActiveObject("pdbody", body)
            except Exception:
                pass
    return body


def _origin_planes(body):
    out = {}
    origin = getattr(body, "Origin", None)
    for f in getattr(origin, "OriginFeatures", []) if origin else []:
        role = getattr(f, "Role", "") or f.Name
        for key, r in PLANE_ROLES.items():
            if role.startswith(r) or f.Name.startswith(r):
                out[key] = f
    return out


def start_pick():
    """Show the origin planes and wait for the user to click one (or a face)."""
    try:
        body = _active_body()
        if body is None:
            return
        planes = _origin_planes(body)
        S.pick_vis = []
        origin = getattr(body, "Origin", None)
        for o in [origin] + list(planes.values()):
            try:
                if o is not None:
                    S.pick_vis.append((o, o.ViewObject.Visibility))
                    o.ViewObject.Visibility = True
            except Exception:
                pass
        S.pick_planes = planes
        S.picking = True
        if S.swirl:
            S.swirl.clear()
        Gui.Selection.clearSelection()
        if planes:
            try:
                Gui.activeDocument().activeView().viewIsometric()
                Gui.SendMsgToActiveView("ViewFit")
            except Exception:
                pass
        _msg("Click a plane (or a face) in the 3D view, or press TOP / FRONT / SIDE.")
    except Exception as e:
        _log("pick plane: {}".format(e))
    refresh()


def end_pick():
    S.picking = False
    for o, vis in S.pick_vis:
        try:
            o.ViewObject.Visibility = vis
        except Exception:
            pass
    S.pick_vis = []
    refresh()


def pick_plane(key):
    """TOP / FRONT / SIDE buttons: select that origin plane, which starts the sketch."""
    plane = S.pick_planes.get(key)
    if plane is None:
        return
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(plane)     # the selection observer takes it from here


def _picked_something():
    try:
        for s in Gui.Selection.getSelectionEx():
            if s.Object.TypeId in ("App::Plane", "PartDesign::Plane", "App::Origin"):
                return True
            if any(n.startswith("Face") for n in s.SubElementNames):
                return True
    except Exception:
        pass
    return False


# ───────────────────────────── actions ─────────────────────────────

def go_sketch():
    if in_sketch() or _task_open():
        return
    try:
        if App.ActiveDocument is None:
            App.newDocument()
        sel = Gui.Selection.getSelection()
        if len(sel) == 1 and sel[0].TypeId == "Sketcher::SketchObject":
            Gui.ActiveDocument.setEdit(sel[0].Name)   # edit selected sketch
        elif not sel and PICK_PLANE_IN_VIEW and not S.picking:
            start_pick()                              # click a plane in the 3D view
            return
        else:
            # With a face or plane selected this sketches straight onto it.
            cmd = available([("PartDesign_NewSketch", "Sketcher_NewSketch")])
            if cmd:
                Gui.runCommand(cmd[0])
    except Exception as e:
        _log(e)
    refresh()


def go_solid():
    if not in_sketch():
        return
    try:
        sketch = Gui.ActiveDocument.getInEdit().Object
        if "Sketcher_LeaveSketch" in Gui.listCommands():
            Gui.runCommand("Sketcher_LeaveSketch")
        else:
            Gui.ActiveDocument.resetEdit()
        if App.ActiveDocument:
            App.ActiveDocument.recompute()
        # Leave the finished sketch selected, so Extrude/Revolve/etc. is one click.
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(sketch)
        if AUTO_EXTRUDE and "PartDesign_Pad" in Gui.listCommands():
            QtCore.QTimer.singleShot(150, lambda: Gui.runCommand("PartDesign_Pad"))
    except Exception as e:
        _log(e)
    refresh()


def _in_dock(w):
    while w is not None:
        if isinstance(w, QtWidgets.QDockWidget):
            return True
        w = w.parentWidget()
    return False


def confirm_task():
    """Press OK on whatever tool dialog is open in the task panel (Pad, Fillet...)."""
    # 1) FreeCAD's own route: TaskDialog.accept() clicks the dialog's OK for us.
    try:
        dlg = Gui.Control.activeTaskDialog()
        if dlg is not None and hasattr(dlg, "accept"):
            dlg.accept()          # FreeCAD may close the panel a moment later,
            return True           # so don't fall through and click twice
    except Exception:
        pass
    # 2) Fallback: find the OK button ourselves. Don't require it to be on
    #    screen - it counts as hidden whenever the Tasks tab isn't in front.
    std = getattr(QtWidgets.QDialogButtonBox, "StandardButton", QtWidgets.QDialogButtonBox)
    role = getattr(QtWidgets.QDialogButtonBox, "ButtonRole", QtWidgets.QDialogButtonBox)
    for bb in _mw().findChildren(QtWidgets.QDialogButtonBox):
        try:
            if not _in_dock(bb):
                continue
            ok = bb.button(std.Ok)
            if ok is None:
                ok = next((b for b in bb.buttons()
                           if bb.buttonRole(b) == role.AcceptRole), None)
            if ok is not None and not ok.isHidden() and ok.isEnabled():
                ok.click()
                return True
        except RuntimeError:
            pass
    if _task_open():
        _msg("Couldn't press OK - finish the step in the Tasks tab.")
    return False


def _face_axes(normal):
    """Camera axes looking straight at a face: z out of the face, y kept 'up'."""
    z = App.Vector(normal)
    z.normalize()
    up = App.Vector(0, 0, 1) if abs(z.z) < 0.9 else App.Vector(0, 1, 0)
    y = up - z * up.dot(z)
    y.normalize()
    x = y.cross(z)
    x.normalize()
    return x, y, z


def snap_to_face():
    """Look straight at the selected face (or sketch), and zoom to it."""
    view = _active_view()
    if view is None:
        return
    try:
        sel = Gui.Selection.getSelectionEx()
        normal = None
        for s in sel:
            for sub in getattr(s, "SubObjects", []):
                if getattr(sub, "ShapeType", "") == "Face":
                    u0, u1, v0, v1 = sub.ParameterRange
                    normal = sub.normalAt((u0 + u1) / 2, (v0 + v1) / 2)
                    break
            if normal is not None:
                break
        if normal is None:
            # a whole sketch / datum plane selected, or sitting in a sketch
            obj = sel[0].Object if sel else None
            if obj is None and in_sketch():
                obj = Gui.ActiveDocument.getInEdit().Object
            if obj is not None and hasattr(obj, "getGlobalPlacement"):
                normal = obj.getGlobalPlacement().Rotation.multVec(App.Vector(0, 0, 1))
        if normal is None:
            _msg("Select a face first, then press SNAP TO FACE.")
            return
        x, y, z = _face_axes(normal)
        view.setCameraOrientation(App.Rotation(x, y, z, "ZYX"))
        if sel:
            Gui.SendMsgToActiveView("ViewSelection")
        else:
            Gui.SendMsgToActiveView("ViewFit")
    except Exception as e:
        _log("snap to face: {}".format(e))


def toggle_mode():
    """The big red button: start a sketch, finish it, or OK the open tool."""
    mode = current_mode()
    if mode == "sketch":
        go_solid()
    elif mode == "task":
        confirm_task()   # never start a sketch on top of an open dialog
    elif mode == "pick":
        end_pick()
    else:
        go_sketch()
    refresh()


def toggle_auto_extrude():
    global AUTO_EXTRUDE
    AUTO_EXTRUDE = not AUTO_EXTRUDE


def declutter():
    """Hide every main-window toolbar that isn't ours (or kept).

    FreeCAD saves toolbar visibility and restores it on the next launch, but
    it skips toolbars whose show/hide menu entry is hidden. So we hide that
    entry too: FreeCAD never records our hiding, and a fresh start (with or
    without SimpleCAD) always gets every toolbar back.
    """
    m = _mw()
    for tb in m.findChildren(QtWidgets.QToolBar):
        try:
            if m.toolBarArea(tb) == QtCore.Qt.NoToolBarArea:
                continue  # toolbar embedded in some panel, leave it
            name = tb.objectName()
            if name in OURS or name in NEVER_HIDE or not tb.isVisible():
                continue
            if not S.nuked and name in KEEP_TOOLBARS:
                continue
            S.hidden[name] = tb
            tb.toggleViewAction().setVisible(False)   # -> FreeCAD won't save it
            tb.hide()
        except RuntimeError:
            pass


def restore_toolbars(only=None):
    for name, tb in list(S.hidden.items()):
        if only is not None and name not in only:
            continue
        try:
            tb.toggleViewAction().setVisible(True)
            tb.show()
        except RuntimeError:
            pass
        del S.hidden[name]


def nuke():
    m = _mw()
    S.nuked = not S.nuked
    if S.nuked:
        declutter()
        for dw in m.findChildren(QtWidgets.QDockWidget):
            if dw.isVisible() and dw.objectName() not in KEEP_DOCKS:
                S.docks.append(dw)
                dw.hide()
        if m.statusBar().isVisible():
            S.statusbar = True
            m.statusBar().hide()
        App.ParamGet(SC_PARAMS).SetBool("ClutterHidden", True)   # for startup repair
        App.Console.PrintMessage("SimpleCAD: 💥 clutter nuked. Press again to undo.\n")
    else:
        for dw in S.docks:
            try:
                dw.show()
            except RuntimeError:
                pass
        S.docks = []
        if S.statusbar:
            m.statusBar().show()
            S.statusbar = False
        App.ParamGet(SC_PARAMS).SetBool("ClutterHidden", False)
        restore_toolbars(only=KEEP_TOOLBARS)
    if S.deck:
        S.deck.set_nuked(S.nuked)


def about():
    QtWidgets.QMessageBox.information(
        Gui.getMainWindow(), "About SimpleCAD",
        "SimpleCAD %s\n\nRequired Notice: Copyright Matthew Armstrong "
        "(https://github.com/The-Dorkknight)\n\nLicensed under the PolyForm "
        "Noncommercial License 1.0.0 (source-available, non-commercial use only). "
        "No warranty; use at your own risk.\n\n"
        "https://github.com/The-Dorkknight/simplecad" % VERSION)


def show_everything():
    if S.nuked:
        nuke()
    restore_toolbars()


def full_partdesign():
    Gui.activateWorkbench("PartDesignWorkbench")


# ─────────────────────────── look & feel ───────────────────────────

VIEW_PARAMS = "User parameter:BaseApp/Preferences/View"
BACKUP_PARAMS = "User parameter:BaseApp/Preferences/Mod/SimpleCAD/ViewBackup"


def _is_solid(obj):
    try:
        return (obj.isDerivedFrom("Part::Feature")
                and not obj.isDerivedFrom("Part::Part2DObject")   # sketches
                and not obj.isDerivedFrom("PartDesign::Datum")
                and getattr(obj, "ViewObject", None) is not None)
    except Exception:
        return False


def _palette():
    return THEMES.get(S.theme or DEFAULT_THEME, THEMES[DEFAULT_THEME])["solid"]


def _set_glow(vo, glow):
    """Emissive colour = the solid gives off its own light (FreeCAD 1.x and 0.2x)."""
    try:
        if hasattr(vo, "ShapeAppearance"):          # FreeCAD 1.x
            mats = list(vo.ShapeAppearance)
            for m in mats:
                m.EmissiveColor = glow
            vo.ShapeAppearance = mats
        elif hasattr(vo, "ShapeMaterial"):          # FreeCAD 0.2x
            m = vo.ShapeMaterial
            m.EmissiveColor = glow
            vo.ShapeMaterial = m
    except Exception:
        pass


def _rainbow_on():
    return App.ParamGet(SC_PARAMS).GetBool("RainbowFaces", RAINBOW_FACES)


def toggle_rainbow():
    App.ParamGet(SC_PARAMS).SetBool("RainbowFaces", not _rainbow_on())
    restyle_all(all_docs=True)


def face_colours(n, glow):
    """n bright, clearly different colours (golden-ratio hue steps)."""
    import colorsys
    out = []
    for i in range(n):
        h = (0.13 + i * 0.618033988749895) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, RAINBOW_SATURATION, 1.0)
        out.append(((r, g, b), tuple(c * glow for c in (r, g, b))))
    return out


def _face_count(obj):
    try:
        return len(obj.Shape.Faces)
    except Exception:
        return 0


def _paint_faces(vo, n, pal):
    """Give each face its own bright, see-through colour."""
    t = FACE_TRANSPARENCY / 100.0
    cols = face_colours(n, pal.get("rainbow_glow", 0.0))
    try:
        vo.Transparency = FACE_TRANSPARENCY
    except Exception:
        pass
    if hasattr(vo, "ShapeAppearance") and hasattr(App, "Material"):    # FreeCAD 1.x
        mats = []
        for (rgb, emis) in cols:
            m = App.Material()
            m.DiffuseColor = rgb
            m.AmbientColor = tuple(c * 0.3 for c in rgb)
            m.SpecularColor = (0.35, 0.35, 0.35)
            m.EmissiveColor = emis
            m.Shininess = 0.5
            m.Transparency = t
            mats.append(m)
        vo.ShapeAppearance = mats
    elif hasattr(vo, "DiffuseColor"):                                    # FreeCAD 0.2x
        vo.DiffuseColor = [rgb + (t,) for rgb, _ in cols]


def style_obj(obj):
    pal = _palette()
    vo = obj.ViewObject
    n = _face_count(obj)
    rainbow = _rainbow_on() and n > 0
    props = [("LineColor", pal["edge"]), ("LineWidth", pal["width"])]
    if not rainbow:
        props.insert(0, ("ShapeColor", pal["color"]))
    for prop, val in props:
        try:
            if hasattr(vo, prop):
                setattr(vo, prop, val)
        except Exception:
            pass
    try:
        if DISPLAY_MODE in vo.listDisplayModes():
            vo.DisplayMode = DISPLAY_MODE
    except Exception:
        pass
    if rainbow:
        try:
            _paint_faces(vo, n, pal)
        except Exception as e:
            _log("face colours: {}".format(e))
    else:
        _set_glow(vo, pal["glow"])
    S.styled[(obj.Document.Name, obj.Name)] = n


class _RestyleOnRecompute:
    """A Pad/Pocket changes the face count, so recolour our solids after recomputes."""

    def slotRecomputedObject(self, obj):
        try:
            key = (obj.Document.Name, obj.Name)
        except Exception:
            return
        if key in S.styled:
            S.dirty.add(key)
            if not S.flush_pending:
                S.flush_pending = True
                QtCore.QTimer.singleShot(0, _flush_restyle)


def _flush_restyle():
    S.flush_pending = False
    keys, S.dirty = S.dirty, set()
    for dn, on in keys:
        try:
            obj = App.getDocument(dn).getObject(on)
        except Exception:
            obj = None
        if obj is not None and _is_solid(obj) and _face_count(obj) != S.styled.get((dn, on)):
            style_obj(obj)


def _watch_recomputes():
    if S.observer is None:
        S.observer = _RestyleOnRecompute()
        try:
            App.addDocumentObserver(S.observer)
        except Exception as e:
            _log(e)


def restyle_all(all_docs=False):
    docs = App.listDocuments().values() if all_docs else [App.ActiveDocument]
    for doc in docs:
        if doc is None:
            continue
        for o in doc.Objects:
            if _is_solid(o):
                style_obj(o)


def _auto_style():
    """Style solids created this session; leave ones loaded from a file alone."""
    for doc in App.listDocuments().values():
        seen = S.seen.get(doc.Name)
        names = {o.Name for o in doc.Objects}
        if seen is None:
            S.seen[doc.Name] = names       # first look at this doc: just remember
            continue
        new = names - seen
        if new:
            for n in new:
                o = doc.getObject(n)
                if o is not None and _is_solid(o):
                    style_obj(o)
            seen |= new


def ghost(on):
    if on:
        doc = App.ActiveDocument
        if doc is None:
            return
        for o in doc.Objects:
            if _is_solid(o):
                vo = o.ViewObject
                try:
                    if (doc.Name, o.Name) in S.ghosted:
                        continue
                    if vo.Visibility and hasattr(vo, "Transparency"):
                        S.ghosted[(doc.Name, o.Name)] = vo.Transparency
                        vo.Transparency = max(vo.Transparency, GHOST_TRANSPARENCY)
                except Exception:
                    pass
    else:
        for (dn, on_), t in S.ghosted.items():
            try:
                App.getDocument(dn).getObject(on_).ViewObject.Transparency = t
            except Exception:
                pass
        S.ghosted = {}


def toggle_ghost():
    global GHOST_WHILE_SKETCHING
    GHOST_WHILE_SKETCHING = not GHOST_WHILE_SKETCHING
    if in_sketch():
        ghost(GHOST_WHILE_SKETCHING)


def _param_get(grp, key, sample):
    if isinstance(sample, bool):
        return grp.GetBool(key, sample)
    if isinstance(sample, str):
        return grp.GetString(key, sample)
    return grp.GetUnsigned(key, sample) if sample > 0xFFFF else grp.GetInt(key, sample)


def _param_set(grp, key, val):
    if isinstance(val, bool):
        grp.SetBool(key, val)
    elif isinstance(val, str):
        grp.SetString(key, val)
    elif val > 0xFFFF:
        grp.SetUnsigned(key, val)
    else:
        grp.SetInt(key, val)


SC_PARAMS = "User parameter:BaseApp/Preferences/Mod/SimpleCAD"


def _all_viewport_keys():
    keys = {}
    for t in THEMES.values():
        keys.update(t["viewport"])
    return keys


def apply_theme(name):
    """Switch look: viewport colours + restyle solids in every open document."""
    if name not in THEMES:
        return
    view = App.ParamGet(VIEW_PARAMS)
    backup = App.ParamGet(BACKUP_PARAMS)
    if not backup.GetBool("_saved", False):
        for k, v in _all_viewport_keys().items():
            _param_set(backup, k, _param_get(view, k, v))
        backup.SetBool("_saved", True)
    for k, v in THEMES[name]["viewport"].items():
        _param_set(view, k, v)
    S.theme = name
    App.ParamGet(SC_PARAMS).SetString("Theme", name)
    restyle_all(all_docs=True)
    if S.deck:
        S.deck.set_theme(name)
    _msg("{} theme on. If the background didn't change, restart FreeCAD once."
         .format(THEMES[name]["label"]))


def toggle_luminous():
    apply_theme("clean" if S.theme == "luminous" else "luminous")


def restore_viewport_theme():
    view = App.ParamGet(VIEW_PARAMS)
    backup = App.ParamGet(BACKUP_PARAMS)
    if not backup.GetBool("_saved", False):
        _msg("Nothing to restore - no theme was ever applied.")
        return
    for k, v in _all_viewport_keys().items():
        _param_set(view, k, _param_get(backup, k, v))
    backup.SetBool("_saved", False)
    S.theme = None
    App.ParamGet(SC_PARAMS).SetString("Theme", "")
    if S.deck:
        S.deck.set_theme(None)
    _msg("Original FreeCAD viewport settings restored.")


def load_saved_theme():
    t = App.ParamGet(SC_PARAMS).GetString("Theme", "")
    S.theme = t if t in THEMES else None
    n = App.ParamGet(SC_PARAMS).GetString("Nav", "")
    S.nav = n if n in [p[0] for p in NAV_PRESETS] else None


# ─────────────────────────── navigation ───────────────────────────

NAV_BACKUP = "User parameter:BaseApp/Preferences/Mod/SimpleCAD/NavBackup"


def _nav_keys():
    keys = {}
    for _, vals, _ in NAV_PRESETS:
        keys.update(vals)
    return keys


def _views():
    out = []
    try:
        for name in App.listDocuments():
            gd = Gui.getDocument(name)
            out += gd.mdiViewsOfType("Gui::View3DInventor")
    except Exception:
        pass
    return out


def apply_nav(name):
    preset = next((p for p in NAV_PRESETS if p[0] == name), None)
    if preset is None:
        return
    view = App.ParamGet(VIEW_PARAMS)
    backup = App.ParamGet(NAV_BACKUP)
    if not backup.GetBool("_saved", False):
        for k, v in _nav_keys().items():
            _param_set(backup, k, _param_get(view, k, v))
        backup.SetBool("_saved", True)
    for k, v in preset[1].items():
        _param_set(view, k, v)
    # Open views pick most of this up by themselves; the style needs a nudge.
    for v in _views():
        try:
            v.setNavigationType(preset[1]["NavigationStyle"])
        except Exception:
            pass
    S.nav = name
    App.ParamGet(SC_PARAMS).SetString("Nav", name)
    attach_trackpad()
    if S.deck:
        S.deck.set_nav(name)
    _msg("Navigation: {}. {}".format(name, preset[2]))


def cycle_nav():
    names = [p[0] for p in NAV_PRESETS
             if CYCLE_MOUSE_PRESETS or p[0] not in MOUSE_ONLY_PRESETS]
    i = names.index(S.nav) + 1 if S.nav in names else 0
    apply_nav(names[i % len(names)])


def restore_nav():
    view = App.ParamGet(VIEW_PARAMS)
    backup = App.ParamGet(NAV_BACKUP)
    if not backup.GetBool("_saved", False):
        _msg("Nothing to restore - navigation was never changed.")
        return
    for k, v in _nav_keys().items():
        _param_set(view, k, _param_get(backup, k, v))
    style = backup.GetString("NavigationStyle", "")
    for v in _views():
        try:
            if style:
                v.setNavigationType(style)
        except Exception:
            pass
    backup.SetBool("_saved", False)
    S.nav = None
    App.ParamGet(SC_PARAMS).SetString("Nav", "")
    if S.deck:
        S.deck.set_nav(None)
    _msg("Original FreeCAD navigation restored.")


# ─────────────────────────── trackpad ───────────────────────────

def _touch_on():
    return S.nav in TOUCH_PRESETS


def _touch_settings():
    p = App.ParamGet(SC_PARAMS)
    return {"pan": TRACKPAD_PAN_SPEED, "orbit": TRACKPAD_ORBIT_SPEED,
            "zoom": TRACKPAD_ZOOM_SPEED,
            "invert_pan": p.GetBool("InvertPan", False),
            "invert_orbit": p.GetBool("InvertOrbit", False)}


def _toggle_param(key):
    p = App.ParamGet(SC_PARAMS)
    p.SetBool(key, not p.GetBool(key, False))


def _active_view():
    try:
        v = Gui.ActiveDocument.ActiveView
        return v if hasattr(v, "getCameraNode") else None
    except Exception:
        return None


def attach_trackpad():
    """Install SimpleCAD's app-wide filters once: trackpad gestures + Enter = OK.

    App-wide rather than per-view, because FreeCAD's 3D view is built from
    several nested widgets (and differs between versions); the filter itself
    checks that the event is aimed at a 3D view before touching it.
    """
    if S.touch is not None:
        return
    app = QtWidgets.QApplication.instance()
    if app is None:
        return
    import SimpleCADTouch
    S.touch = SimpleCADTouch.TrackpadFilter(_touch_on, _active_view, _touch_settings, app)
    app.installEventFilter(S.touch)
    S.keys = EnterFilter(app)
    app.installEventFilter(S.keys)


# ─────────────────────── selection: plane pick + swirl ───────────────────────

class _SelectionWatcher:
    """FreeCAD selection observer. Work is deferred to the Qt loop, never done
    inside FreeCAD's callback."""

    def _kick(self):
        if not S.sel_pending:
            S.sel_pending = True
            QtCore.QTimer.singleShot(0, _on_selection)

    def addSelection(self, doc, obj, sub, pnt):
        self._kick()

    def removeSelection(self, doc, obj, sub):
        self._kick()

    def setSelection(self, doc):
        self._kick()

    def clearSelection(self, doc):
        self._kick()


def _swirl_on():
    return App.ParamGet(SC_PARAMS).GetBool("SwirlSelection", SWIRL_SELECTION)


def toggle_swirl():
    App.ParamGet(SC_PARAMS).SetBool("SwirlSelection", not _swirl_on())
    _on_selection()


def toggle_swirl_animation():
    p = App.ParamGet(SC_PARAMS)
    p.SetBool("AnimateSwirl", not p.GetBool("AnimateSwirl", True))
    if S.swirl:
        S.swirl.too_slow = False     # give it a fresh chance when turned back on
    _on_selection()


def _selected_faces():
    """Selected faces of real solids only (never datum/origin planes, which are
    huge and would paint the swirl across the whole view)."""
    faces = []
    try:
        for s in Gui.Selection.getSelectionEx():
            obj = s.Object
            if not _is_solid(obj) or obj.TypeId in ("App::Plane", "PartDesign::Plane"):
                continue
            for sub in getattr(s, "SubObjects", []):
                if getattr(sub, "ShapeType", "") == "Face":
                    faces.append(sub)
    except Exception:
        pass
    return faces


def _on_selection():
    S.sel_pending = False
    if not S.active:
        if S.swirl:
            S.swirl.clear()
        return
    if S.picking and _picked_something():
        end_pick()
        go_sketch()            # a plane/face is selected now -> sketch straight on it
        return
    if S.swirl is None:
        import SimpleCADSwirl
        S.swirl = SimpleCADSwirl.Swirl(
            _active_view, QtCore,
            animate=lambda: App.ParamGet(SC_PARAMS).GetBool("AnimateSwirl", True),
            alpha=lambda: SWIRL_OPACITY,
            on_slow=lambda: _msg("This PC is busy redrawing, so the rainbow swirl is "
                                 "now static (More tools → Look to change)."))
    if _swirl_on() and not in_sketch():
        S.swirl.show(_selected_faces())
    else:
        S.swirl.clear()


def _watch_selection():
    if S.selobs is None:
        S.selobs = _SelectionWatcher()
        try:
            Gui.Selection.addObserver(S.selobs)
        except Exception as e:
            _log(e)


def _ok_ready():
    """A tool dialog is open and its OK button is enabled."""
    if not _task_open():
        return False
    std = getattr(QtWidgets.QDialogButtonBox, "StandardButton", QtWidgets.QDialogButtonBox)
    for bb in _mw().findChildren(QtWidgets.QDialogButtonBox):
        try:
            if _in_dock(bb):
                ok = bb.button(std.Ok)
                if ok is not None and not ok.isHidden():
                    return ok.isEnabled()
        except RuntimeError:
            pass
    return True


# ─────────────────────── Enter = OK on tool dialogs ───────────────────────

class EnterFilter(QtCore.QObject):
    """Enter/Return presses OK on Pad, Pocket, Fillet... so no sidebar clicking.

    The key still reaches the field you're typing in first (so a value you just
    typed is committed), then OK is pressed a moment later. Left alone: sketch
    edit (Enter confirms on-screen dimensions there), the Python console and
    other text editors, and any pop-up dialog window.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        E = QtCore.QEvent
        T = getattr(E, "Type", E)
        # ShortcutOverride too: if anything claims Return as a shortcut, the
        # plain KeyPress never arrives.
        self.KEYTYPES = {T.KeyPress, T.ShortcutOverride}
        K = getattr(QtCore.Qt, "Key", QtCore.Qt)
        self.KEYS = {K.Key_Return, K.Key_Enter}
        self.MODS = (QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier
                     | QtCore.Qt.AltModifier | QtCore.Qt.MetaModifier)
        self.last = 0.0

    def eventFilter(self, obj, ev):
        try:
            if ev.type() not in self.KEYTYPES or ev.key() not in self.KEYS:
                return False
            if ev.isAutoRepeat() or (ev.modifiers() & self.MODS):
                return False
            if not ENTER_CONFIRMS or not S.active:
                return False
            import time
            if time.time() - self.last < 0.4:   # same press seen by parent widgets
                return False
            if QtWidgets.QApplication.activeModalWidget() is not None:
                return False
            if current_mode() != "task":
                return False
            fw = QtWidgets.QApplication.focusWidget()
            if isinstance(fw, (QtWidgets.QPlainTextEdit, QtWidgets.QTextEdit)):
                return False
            self.last = time.time()
            QtCore.QTimer.singleShot(120, _enter_confirm)
        except Exception as e:
            _log(e)
        return False


def _enter_confirm():
    if current_mode() == "task":
        confirm_task()
        QtCore.QTimer.singleShot(150, refresh)


# ─────────────────────────── panels ───────────────────────────

def _anchor_dock(docks):
    for name in ("Model", "Combo View", "Tree view"):
        for d in docks:
            if d.objectName() == name:
                return d
    return None


def _overlay_busy():
    """True if FreeCAD 1.x's overlay system is holding any panel."""
    for tw in _mw().findChildren(QtWidgets.QTabWidget):
        try:
            if "Overlay" in tw.metaObject().className() and tw.count() > 0:
                return True
        except RuntimeError:
            pass
    return False


def _in_main_layout(m, d):
    try:
        return d.isFloating() or m.dockWidgetArea(d) != QtCore.Qt.NoDockWidgetArea
    except Exception:
        return False


def release_overlays():
    """Ask FreeCAD itself to take every panel out of overlay mode.

    Std_DockOverlayAll toggles, but when any panel is in overlay it always
    switches ALL of them off, so it's safe to call only when one is busy.
    Never reparent overlay panels by hand: FreeCAD keeps track of them and
    crashes if they move behind its back.
    """
    import time
    if not _overlay_busy() or S.overlay_tries >= 3:
        return
    if time.time() - S.overlay_last < 5:
        return
    if "Std_DockOverlayAll" not in Gui.listCommands():
        return
    S.overlay_tries += 1
    S.overlay_last = time.time()
    try:
        Gui.runCommand("Std_DockOverlayAll")
    except Exception as e:
        _log("overlay: {}".format(e))
    if S.overlay_tries == 3 and _overlay_busy():
        _msg("A panel is still in FreeCAD's overlay mode. Hover over it and press F3 "
             "to dock it, then SimpleCAD will tab it on the left.")


def tab_panels(force=False):
    """Put every normally docked panel into one tabbed column on the left."""
    if not TAB_PANELS_LEFT and not force:
        return
    if _task_open() and not force:
        return          # never shuffle panels while a tool dialog is live
    release_overlays()
    m = _mw()
    docks = [d for d in m.findChildren(QtWidgets.QDockWidget)
             if d.objectName() and not d.isHidden() and _in_main_layout(m, d)]
    anchor = _anchor_dock(docks)
    if anchor is None:
        return
    left = QtCore.Qt.LeftDockWidgetArea
    todo = [d for d in docks if force or d.objectName() not in S.tabbed]
    if not todo:
        return
    try:
        if anchor in todo or m.dockWidgetArea(anchor) != left:
            anchor.setFloating(False)
            m.addDockWidget(left, anchor)
        for d in todo:
            S.tabbed.add(d.objectName())
            if d is anchor:
                continue
            d.setFloating(False)
            m.addDockWidget(left, d)
            m.tabifyDockWidget(anchor, d)
            d.show()
        try:
            m.setTabPosition(left, QtWidgets.QTabWidget.North)
        except Exception:
            pass
        m.resizeDocks([anchor], [LEFT_PANEL_WIDTH], QtCore.Qt.Horizontal)
        anchor.raise_()
    except Exception as e:
        _log("tabbing panels: {}".format(e))


def _raise_dock(names):
    m = _mw()
    for n in names:
        d = m.findChild(QtWidgets.QDockWidget, n)
        if d is not None and d.isVisible():
            d.raise_()
            return


def _task_open():
    try:
        return bool(Gui.Control.activeDialog())
    except Exception:
        return False


def _follow_tasks():
    """Bring the task tab forward when a dialog opens, the model tree when it closes."""
    t = _task_open()
    if t != S.had_task:
        S.had_task = t
        _raise_dock(["Tasks"] if t else ["Model", "Combo View", "Tree view"])


# ─────────────────────── stay in SimpleCAD ───────────────────────

def _wb_name():
    try:
        wb = Gui.activeWorkbench()
        try:
            return wb.name()
        except Exception:
            return type(wb).__name__
    except Exception:
        return ""


def _watch():
    """Undo FreeCAD's automatic workbench switches while editing.

    FreeCAD 1.x forces a switch when you open a sketch (to Sketcher) and when
    any Part Design tool dialog opens (Pad, Pocket, Fillet... to Part Design).
    We hop straight back. SimpleCAD isn't torn down in between (see
    deactivate), so Declutter, the deck and the buttons all stay as they were.
    """
    if not STAY_IN_SIMPLECAD:
        return
    import time
    now = time.time()
    if S.active:
        S.sticky = True
        return
    if (FOLLOW_NEW_DOCUMENTS and _start_in_simplecad() and now - S.new_doc_at < 3.0
            and _wb_name() == "PartDesignWorkbench"):
        S.new_doc_at = 0.0                  # once per new document
        try:
            Gui.activateWorkbench("SimpleCADWorkbench")
        except Exception as e:
            _log(e)
        return
    if not S.sticky:
        return
    if _wb_name() in BOUNCE_FROM and (in_sketch() or _task_open()):
        # loop guard: if FreeCAD keeps switching away, stop fighting it
        S.bounces = [t for t in S.bounces if now - t < 5.0] + [now]
        if len(S.bounces) > 4:
            S.sticky = False
            _finish_deactivate(force=True)
            _msg("FreeCAD keeps switching workbench, so SimpleCAD stepped aside. "
                 "Pick SimpleCAD again from the workbench list when you're ready.")
            return
        try:
            Gui.activateWorkbench("SimpleCADWorkbench")
        except Exception as e:
            _log(e)
            S.sticky = False
            _finish_deactivate(force=True)
        return
    # Switched away on purpose (not for an edit): stop following, tidy up.
    if now - S.left_at > 1.5:
        S.sticky = False
        _finish_deactivate()


# ─────────────────────── startup, quitting, new documents ───────────────────────

TOOLBAR_PREFS = "User parameter:BaseApp/MainWindow/Toolbars"
GENERAL_PREFS = "User parameter:BaseApp/Preferences/General"
ESSENTIAL_TOOLBARS = ("File", "Edit", "Workbench", "View")


def repair_toolbars():
    """Undo anything an older SimpleCAD left behind: essential toolbars, the
    workbench switcher and the status bar always come back at startup."""
    tp = App.ParamGet(TOOLBAR_PREFS)
    for name in ESSENTIAL_TOOLBARS:
        tp.SetBool(name, True)
    m = _mw()
    for tb in m.findChildren(QtWidgets.QToolBar):
        try:
            if tb.objectName() in ESSENTIAL_TOOLBARS and not tb.isVisible() \
                    and tb.objectName() not in S.hidden:
                tb.toggleViewAction().setVisible(True)
                tb.show()
        except RuntimeError:
            pass
    sc = App.ParamGet(SC_PARAMS)
    if sc.GetBool("ClutterHidden", False) and not S.nuked:
        m.statusBar().show()
        sc.SetBool("ClutterHidden", False)


class _CloseGuard(QtCore.QObject):
    """Before FreeCAD saves its window layout on quit, put everything back, so
    nothing SimpleCAD hid is remembered. If the quit is cancelled (unsaved
    work), the next event-loop turn hides it again."""

    def eventFilter(self, obj, ev):
        try:
            close = getattr(getattr(QtCore.QEvent, "Type", QtCore.QEvent), "Close")
            if obj is _mw() and ev.type() == close:
                was_nuked = S.nuked
                if S.nuked:
                    nuke()
                restore_toolbars()
                QtCore.QTimer.singleShot(0, lambda: _after_cancelled_close(was_nuked))
        except Exception as e:
            _log(e)
        return False


def _after_cancelled_close(was_nuked):
    if not S.active:
        return
    if was_nuked and not S.nuked:
        nuke()
    S.last_mode = None
    refresh()


class _NewDocWatcher:
    def slotCreatedDocument(self, doc):
        import time
        S.new_doc_at = time.time()


def _start_in_simplecad():
    return App.ParamGet(SC_PARAMS).GetBool("StartInSimpleCAD", START_IN_SIMPLECAD)


def set_start_in_simplecad(on):
    """FreeCAD opens in SimpleCAD (your previous start workbench is kept for 'off')."""
    sc, gen = App.ParamGet(SC_PARAMS), App.ParamGet(GENERAL_PREFS)
    sc.SetBool("StartInSimpleCAD", on)
    cur = gen.GetString("AutoloadModule", "")
    if on and cur != "SimpleCADWorkbench":
        sc.SetString("OldAutoloadModule", cur)
        gen.SetString("AutoloadModule", "SimpleCADWorkbench")
    elif not on and cur == "SimpleCADWorkbench":
        gen.SetString("AutoloadModule", sc.GetString("OldAutoloadModule", "PartDesignWorkbench")
                      or "PartDesignWorkbench")


def toggle_start_in_simplecad():
    set_start_in_simplecad(not _start_in_simplecad())


def startup():
    """Runs once when FreeCAD's window is up, even if SimpleCAD isn't active."""
    if S.started:
        return
    S.started = True
    try:
        repair_toolbars()
        S.close_guard = _CloseGuard(_mw())
        _mw().installEventFilter(S.close_guard)
        S.docwatch = _NewDocWatcher()
        App.addDocumentObserver(S.docwatch)
        if _start_in_simplecad():
            set_start_in_simplecad(True)    # keep FreeCAD's start workbench pointed at us
        if S.watch is None:
            S.watch = QtCore.QTimer()
            S.watch.timeout.connect(_watch)
            S.watch.start(150)
    except Exception as e:
        _log("startup: {}".format(e))


def _msg(t):
    App.Console.PrintMessage("SimpleCAD: {}\n".format(t))


# ───────────────────────────── widgets ─────────────────────────────

class CautionTape(QtWidgets.QWidget):
    """Yellow/black hazard-striped frame around a child widget."""

    def __init__(self, child, parent=None):
        super().__init__(parent)
        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(7, 7, 7, 7)
        lay.addWidget(child)

    def paintEvent(self, ev):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        r = self.rect()
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(r), 6, 6)
        p.setClipPath(path)
        p.fillRect(r, QtGui.QColor("#FFCC00"))
        p.setPen(QtCore.Qt.NoPen)
        p.setBrush(QtGui.QColor("#111111"))
        h, w = r.height(), 9
        x = -h
        while x < r.width() + h:
            p.drawPolygon(QtGui.QPolygonF([
                QtCore.QPointF(x, 0), QtCore.QPointF(x + w, 0),
                QtCore.QPointF(x + w + h, h), QtCore.QPointF(x + h, h)]))
            x += 2 * w
        p.end()


BIG_RED_CSS = """
QPushButton { color: white; font-weight: 900; font-size: 17px; padding: 10px 28px;
  min-width: 190px; border: 3px solid #4a0000; border-radius: 12px;
  background: qradialgradient(cx:0.5, cy:0.35, radius:0.9, fx:0.5, fy:0.3,
      stop:0 #ff6b6b, stop:0.55 #d10000, stop:1 #6e0000); }
QPushButton:hover { background: qradialgradient(cx:0.5, cy:0.35, radius:0.9, fx:0.5, fy:0.3,
      stop:0 #ff8f8f, stop:0.55 #f01010, stop:1 #8a0000); }
QPushButton:pressed { background: #5a0000; padding-top: 12px; padding-bottom: 8px; }
"""

class BubbleBadge(QtWidgets.QWidget):
    """Cartoon acid-green 'X ACTIVE' badge with a few rising bubbles.

    Cheap on purpose: ~10 circles, 20 fps, and the timer only runs while the
    badge is actually on screen.
    """
    TEXT = {"sketch": "✏  SKETCH ACTIVE", "solid": "⬛  SOLID ACTIVE",
            "task": "⚙  TOOL ACTIVE", "pick": "👆  PICK A PLANE"}
    N_BUBBLES = 16

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(220, 62)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.mode = "solid"
        import random
        self._rnd = random.Random(7)
        self.bubbles = [self._new_bubble(start=True) for _ in range(self.N_BUBBLES)]
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._tick)

    def sizeHint(self):
        return QtCore.QSize(220, 62)

    def _new_bubble(self, start=False):
        r = self._rnd
        w, h = max(self.width(), 250), max(self.height(), 62)
        return [r.uniform(14, w - 14),                       # x
                r.uniform(8, h) if start else h + r.uniform(2, 14),  # y
                r.uniform(3.0, 8.0),                          # radius
                r.uniform(0.6, 1.8),                          # rise speed
                r.uniform(0, 6.28)]                           # wobble phase

    def set_mode(self, mode):
        if mode != self.mode:
            self.mode = mode
            self.update()

    def showEvent(self, e):
        if ANIMATE_BADGE:
            self.timer.start(50)
        super().showEvent(e)

    def hideEvent(self, e):
        self.timer.stop()
        super().hideEvent(e)

    def _tick(self):
        import math
        for b in self.bubbles:
            b[1] -= b[3]
            b[4] += 0.15
            b[0] += math.sin(b[4]) * 0.35
            if b[1] < -b[2]:
                b[:] = self._new_bubble()
        self.update()

    def paintEvent(self, ev):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        r = QtCore.QRectF(self.rect()).adjusted(2, 2, -2, -2)
        path = QtGui.QPainterPath()
        path.addRoundedRect(r, 14, 14)

        g = QtGui.QLinearGradient(0, r.top(), 0, r.bottom())
        g.setColorAt(0.0, QtGui.QColor("#E4FF3A"))
        g.setColorAt(0.5, QtGui.QColor("#9DFF00"))
        g.setColorAt(1.0, QtGui.QColor("#2FD600"))
        p.fillPath(path, g)

        p.save()
        p.setClipPath(path)
        p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 190), 1.4))
        p.setBrush(QtGui.QColor(255, 255, 255, 70))
        for x, y, rad, _, _ in self.bubbles:
            p.drawEllipse(QtCore.QPointF(x, y), rad, rad)
        p.setPen(QtCore.Qt.NoPen)
        p.setBrush(QtGui.QColor(255, 255, 255, 220))
        for x, y, rad, _, _ in self.bubbles:
            p.drawEllipse(QtCore.QPointF(x - rad * 0.35, y - rad * 0.35),
                          rad * 0.28, rad * 0.28)
        # glossy cartoon highlight
        p.setBrush(QtGui.QColor(255, 255, 255, 75))
        p.drawRoundedRect(QtCore.QRectF(r.left() + 10, r.top() + 4,
                                        r.width() - 20, r.height() * 0.32), 8, 8)
        p.restore()

        p.setPen(QtGui.QPen(QtGui.QColor("#1B4D00"), 3))
        p.setBrush(QtCore.Qt.NoBrush)
        p.drawPath(path)

        f = self.font()
        f.setBold(True)
        f.setPixelSize(17)
        try:
            f.setWeight(QtGui.QFont.Black)
        except Exception:
            pass
        p.setFont(f)
        text = self.TEXT.get(self.mode, "")
        p.setPen(QtGui.QColor(255, 255, 255, 170))
        p.drawText(r.translated(0, 1.5), QtCore.Qt.AlignCenter, text)
        p.setPen(QtGui.QColor("#0E2A00"))
        p.drawText(r, QtCore.Qt.AlignCenter, text)
        p.end()


class CrosshairButton(QtWidgets.QAbstractButton):
    """Big dark button with a rainbow crosshair: SNAP TO FACE."""

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFixedSize(210, 62)
        self._hover = False

    def enterEvent(self, e):
        self._hover = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hover = False
        self.update()
        super().leaveEvent(e)

    def paintEvent(self, ev):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        r = QtCore.QRectF(self.rect()).adjusted(2, 2, -2, -2)
        down = self.isDown()
        if down:
            r.translate(0, 1.5)
        g = QtGui.QLinearGradient(0, r.top(), 0, r.bottom())
        g.setColorAt(0, QtGui.QColor("#3a4a6b" if self._hover else "#2c3852"))
        g.setColorAt(1, QtGui.QColor("#121826"))
        path = QtGui.QPainterPath()
        path.addRoundedRect(r, 14, 14)
        p.fillPath(path, g)
        # rainbow rim
        rim = QtGui.QConicalGradient(r.center(), 90)
        for i, c in enumerate(("#ff3b3b", "#ffb300", "#f5ff3a", "#39ff14",
                               "#00e5ff", "#3d5afe", "#d500f9", "#ff3b3b")):
            rim.setColorAt(i / 7.0, QtGui.QColor(c))
        p.setPen(QtGui.QPen(QtGui.QBrush(rim), 3))
        p.drawPath(path)

        # crosshair icon
        cx, cy, R = r.left() + 34, r.center().y(), 17.0
        ring = QtGui.QConicalGradient(QtCore.QPointF(cx, cy), 0)
        for i, c in enumerate(("#ff3b3b", "#ffb300", "#39ff14", "#00e5ff",
                               "#d500f9", "#ff3b3b")):
            ring.setColorAt(i / 5.0, QtGui.QColor(c))
        p.setPen(QtGui.QPen(QtGui.QBrush(ring), 3.5))
        p.setBrush(QtCore.Qt.NoBrush)
        p.drawEllipse(QtCore.QPointF(cx, cy), R, R)
        for (dx, dy), col in (((0, -1), "#ff3b3b"), ((1, 0), "#39ff14"),
                              ((0, 1), "#00e5ff"), ((-1, 0), "#ffb300")):
            p.setPen(QtGui.QPen(QtGui.QColor(col), 3, QtCore.Qt.SolidLine,
                                QtCore.Qt.RoundCap))
            p.drawLine(QtCore.QPointF(cx + dx * (R - 9), cy + dy * (R - 9)),
                       QtCore.QPointF(cx + dx * (R + 6), cy + dy * (R + 6)))
        p.setPen(QtCore.Qt.NoPen)
        p.setBrush(QtGui.QColor("white"))
        p.drawEllipse(QtCore.QPointF(cx, cy), 3, 3)

        f = self.font()
        f.setBold(True)
        f.setPixelSize(17)
        p.setFont(f)
        p.setPen(QtGui.QColor("white"))
        p.drawText(r.adjusted(62, 0, -8, 0), QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft,
                   self.text())
        p.end()


class EnterButton(QtWidgets.QAbstractButton):
    """Big ⏎ ENTER key: grey when there's nothing to confirm, pulsing red when a
    tool dialog is open and ready for OK."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFixedSize(170, 62)
        self.ready = False
        self.phase = 0.0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.setEnabled(False)

    def set_ready(self, ready):
        if ready == self.ready:
            return
        self.ready = ready
        self.setEnabled(ready)
        if ready and self.isVisible():
            self.timer.start(50)
        else:
            self.timer.stop()
        self.update()

    def showEvent(self, e):
        if self.ready:
            self.timer.start(50)
        super().showEvent(e)

    def hideEvent(self, e):
        self.timer.stop()
        super().hideEvent(e)

    def _tick(self):
        self.phase = (self.phase + 0.05 / 0.9) % 1.0     # one pulse every 0.9 s
        self.update()

    def paintEvent(self, ev):
        import math
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        r = QtCore.QRectF(self.rect()).adjusted(3, 3, -3, -3)
        if self.isDown():
            r.translate(0, 2)
        path = QtGui.QPainterPath()
        path.addRoundedRect(r, 12, 12)
        if self.ready:
            k = 0.5 + 0.5 * math.sin(self.phase * 2 * math.pi)     # 0..1 pulse
            top = QtGui.QColor.fromRgbF(1.0, 0.25 + 0.2 * k, 0.25 + 0.2 * k)
            bot = QtGui.QColor.fromRgbF(0.55 + 0.35 * k, 0.0, 0.0)
            glow = QtGui.QColor(255, 60, 60, int(60 + 120 * k))
            p.setPen(QtGui.QPen(glow, 5))
            p.drawPath(path)
            text_col = QtGui.QColor("white")
            sub = "confirm"
        else:
            top, bot = QtGui.QColor("#5a5f68"), QtGui.QColor("#35393f")
            text_col = QtGui.QColor("#9aa0a8")
            sub = "nothing to confirm"
        g = QtGui.QLinearGradient(0, r.top(), 0, r.bottom())
        g.setColorAt(0, top)
        g.setColorAt(1, bot)
        p.fillPath(path, g)
        # key-cap bevel
        p.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 120), 2))
        p.drawPath(path)
        p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 60), 1))
        p.drawRoundedRect(r.adjusted(4, 3, -4, -r.height() * 0.5), 8, 8)

        f = self.font()
        f.setBold(True)
        f.setPixelSize(19)
        p.setFont(f)
        p.setPen(text_col)
        main = QtCore.QRectF(r.left(), r.top() + 4, r.width(), r.height() * 0.62)
        p.drawText(main, QtCore.Qt.AlignCenter, "⏎  ENTER")
        f.setPixelSize(10)
        f.setBold(False)
        p.setFont(f)
        cap = QtCore.QRectF(r.left(), r.top() + r.height() * 0.64, r.width(), r.height() * 0.3)
        p.drawText(cap, QtCore.Qt.AlignCenter, sub)
        p.end()


class PlaneChips(QtWidgets.QWidget):
    """TOP / FRONT / SIDE buttons shown while picking a sketch plane."""

    CHIPS = (("XY", "TOP", "#2f6bff"), ("XZ", "FRONT", "#1fae3c"), ("YZ", "SIDE", "#e0343c"))

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        for key, label, col in self.CHIPS:
            b = QtWidgets.QPushButton("{}\n{}".format(label, key))
            b.setCursor(QtCore.Qt.PointingHandCursor)
            b.setFixedSize(76, 62)
            b.setStyleSheet(
                "QPushButton{{color:white;font-weight:bold;font-size:14px;border-radius:12px;"
                "border:3px solid rgba(0,0,0,90);background:{c};}}"
                "QPushButton:hover{{border-color:white;}}".format(c=col))
            b.setToolTip("Sketch on the {} plane ({})".format(key, label.lower()))
            b.clicked.connect(lambda _=False, k=key: pick_plane(k))
            lay.addWidget(b)


class Deck(Panel.Plate):
    """The control deck: a screwed-on brushed-aluminium plate with recessed modules."""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(26, 5, 26, 6)      # room for the screws
        lay.setSpacing(10)

        # ── MODE: the big red button + the green ACTIVE badge
        self.m_mode = Panel.Module("Mode")
        self.b_big = QtWidgets.QPushButton()
        self.b_big.setStyleSheet(BIG_RED_CSS)
        self.b_big.setCursor(QtCore.Qt.PointingHandCursor)
        self.b_big.setMinimumHeight(48)
        self.b_big.clicked.connect(toggle_mode)
        self.m_mode.row.addWidget(CautionTape(self.b_big))
        self.pill = BubbleBadge()
        self.m_mode.row.addWidget(self.pill, 0, QtCore.Qt.AlignVCenter)
        lay.addWidget(self.m_mode)

        # ── CONFIRM: pulsing ENTER (or TOP / FRONT / SIDE while picking a plane)
        self.m_act = Panel.Module("Confirm")
        self.chips = PlaneChips()
        self.chips.hide()
        self.m_act.row.addWidget(self.chips, 0, QtCore.Qt.AlignVCenter)
        self.b_enter = EnterButton()
        self.b_enter.setToolTip("Confirm the open tool (Pad, Pocket, Fillet...). "
                                "Pulses red when it's ready. Same as pressing Enter.")
        self.b_enter.clicked.connect(lambda: (confirm_task(),
                                              QtCore.QTimer.singleShot(150, refresh)))
        self.m_act.row.addWidget(self.b_enter, 0, QtCore.Qt.AlignVCenter)
        lay.addWidget(self.m_act)

        # ── VIEW: look straight at the selected face
        self.m_view = Panel.Module("View")
        self.b_snap = CrosshairButton("SNAP TO FACE")
        self.b_snap.setToolTip("Look straight at the selected face (or the sketch you're "
                               "in) and zoom to it")
        self.b_snap.clicked.connect(snap_to_face)
        self.m_view.row.addWidget(self.b_snap, 0, QtCore.Qt.AlignVCenter)
        lay.addWidget(self.m_view)

        lay.addStretch(1)

        # ── SYSTEM: phosphor nav readout + machined keys with LEDs
        self.m_sys = Panel.Module("System")
        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(7)
        grid.setVerticalSpacing(6)

        self.b_nav = Panel.Phosphor()               # click = next navigation style
        self.b_nav.clicked.connect(cycle_nav)

        more = Panel.Key("More tools")
        more.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.menu = QtWidgets.QMenu(more)
        self.menu.aboutToShow.connect(self._fill_menu)
        more.setMenu(self.menu)
        more.setToolTip("Every Part Design / Sketcher tool, looks, navigation and settings")

        self.b_lum = Panel.Key("Luminous", led="g")
        self.b_lum.setToolTip("High-contrast luminous 3D view on/off "
                              "(restyles solids in open files)")
        self.b_lum.clicked.connect(toggle_luminous)

        self.b_nuke = Panel.Key("Declutter", led="a")
        self.b_nuke.setToolTip("Hide ALL remaining clutter (toolbars, panels, status bar). "
                               "Press again to bring it back.")
        self.b_nuke.clicked.connect(nuke)

        for w, row, col in ((self.b_nav, 0, 0), (more, 0, 1),
                            (self.b_lum, 1, 0), (self.b_nuke, 1, 1)):
            w.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            grid.addWidget(w, row, col)
        self.m_sys.row.addLayout(grid)
        lay.addWidget(self.m_sys)

        self.set_nuked(False)
        self.set_theme(S.theme)
        self.set_nav(S.nav)
        self._mode = None
        self.set_mode("solid")

    def set_nav(self, name):
        preset = next((p for p in NAV_PRESETS if p[0] == name), None)
        if preset is None:
            self.b_nav.setText("Nav: FreeCAD")
            self.b_nav.led = "a"
            self.b_nav.setToolTip("Navigation style. Click to cycle: "
                                  + " → ".join(p[0] for p in NAV_PRESETS))
        else:
            self.b_nav.setText("Nav: " + name)
            self.b_nav.led = "g"
            self.b_nav.setToolTip(preset[2] + "\n\nClick for the next style.")
        self.b_nav.updateGeometry()
        self.b_nav.update()

    def set_theme(self, name):
        self.b_lum.set_lit(name == "luminous")

    def set_mode(self, mode):
        if mode == self._mode:
            return
        self._mode = mode
        key = " ({})".format(TOGGLE_SHORTCUT) if TOGGLE_SHORTCUT else ""
        if mode == "sketch":
            self.b_big.setText("✔  FINISH SKETCH")
            self.b_big.setToolTip("Close the sketch and go back to solid tools, with the "
                                  "sketch selected ready to extrude" + key)
        elif mode == "task":
            self.b_big.setText("✔  OK – FINISH STEP")
            self.b_big.setToolTip("Press OK on the open tool (Pad, Fillet, plane picker...)"
                                  + key)
        elif mode == "pick":
            self.b_big.setText("✖  CANCEL")
            self.b_big.setToolTip("Stop picking a plane")
        else:
            self.b_big.setText("✏  SKETCH")
            self.b_big.setToolTip("Start a sketch: on the selected face, edit the selected "
                                  "sketch, or pick a plane" + key)
        self.pill.set_mode(mode)
        self.chips.setVisible(mode == "pick")
        self.b_enter.setVisible(mode != "pick")
        self.m_act.set_label("Pick a plane" if mode == "pick" else "Confirm")

    def set_nuked(self, nuked):
        self.b_nuke.set_lit(nuked)

    def _fill_menu(self):
        m = self.menu
        m.clear()
        for title, cmds in (("Part Design", PD_ALL), ("Sketcher", SK_ALL)):
            sub = m.addMenu(title)
            for c in available(cmds):
                if c == "Separator":
                    sub.addSeparator()
                else:
                    _add_cmd(sub, c)
        m.addSeparator()
        ae = m.addAction("Auto-extrude after finishing a sketch", toggle_auto_extrude)
        ae.setCheckable(True)
        ae.setChecked(AUTO_EXTRUDE)
        look = m.addMenu("🎨 Look")
        for name, t in THEMES.items():
            a = look.addAction(t["label"] + " theme", lambda _=False, n=name: apply_theme(n))
            a.setCheckable(True)
            a.setChecked(S.theme == name)
        look.addAction("Restore original FreeCAD viewport", restore_viewport_theme)
        look.addSeparator()
        rb = look.addAction("🌈 Rainbow see-through faces", toggle_rainbow)
        rb.setCheckable(True)
        rb.setChecked(_rainbow_on())
        look.addAction("Restyle all solids in this document", restyle_all)
        sw = look.addAction("🌀 Rainbow swirl on selected faces", toggle_swirl)
        sw.setCheckable(True)
        sw.setChecked(_swirl_on())
        an = look.addAction("   ↳ animate it (off = static, lighter on old PCs)",
                            toggle_swirl_animation)
        an.setCheckable(True)
        an.setChecked(App.ParamGet(SC_PARAMS).GetBool("AnimateSwirl", True))
        g = look.addAction("Ghost solids while sketching", toggle_ghost)
        g.setCheckable(True)
        g.setChecked(GHOST_WHILE_SKETCHING)
        m.addSeparator()
        nav = m.addMenu("🧭 Navigation")
        for name, _, tip in NAV_PRESETS:
            a = nav.addAction(name, lambda _=False, n=name: apply_nav(n))
            a.setCheckable(True)
            a.setChecked(S.nav == name)
            a.setToolTip(tip)
        nav.addSeparator()
        for key, label in (("InvertPan", "Trackpad: reverse pan direction"),
                           ("InvertOrbit", "Trackpad: reverse orbit direction")):
            a = nav.addAction(label, lambda _=False, k=key: _toggle_param(k))
            a.setCheckable(True)
            a.setChecked(App.ParamGet(SC_PARAMS).GetBool(key, False))
        nav.addSeparator()
        nav.addAction("Restore original FreeCAD navigation", restore_nav)
        m.addAction("Tab all panels on the left", lambda: tab_panels(force=True))
        m.addSeparator()
        st = m.addAction("Start FreeCAD in SimpleCAD", toggle_start_in_simplecad)
        st.setCheckable(True)
        st.setChecked(_start_in_simplecad())
        m.addAction("Show all hidden toolbars", show_everything)
        m.addAction("Switch to full Part Design workbench", full_partdesign)
        m.addSeparator()
        m.addAction("About SimpleCAD", about)


def _add_cmd(menu, name):
    try:
        acts = Gui.Command.get(name).getAction()
        if acts:
            menu.addAction(acts[0])  # FreeCAD's own action: icon, shortcut, enabled state
            return
    except Exception:
        pass
    a = menu.addAction(name.split("_", 1)[-1])
    a.triggered.connect(lambda _=False, n=name: Gui.runCommand(n))


# ──────────────────────────── lifecycle ────────────────────────────

def _style_mode_toolbars():
    for name in (SOLID_TB, SKETCH_TB):
        tb = _toolbar(name)
        if tb:
            tb.setIconSize(QtCore.QSize(ICON_SIZE, ICON_SIZE))
            if TEXT_UNDER_ICONS:
                tb.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            if ALU_TOOLBARS and not tb.property("simplecad_alu"):
                tb.setStyleSheet(Panel.toolbar_css())   # brushed plate + machined keys
                tb.setProperty("simplecad_alu", True)


def refresh():
    if S.deck is None:
        return
    try:
        sk = in_sketch()
        if S.picking and (sk or _task_open()):
            end_pick()                      # something else took over
        mode = current_mode()
        S.deck.set_mode(mode)
        S.deck.b_enter.set_ready(mode == "task" and _ok_ready())
        tab_panels()
        _follow_tasks()
        attach_trackpad()
        if AUTO_STYLE:
            _auto_style()
        if sk != S.last_mode:
            first = S.last_mode is None
            S.last_mode = sk
            if GHOST_WHILE_SKETCHING and not (first and not sk):
                ghost(sk)
            a, b = _toolbar(SKETCH_TB), _toolbar(SOLID_TB)
            if a:
                a.setVisible(sk)
            if b:
                b.setVisible(not sk)
            _style_mode_toolbars()
            declutter()
    except Exception as e:
        _log(e)


def activate():
    startup()
    m = _mw()
    if S.deck_tb is None:
        load_saved_theme()
        tb = QtWidgets.QToolBar(DECK_TB, m)
        tb.setObjectName(DECK_TB)
        tb.setStyleSheet(Panel.toolbar_css() + "QToolBar{padding:0;spacing:0;}")
        S.deck = Deck()
        S.deck.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        tb.addWidget(S.deck)
        m.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        m.addToolBar(QtCore.Qt.TopToolBarArea, tb)
        S.deck_tb = tb
    S.deck_tb.show()
    if TOGGLE_SHORTCUT and S.shortcut is None:
        Shortcut = getattr(QtWidgets, "QShortcut", None) or QtGui.QShortcut  # Qt5 / Qt6
        S.shortcut = Shortcut(QtGui.QKeySequence(TOGGLE_SHORTCUT), m)
        S.shortcut.setContext(QtCore.Qt.ApplicationShortcut)
        S.shortcut.activated.connect(toggle_mode)
    if S.shortcut:
        S.shortcut.setEnabled(True)
    S.last_mode = None
    S.active = True
    S.sticky = True
    S.torn_down = False
    _watch_recomputes()
    _watch_selection()
    attach_trackpad()
    if S.watch is None:
        S.watch = QtCore.QTimer()
        S.watch.timeout.connect(_watch)
        S.watch.start(150)          # keeps running while other workbenches are active
    if S.timer is None:
        S.timer = QtCore.QTimer()
        S.timer.timeout.connect(refresh)
    S.timer.start(400)
    # let FreeCAD finish laying out the workbench before we tidy up
    QtCore.QTimer.singleShot(200, refresh)


def deactivate():
    """FreeCAD switched away from SimpleCAD.

    Often that's FreeCAD's own automatic switch when a sketch or a Pad/Pocket
    dialog opens, and _watch hops straight back. So nothing is torn down here;
    _finish_deactivate does that only once it's clear you really left.
    """
    import time
    S.active = False
    S.left_at = time.time()
    QtCore.QTimer.singleShot(60, _watch)      # bounce back fast if it's an edit switch


def _finish_deactivate(force=False):
    if S.active or S.torn_down:
        return
    S.torn_down = True
    if S.picking:
        end_pick()
    if S.swirl:
        S.swirl.clear()
    if S.timer:
        S.timer.stop()
    ghost(False)
    if S.nuked:
        nuke()
    restore_toolbars()
    if S.deck_tb:
        S.deck_tb.hide()
    if S.shortcut:
        S.shortcut.setEnabled(False)
