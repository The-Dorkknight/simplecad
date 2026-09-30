# SimpleCAD - brushed-aluminium instrument-panel kit for Qt
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Required Notice: Copyright Matthew Armstrong (https://github.com/The-Dorkknight)
# Licensed under the PolyForm Noncommercial License 1.0.0. No warranty.
#
# A Qt port of the "brushed aluminium panel" web style: a brushed-metal plate
# with slotted screws, engraved labels, recessed modules, machined keys with
# indicator LEDs and a green phosphor readout. Pure QPainter + one grain tile,
# so it works offline and costs nothing at rest.

import os

try:
    from PySide import QtCore, QtGui, QtWidgets
except ImportError:  # pragma: no cover
    from PySide import QtCore, QtGui
    QtWidgets = QtGui

HERE = os.path.dirname(os.path.abspath(__file__))
GRAIN = os.path.join(HERE, "icons", "brushed_alu_grain.png")
TILE = os.path.join(HERE, "icons", "brushed_alu_tile.png")

INK = QtGui.QColor("#1d2126")
ENGRAVE = QtGui.QColor("#23272c")
HI = QtGui.QColor(255, 255, 255, 140)
LO = QtGui.QColor(0, 0, 0, 97)
PHOS = QtGui.QColor("#8dffb0")
PHOS_BG = QtGui.QColor("#08120c")
LED = {"g": ("#eaffef", "#46ff8a", "#139a45"),
       "a": ("#fff5dc", "#ffb020", "#b86b00"),
       "r": ("#ffe1de", "#ff3b30", "#a3150d")}

_grain = None


def grain():
    """The grain tile at half its pixel size (sharp on retina, as the skill says)."""
    global _grain
    if _grain is None:
        pm = QtGui.QPixmap(GRAIN)
        if not pm.isNull():
            pm.setDevicePixelRatio(2.0)
        _grain = pm
    return _grain


def mono(px, bold=True):
    f = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
    f.setPixelSize(px)
    f.setBold(bold)
    return f


def paint_alu(p, rect):
    """Brushed aluminium: warm sheen gradient + grain tile blended in Overlay mode."""
    p.save()
    r = QtCore.QRectF(rect)
    # 115deg sheen
    g = QtGui.QLinearGradient(r.topLeft(), QtCore.QPointF(r.right(), r.bottom() + r.width() * 0.47))
    for pos, c in ((0, "#6e7379"), (.24, "#979ca1"), (.46, "#bdbdb8"), (.64, "#a3a7ab"),
                   (.82, "#8a8f94"), (1, "#6c7177")):
        g.setColorAt(pos, QtGui.QColor(c))
    p.fillRect(r, g)
    rg = QtGui.QRadialGradient(QtCore.QPointF(r.left() + r.width() * .3, r.center().y()),
                               r.width() * .45)
    rg.setColorAt(0, QtGui.QColor(255, 252, 244, 128))
    rg.setColorAt(1, QtGui.QColor(255, 252, 244, 0))
    p.fillRect(r, rg)
    pm = grain()
    if not pm.isNull():
        p.setCompositionMode(QtGui.QPainter.CompositionMode_Overlay)
        p.drawTiledPixmap(r, pm)
    p.restore()


def paint_screw(p, cx, cy, angle=30, d=12.0):
    p.save()
    p.setRenderHint(QtGui.QPainter.Antialiasing)
    rad = d / 2
    p.setPen(QtGui.QPen(HI, 1))
    p.setBrush(QtCore.Qt.NoBrush)
    p.drawEllipse(QtCore.QPointF(cx, cy + 1), rad, rad)
    g = QtGui.QRadialGradient(QtCore.QPointF(cx - rad * .3, cy - rad * .4), d)
    g.setColorAt(0, QtGui.QColor("#fdfdfd"))
    g.setColorAt(.55, QtGui.QColor("#a3a9ae"))
    g.setColorAt(1, QtGui.QColor("#5f656b"))
    p.setBrush(g)
    p.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 90), 1))
    p.drawEllipse(QtCore.QPointF(cx, cy), rad, rad)
    p.translate(cx, cy)
    p.rotate(angle)
    p.setPen(QtCore.Qt.NoPen)
    p.setBrush(QtGui.QColor(255, 255, 255, 128))
    p.drawRoundedRect(QtCore.QRectF(-rad + 2, 0, d - 4, 2), 1, 1)
    p.setBrush(QtGui.QColor("#4b5157"))
    p.drawRoundedRect(QtCore.QRectF(-rad + 2, -1, d - 4, 2), 1, 1)
    p.restore()


