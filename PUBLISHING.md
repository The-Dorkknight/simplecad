# Publishing SimpleCAD (account: **The-Dorkknight**)

Keep this file outside the repo. Never give anyone your GitHub password; `gh` logs in through your browser.

## 0. Commit email (do this first)
GitHub Settings → Emails → tick **Keep my email addresses private** and copy your no-reply address (`12345+The-Dorkknight@users.noreply.github.com`). The first commit uses a placeholder, so swap it in **before the first push**:
```bash
cd simplecad
git config user.email "12345+The-Dorkknight@users.noreply.github.com"
git commit --amend --reset-author --no-edit
git tag -fa v0.9.3 -m "SimpleCAD 0.9.3"
```
Also put that address in the `<maintainer email>` line of `package.xml` (amend the commit again if you change it).

## 1. Route A: browser
Create an empty **public** repo `simplecad` on github.com (no README/licence), then drag the folder contents in. Note: this route loses the git history and tag; Route B is better.

## 2. Route B: git + gh (recommended)
```bash
gh auth login
gh repo create simplecad --public --source . --push \
  --description "Fusion 360-style decluttered workbench for FreeCAD (source-available, non-commercial)"
git push origin v0.9.3
gh repo edit --add-topic freecad --add-topic freecad-workbench --add-topic addon
gh release create v0.9.3 --title "SimpleCAD 0.9.3" --notes-file CHANGELOG.md
```
Make sure **Issues** are enabled (Settings → Features). This is not marked pre-release because it isn't work-in-progress.

## 3. GitHub Pages
```bash
gh api -X POST repos/The-Dorkknight/simplecad/pages -f "source[branch]=main" -f "source[path]=/docs"
```
or Settings → Pages → Branch `main`, folder `/docs`. Site: https://The-Dorkknight.github.io/simplecad/

## 4. Screenshots
The images are renders from a simulated harness. Replace `docs/images/deck.webp` and `swirl.webp` with real FreeCAD screenshots (keep WebP for the grainy metal) when you can.

## 5. Addon Manager listing (optional)
Users can add the repo URL as a custom repository. To be listed by default, open an "Addon - Addition" issue at https://github.com/FreeCAD/FreeCAD-addons. Bump `version`/`date` in `package.xml` for each release. Because the repo is non-commercial, source-available and not OSI-approved, the FreeCAD maintainers may decline to list it.

GitHub will show the licence as "Other". This is not legal advice.
