# SimpleCAD workbench registration
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Required Notice: Copyright Matthew Armstrong (https://github.com/The-Dorkknight)
# Licensed under the PolyForm Noncommercial License 1.0.0. No warranty.
# Note: FreeCAD exec()s this file with separate globals/locals, so names
# imported at the top are NOT visible inside the class body or its methods.
# Everything the class needs is imported inside the methods, and the icon is
# attached after the class is defined.

import os
import FreeCADGui as Gui
import SimpleCADDeck


class SimpleCADWorkbench(Gui.Workbench):
    MenuText = "SimpleCAD"
    ToolTip = "Decluttered sketch-and-solid workbench, Fusion 360 style"

    def Initialize(self):
        import PartDesignGui  # noqa: F401  (registers Part Design commands)
        import SketcherGui    # noqa: F401  (registers Sketcher commands)
        import SimpleCADDeck as d

        self.appendToolbar(d.SOLID_TB, d.available(d.SOLID_CMDS))
        self.appendToolbar(d.SKETCH_TB, d.available(d.SKETCH_CMDS))
        # Classic menus too, so nothing is ever more than two clicks away
        self.appendMenu(["SimpleCAD", "Part Design"], d.available(d.PD_ALL))
        self.appendMenu(["SimpleCAD", "Sketcher"], d.available(d.SK_ALL))

    def Activated(self):
        import SimpleCADDeck
        SimpleCADDeck.activate()

    def Deactivated(self):
        import SimpleCADDeck
        SimpleCADDeck.deactivate()

    def GetClassName(self):
        return "Gui::PythonWorkbench"


SimpleCADWorkbench.Icon = os.path.join(SimpleCADDeck.ICON_DIR, "SimpleCAD.svg")
Gui.addWorkbench(SimpleCADWorkbench())

# Repair/guard FreeCAD's saved layout and hook "new document" as soon as the
# window is up, whichever workbench FreeCAD starts in.
try:
    from PySide import QtCore as _QtCore
    _QtCore.QTimer.singleShot(1500, SimpleCADDeck.startup)
except Exception:
    pass