def paint_led(p, cx, cy, colour, on, d=8.0):
    p.save()
    p.setRenderHint(QtGui.QPainter.Antialiasing)
    rad = d / 2
    if on:
        hi, mid, lo = (QtGui.QColor(c) for c in LED[colour])
        glow = QtGui.QRadialGradient(QtCore.QPointF(cx, cy), d * 1.3)
        gc = QtGui.QColor(mid)
        gc.setAlpha(150)
        glow.setColorAt(0, gc)
        gc.setAlpha(0)
        glow.setColorAt(1, gc)
        p.setPen(QtCore.Qt.NoPen)
        p.setBrush(glow)
        p.drawEllipse(QtCore.QPointF(cx, cy), d * 1.3, d * 1.3)
        g = QtGui.QRadialGradient(QtCore.QPointF(cx - rad * .2, cy - rad * .3), rad)
        g.setColorAt(0, hi)
        g.setColorAt(.5, mid)
        g.setColorAt(1, lo)
        p.setBrush(g)
    else:
        p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 150), 1))
        p.setBrush(QtCore.Qt.NoBrush)
        p.drawEllipse(QtCore.QPointF(cx, cy + .5), rad, rad)
        p.setPen(QtCore.Qt.NoPen)
        p.setBrush(QtGui.QColor("#3d2f2a"))
    p.drawEllipse(QtCore.QPointF(cx, cy), rad, rad)
    p.restore()


def draw_engraved(p, rect, text, px=9, align=QtCore.Qt.AlignCenter, spacing=2.2):
    f = mono(px)
    f.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, spacing)
    p.save()
    p.setFont(f)
    p.setPen(HI)
    p.drawText(QtCore.QRectF(rect).translated(0, 1), align, text.upper())
    p.setPen(QtGui.QColor(0, 0, 0, 46))
    p.drawText(QtCore.QRectF(rect).translated(0, -1), align, text.upper())
    p.setPen(ENGRAVE)
    p.drawText(QtCore.QRectF(rect), align, text.upper())
    p.restore()


# ───────────────────────────── widgets ─────────────────────────────

class Plate(QtWidgets.QWidget):
    """A brushed plate with a slotted screw at each end."""

    def paintEvent(self, ev):
        p = QtGui.QPainter(self)
        r = self.rect()
        paint_alu(p, r)
        p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 100), 1))
        p.drawLine(0, 0, r.width(), 0)
        p.setPen(QtGui.QPen(LO, 1))
        p.drawLine(0, r.height() - 1, r.width(), r.height() - 1)
        cy = r.height() / 2
        paint_screw(p, 10, cy, 30)
        paint_screw(p, r.width() - 10, cy, -50)
        p.end()


