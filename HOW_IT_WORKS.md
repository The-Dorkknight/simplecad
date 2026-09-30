# How SimpleCAD works

**What it reads:** which FreeCAD toolbars and panels exist, the current selection, the open document's bodies and sketches, and FreeCAD's own preferences.

**What it changes:** only how FreeCAD *looks and behaves in the window*: it hides toolbars and panels (never deleting them, and never remembering the hidden state so a restart restores everything), shows its own deck, re-colours faces in the 3D view, draws a rainbow overlay on the selected face, and optionally changes navigation style (your originals are backed up; **More tools → Restore**). A couple of preferences are stored under FreeCAD's user parameters (start workbench, navigation backup).

**What it never does:** edit your model data or files, use the network, send any data anywhere, or run anything outside FreeCAD.

## Architecture
- `InitGui.py` registers the workbench.
- `SimpleCADDeck.py` holds the logic and UI: the deck, mode detection (sketch / tool / pick / solid), declutter, looks, and bounce-back logic because FreeCAD 1.x switches to the Sketcher or Part Design workbench on its own; SimpleCAD hops back without resetting anything and gives up if FreeCAD keeps fighting it.
- `SimpleCADTouch.py` turns trackpad gestures into camera moves.
- `SimpleCADSwirl.py` draws the rainbow overlay as an unpickable Coin3D texture.
- `SimpleCADPanel.py` paints the brushed-aluminium widgets; `tools/make_brushed_alu.py` generates the grain tiles.

Not a medical device or safety tool. Keep backups of your work.
