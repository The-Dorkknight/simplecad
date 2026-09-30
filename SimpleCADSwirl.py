# SimpleCAD - animated rainbow swirl drawn over the selected face(s)
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Required Notice: Copyright Matthew Armstrong (https://github.com/The-Dorkknight)
# Licensed under the PolyForm Noncommercial License 1.0.0. No warranty.
#
# The face is tessellated once and drawn as a thin, unpickable Coin overlay with
# one colour per vertex. A timer rotates the hues so the colours spiral around
# the face centre. Only the colour list is updated per frame, so it stays cheap.

import colorsys
import math

MAX_FACES = 6
MAX_VERTS = 3000          # bigger than this: draw it, but don't animate
FPS = 10                  # every frame redraws the whole 3D view, so keep it low
# Watchdog: if frames arrive this many times slower than planned (the PC is
# busy redrawing), freeze the swirl for this session. It stays on screen.
SLOW_FACTOR = 2.5


# ───────────────────────── pure maths (testable) ─────────────────────────

def plane_coords(points, normal):
    """Project 3D points onto the face plane -> (u, v) relative to their centre."""
    nx, ny, nz = normal
    n = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    nx, ny, nz = nx / n, ny / n, nz / n
    ax = (0.0, 0.0, 1.0) if abs(nz) < 0.9 else (0.0, 1.0, 0.0)
    # e1 = ax x n, e2 = n x e1
    e1 = (ax[1] * nz - ax[2] * ny, ax[2] * nx - ax[0] * nz, ax[0] * ny - ax[1] * nx)
    l1 = math.sqrt(sum(c * c for c in e1)) or 1.0
    e1 = tuple(c / l1 for c in e1)
    e2 = (ny * e1[2] - nz * e1[1], nz * e1[0] - nx * e1[2], nx * e1[1] - ny * e1[0])
    cnt = len(points) or 1
    cx = sum(p[0] for p in points) / cnt
    cy = sum(p[1] for p in points) / cnt
    cz = sum(p[2] for p in points) / cnt
    out = []
    for x, y, z in points:
        dx, dy, dz = x - cx, y - cy, z - cz
        out.append((dx * e1[0] + dy * e1[1] + dz * e1[2],
                    dx * e2[0] + dy * e2[1] + dz * e2[2]))
    return out


def refine(pts, tris, target_edge, budget=2400):
    """Split every triangle into 4 (shared midpoints, so no cracks) until the
    longest edge is under target_edge or the vertex budget would be exceeded.

    Big flat faces come out of FreeCAD's tessellation as a handful of huge
    triangles; colours are only set per vertex, so without this the swirl is
    smeared into a washed-out blend across the whole face.
    """
    import math as _m

    def longest(ps, ts):
        best = 0.0
        for a, b, c in ts:
            for i, j in ((a, b), (b, c), (c, a)):
                best = max(best, _m.dist(ps[i], ps[j]))
        return best

    pts, tris = list(pts), list(tris)
    while tris and longest(pts, tris) > target_edge:
        # each split adds about one new vertex per edge: ~1.5 per triangle
        if len(pts) + int(len(tris) * 1.5) + 1 > budget:
            break
        mid = {}

        def m(i, j):
            key = (i, j) if i < j else (j, i)
            if key not in mid:
                a, b = pts[i], pts[j]
                pts.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2))
                mid[key] = len(pts) - 1
            return mid[key]

        new = []
        for a, b, c in tris:
            ab, bc, ca = m(a, b), m(b, c), m(c, a)
            new += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
        tris = new
    return pts, tris


def polar(uv):
    """(angle 0..1, radius 0..1) for each (u, v)."""
    rmax = max((math.hypot(u, v) for u, v in uv), default=1.0) or 1.0
    return [((math.atan2(v, u) / (2 * math.pi)) % 1.0, math.hypot(u, v) / rmax)
            for u, v in uv]


def swirl_colours(pol, t, arms=1.0, twist=1.3, speed=0.35):
    """Rainbow spiral: hue follows angle + radius, drifting with time t (s)."""
    out = []
    for a, r in pol:
        h = (a * arms + r * twist - t * speed) % 1.0
        out.append(colorsys.hsv_to_rgb(h, 0.9, 1.0))
    return out