class Module(QtWidgets.QWidget):
    """Recessed module grouping controls under an engraved label."""

    LABEL_H = 11

    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.label = label
        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(8, 4 + self.LABEL_H + 3, 8, 6)
        outer.setSpacing(0)
        self.row = QtWidgets.QHBoxLayout()
        self.row.setContentsMargins(0, 0, 0, 0)
        self.row.setSpacing(7)
        outer.addLayout(self.row)

    def set_label(self, text):
        if text != self.label:
            self.label = text
            self.update()

    def paintEvent(self, ev):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        r = QtCore.QRectF(self.rect()).adjusted(.5, .5, -.5, -1.5)
        path = QtGui.QPainterPath()
        path.addRoundedRect(r, 9, 9)
        p.fillPath(path, QtGui.QColor(0, 0, 0, 15))
        # inner shadow along the top edge
        p.save()
        p.setClipPath(path)
        g = QtGui.QLinearGradient(0, r.top(), 0, r.top() + 6)
        g.setColorAt(0, QtGui.QColor(0, 0, 0, 70))
        g.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
        p.fillRect(QtCore.QRectF(r.left(), r.top(), r.width(), 6), g)
        p.restore()
        p.setPen(QtGui.QPen(HI, 1))
        p.drawRoundedRect(r.translated(0, 1), 9, 9)
        p.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 72), 1))
        p.drawPath(path)
        draw_engraved(p, QtCore.QRectF(0, 4, self.width(), self.LABEL_H), self.label)
        p.end()


class Key(QtWidgets.QToolButton):
    """Machined key; optional indicator LED ('g', 'a' or 'r' = blinking red)."""

    def __init__(self, text, led=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.led = led
        self.lit = False
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFont(mono(10))
        self._hover = False
        self._blink = None

    def set_lit(self, on):
        if on == self.lit:
            return
        self.lit = on
        if self.led == "r":
            if self._blink is None:
                self._blink = QtCore.QTimer(self)
                self._blink.timeout.connect(self.update)
            self._blink.start(500) if on else self._blink.stop()
        self.update()

    def sizeHint(self):
        fm = QtGui.QFontMetrics(self.font())
        w = fm.horizontalAdvance(self.text().upper()) + len(self.text()) + 24
        if self.led:
            w += 14
        if self.menu():
            w += 10
        return QtCore.QSize(w, 26)

    def minimumSizeHint(self):
        return self.sizeHint()

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
        down = self.isDown()
        r = QtCore.QRectF(self.rect()).adjusted(1, 1, -1, -3)
        if down:
            r.translate(0, 1)
        path = QtGui.QPainterPath()
        path.addRoundedRect(r, 6, 6)
        if not down:   # drop shadow
            p.fillPath(path.translated(0, 2), QtGui.QColor(0, 0, 0, 70))
        g = QtGui.QLinearGradient(0, r.top(), 0, r.bottom())
        stops = ((0, "#f7f8f9"), (.48, "#d4d8dc"), (.52, "#c3c8cd"), (1, "#b4bac0"))
        if down:
            stops = ((0, "#b4bac0"), (.5, "#c3c8cd"), (1, "#d4d8dc"))
        for pos, c in stops:
            col = QtGui.QColor(c)
            if self._hover and not down:
                col = col.lighter(104)
            g.setColorAt(pos, col)
        p.fillPath(path, g)
        p.setPen(QtGui.QPen(QtGui.QColor("#6f757c"), 1))
        p.drawPath(path)
        if not down:
            p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 230), 1))
            p.drawLine(QtCore.QPointF(r.left() + 5, r.top() + 1.5),
                       QtCore.QPointF(r.right() - 5, r.top() + 1.5))
        x0 = r.left() + 10
        if self.led:
            on = self.lit and not (self.led == "r" and (QtCore.QTime.currentTime().msec() // 500) % 2)
            paint_led(p, x0 + 3, r.center().y(), self.led, on, 7)
            x0 += 14
        f = self.font()
        f.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 1.0)
        p.setFont(f)
        tr = QtCore.QRectF(x0, r.top(), r.right() - x0 - (14 if self.menu() else 8), r.height())
        text = self.text().upper()
        col = INK if self.isEnabled() else QtGui.QColor("#6a6f75")
        p.setPen(QtGui.QColor(255, 255, 255, 190))
        p.drawText(tr.translated(0, 1), QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter, text)
        p.setPen(col)
        p.drawText(tr, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter, text)
        if self.menu():   # little engraved caret
            cx, cy = r.right() - 10, r.center().y()
            tri = QtGui.QPolygonF([QtCore.QPointF(cx - 3.5, cy - 1.5), QtCore.QPointF(cx + 3.5, cy - 1.5),
                                   QtCore.QPointF(cx, cy + 2.5)])
            p.setPen(QtCore.Qt.NoPen)
            p.setBrush(col)
            p.drawPolygon(tri)
        p.end()


class Phosphor(QtWidgets.QAbstractButton):
    """Green phosphor readout with scanlines; clickable (e.g. to cycle a setting)."""

    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setFont(mono(11))
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.led = "g"

    def sizeHint(self):
        fm = QtGui.QFontMetrics(self.font())
        return QtCore.QSize(max(150, fm.horizontalAdvance(self.text().upper()) +
                                len(self.text()) + 40), 26)

    def minimumSizeHint(self):
        return self.sizeHint()

    def paintEvent(self, ev):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        r = QtCore.QRectF(self.rect()).adjusted(.5, .5, -.5, -1.5)
        path = QtGui.QPainterPath()
        path.addRoundedRect(r, 6, 6)
        p.setPen(QtGui.QPen(HI, 1))
        p.drawRoundedRect(r.translated(0, 1), 6, 6)
        p.fillPath(path, PHOS_BG)
        p.save()
        p.setClipPath(path)
        p.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 90), 1))
        y = r.top() + 1
        while y < r.bottom():
            p.drawLine(QtCore.QPointF(r.left(), y), QtCore.QPointF(r.right(), y))
            y += 3
        g = QtGui.QLinearGradient(0, r.top(), 0, r.top() + 7)   # inset shadow
        g.setColorAt(0, QtGui.QColor(0, 0, 0, 220))
        g.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
        p.fillRect(QtCore.QRectF(r.left(), r.top(), r.width(), 7), g)
        p.restore()
        p.setPen(QtGui.QPen(QtGui.QColor("#16241a"), 1))
        p.drawPath(path)
        paint_led(p, r.left() + 11, r.center().y(), self.led, True, 7)
        f = self.font()
        f.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 1.0)
        p.setFont(f)
        tr = r.adjusted(22, 0, -8, 0)
        text = self.text().upper()
        glow = QtGui.QColor(90, 255, 150, 60)
        p.setPen(glow)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            p.drawText(tr.translated(dx, dy), QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)
        p.setPen(PHOS.lighter(110) if self.underMouse() else PHOS)
        p.drawText(tr, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)
        p.end()


