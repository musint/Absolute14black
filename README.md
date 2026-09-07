# Absolute 14 Black

Team site for Absolute Volleyball Club 14 Black, 2026 to 2027 season.
Published with GitHub Pages at https://musint.github.io/Absolute14black/

The site sits behind a team password. Every page is shipped as a shell (masthead
plus password form) with the real page encrypted inside it. The browser derives a
key from the password and decrypts in place, then remembers the unlock on that
device until "Sign out" is tapped.

## Layout

- `index.html`, `workouts/YYYY-MM-DD.html` : generated shells (committed)
- `assets/style.css`, `assets/gate.js` : shared styles and the unlock script
- `build/src/` : plaintext pages (NOT committed)
- `build/build_plan.py` : generates a workout page into `build/src/workouts/`
- `build/protect.py` : encrypts everything under `build/src/` into the shells
- `build/drills-YYYY-MM-DD.json` : drill write-ups from the coaching sheet (NOT committed)
- `build/.password` : the team password, one line (NOT committed)
- `build/salt.txt` : key derivation salt, created once (committed, not secret)
- `robots.txt` and a `noindex` meta on every shell keep search engines out

## Adding a workout

1. Export the drills you need from the Drill Library tab to `build/drills-YYYY-MM-DD.json`
   (keys: id, name, format, entry, focus, setup, how, variations, keys, source).
2. Copy the schedule block at the top of `build/build_plan.py`, edit date, blocks, and notes.
3. Add a session card to `build/src/index.html` under Small Group Workouts.
4. Run `python build/build_plan.py` then `python build/protect.py`.
5. Commit the generated shells and push.

## Changing the password

Edit `build/.password`, run `python build/protect.py`, commit, push. Everyone will need
the new password; devices that remembered the old one get the form again.

## What the gate is and is not

It keeps casual visitors and search engines out and keeps the page content out of the
public repo and page source. It is not strong security: the password is short and
anyone who has it can share it. Never put player names, family contacts, or coach
phone numbers on the site, even behind the gate.

Requires Python 3 with the `cryptography` package for the build step.
