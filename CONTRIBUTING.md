# Contributing

Bug reports and pull requests are welcome. By contributing you agree your contribution is licensed under the same [PolyForm Noncommercial 1.0.0](LICENSE.md) licence as the project.

- **Bugs:** use the issue template (FreeCAD version from Help → About, OS, steps, Report view output).
- **Code:** logic in `SimpleCADDeck.py`, camera maths in `SimpleCADTouch.py`, overlay in `SimpleCADSwirl.py`, styling in `SimpleCADPanel.py`. Keep it working on FreeCAD 0.21 and 1.x and on PySide2 and PySide6. FreeCAD `exec()`s `InitGui.py` with separate globals, so import inside methods.
- **Test:** close FreeCAD, copy the folder into `Mod`, restart.