def toolbar_css():
    """Stylesheet for FreeCAD toolbars: brushed tile + machined keys."""
    tile = TILE.replace("\\", "/")
    return """
QToolBar {{ background: #9ea3a7 url("{tile}"); border: 0; border-bottom: 1px solid rgba(0,0,0,90);
  spacing: 5px; padding: 4px 8px; }}
QToolBar::separator {{ width: 2px; margin: 6px 5px; background: rgba(0,0,0,70);
  border-right: 1px solid rgba(255,255,255,140); }}
QToolBar QToolButton {{ color: #1d2126; font-weight: bold; font-size: 10px;
  border: 1px solid #6f757c; border-radius: 6px; padding: 3px 5px; margin: 1px 0 3px 0;
  background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f7f8f9, stop:0.48 #d4d8dc,
    stop:0.52 #c3c8cd, stop:1 #b4bac0); }}
QToolBar QToolButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff,
    stop:0.48 #dfe2e5, stop:0.52 #cfd3d7, stop:1 #bfc4c9); }}
QToolBar QToolButton:pressed, QToolBar QToolButton:checked {{
  background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #aeb4ba, stop:1 #d4d8dc);
  padding-top: 4px; padding-bottom: 2px; }}
QToolBar QToolButton:disabled {{ color: #5f656b; }}
""".format(tile=tile)