# ───────────────────────── swirl texture ─────────────────────────

TEX_SIZE = 256
SWIRL_ALPHA = 0.5         # 0 = invisible, 1 = solid paint
_tex_cache = {}


def swirl_texture(size=TEX_SIZE, alpha=SWIRL_ALPHA, twist=1.3):
    """RGBA bytes of a see-through rainbow spiral (centre of the image = centre
    of the face). Made once and cached: animation just rotates the image."""
    key = (size, round(alpha, 3), twist)
    if key in _tex_cache:
        return _tex_cache[key]
    a8 = int(max(0.0, min(1.0, alpha)) * 255)
    half = (size - 1) / 2.0
    out = bytearray(size * size * 4)
    i = 0
    for y in range(size):
        dy = (y - half) / half
        for x in range(size):
            dx = (x - half) / half
            r = math.hypot(dx, dy)
            h = ((math.atan2(dy, dx) / (2 * math.pi)) + r * twist) % 1.0
            cr, cg, cb = colorsys.hsv_to_rgb(h, 0.9, 1.0)
            out[i] = int(cr * 255)
            out[i + 1] = int(cg * 255)
            out[i + 2] = int(cb * 255)
            out[i + 3] = a8
            i += 4
    _tex_cache[key] = bytes(out)
    return _tex_cache[key]


def tex_coords(uv):
    """Face-plane (u, v) -> texture coords, face centre at (0.5, 0.5)."""
    rmax = max((math.hypot(u, v) for u, v in uv), default=1.0) or 1.0
    return [(u / (2 * rmax) + 0.5, v / (2 * rmax) + 0.5) for u, v in uv]


# ───────────────────────── Coin overlay ─────────────────────────

class Swirl:
    """Rainbow swirl over the selected faces.

    Drawn as a see-through texture (smooth per-pixel colour, real transparency,
    and animating it is just a rotation, so it costs almost nothing). If this
    FreeCAD can't take the texture, it falls back to per-vertex colours.
    """

    def __init__(self, get_view, qtcore, animate=lambda: True, on_slow=None,
                 alpha=lambda: SWIRL_ALPHA):
        self.get_view = get_view
        self.QtCore = qtcore
        self.animate = animate    # callable -> bool (user setting)
        self.on_slow = on_slow    # called once if the watchdog freezes it
        self.alpha = alpha        # callable -> 0..1
        self.nodes = []           # (root, sep, kind, handle, polar, n)
        self.t = 0.0
        self.timer = None
        self.too_slow = False
        self.last = None
        self.gaps = []

    # -- lifecycle --
    def clear(self):
        for root, sep, *_ in self.nodes:
            try:
                root.removeChild(sep)
            except Exception:
                pass
        self.nodes = []
        if self.timer is not None:
            self.timer.stop()

    def show(self, faces):
        """faces: list of Part.Face in global coordinates."""
        self.clear()
        view = self.get_view()
        if view is None or not faces:
            return
        try:
            from pivy import coin
            root = view.getSceneGraph()
        except Exception:
            return
        for face in faces[:MAX_FACES]:
            try:
                self._add(coin, root, face)
            except Exception:
                pass
        if self.nodes and self.animate() and not self.too_slow and all(
                kind == "tex" or n <= MAX_VERTS for _, _, kind, _, _, n in self.nodes):
            if self.timer is None:
                self.timer = self.QtCore.QTimer()
                self.timer.timeout.connect(self._tick)
            self.last, self.gaps = None, []
            self.timer.start(int(1000 / FPS))

    def _common(self, coin, pts, tris):
        sep = coin.SoSeparator()
        pick = coin.SoPickStyle()
        pick.style = coin.SoPickStyle.UNPICKABLE      # never steal clicks
        light = coin.SoLightModel()
        light.model = coin.SoLightModel.BASE_COLOR     # pure bright colours
        off = coin.SoPolygonOffset()                   # sit just on top of the face
        off.factor = -2.0
        off.units = -2.0
        coords = coin.SoCoordinate3()
        coords.point.setValues(0, len(pts), [list(p) for p in pts])
        idx = []
        for a, b, c in tris:
            idx += [a, b, c, -1]
        fs = coin.SoIndexedFaceSet()
        fs.coordIndex.setValues(0, len(idx), idx)
        return sep, (pick, light, off), (coords, fs)

    def _add(self, coin, root, face):
        bb = face.BoundBox
        tol = max(bb.DiagonalLength / 150.0, 1e-3)
        pts, tris = face.tessellate(tol)
        if not tris:
            return
        pts = [(p.x, p.y, p.z) for p in pts]
        u0, u1, v0, v1 = face.ParameterRange
        nrm = face.normalAt((u0 + u1) / 2, (v0 + v1) / 2)
        uv = plane_coords(pts, (nrm.x, nrm.y, nrm.z))
        try:
            self._add_textured(coin, root, pts, tris, uv)
        except Exception:
            self._add_vertex(coin, root, pts, tris)

    def _add_textured(self, coin, root, pts, tris, uv):
        sep, head, tail = self._common(coin, pts, tris)
        cplx = coin.SoComplexity()
        cplx.textureQuality = 1.0                      # smooth filtering, no blocky pixels
        tex = coin.SoTexture2()
        tex.image.setValue(coin.SbVec2s(TEX_SIZE, TEX_SIZE), 4, swirl_texture(alpha=self.alpha()))
        tex.model = coin.SoTexture2.MODULATE
        tex.wrapS = coin.SoTexture2.CLAMP
        tex.wrapT = coin.SoTexture2.CLAMP
        xf = coin.SoTexture2Transform()
        xf.center.setValue(0.5, 0.5)
        xf.rotation = self._angle()
        mat = coin.SoMaterial()
        mat.diffuseColor.setValue(1.0, 1.0, 1.0)       # texture colours unchanged
        tc = coin.SoTextureCoordinate2()
        tcs = tex_coords(uv)
        tc.point.setValues(0, len(tcs), [list(c) for c in tcs])
        for node in head + (cplx, mat, tex, xf, tc) + tail:
            sep.addChild(node)
        root.addChild(sep)
        self.nodes.append((root, sep, "tex", xf, None, len(pts)))

    def _add_vertex(self, coin, root, pts, tris):
        """Fallback: colours per vertex on a refined mesh."""
        pts, tris = refine(pts, tris, max(max(p[i] for p in pts) - min(p[i] for p in pts)
                                          for i in range(3)) / 20.0)
        sep, head, tail = self._common(coin, pts, tris)
        nrm_uv = polar(plane_coords(pts, (0, 0, 1)))
        bind = coin.SoMaterialBinding()
        bind.value = coin.SoMaterialBinding.PER_VERTEX_INDEXED
        mat = coin.SoMaterial()
        n = len(pts)
        mat.diffuseColor.setValues(0, n, [list(c) for c in swirl_colours(nrm_uv, self.t)])
        mat.transparency.setValue(1.0 - self.alpha())
        for node in head + (bind, mat) + tail:
            sep.addChild(node)
        root.addChild(sep)
        self.nodes.append((root, sep, "vtx", mat, nrm_uv, n))

    def _angle(self):
        return -2 * math.pi * 0.35 * self.t            # same speed as before

    def _tick(self):
        import time
        now = time.perf_counter()
        if self.last is not None:
            self.gaps.append(now - self.last)
            if len(self.gaps) >= 10:
                avg = sum(self.gaps) / len(self.gaps)
                self.gaps = []
                if avg > SLOW_FACTOR / FPS:
                    self.too_slow = True
                    self.timer.stop()
                    if self.on_slow:
                        self.on_slow()
                    return
        self.last = now
        self.t += 1.0 / FPS
        for _, _, kind, handle, pol, n in self.nodes:
            try:
                if kind == "tex":
                    handle.rotation = self._angle()    # one number per frame
                elif n <= MAX_VERTS:
                    handle.diffuseColor.setValues(0, n, [list(c) for c in swirl_colours(pol, self.t)])
            except Exception:
                pass
