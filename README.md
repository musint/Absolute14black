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
- `build/build_plan.py` : the workout content (facts, drill write-ups, section order) and the generator
- `build/protect.py` : encrypts everything under `build/src/` into the shells
- `build/.password` : the team password, one line (NOT committed)
- `build/salt.txt` : key derivation salt, created once (committed, not secret)
- `robots.txt` and a `noindex` meta on every shell keep search engines out

## Adding or editing a workout

1. In `build/build_plan.py`, set the date and facts, add or edit drills in `DRILLS`
   (name, setup, `how` steps, `keys`), and set the section order in `PLAN`.
   For a second workout, copy the file to `build/build_plan_YYYY-MM-DD.py`.
2. Add or update the session card in `build/src/index.html` under Small Group Workouts.
3. Run `python build/build_plan.py` then `python build/protect.py`.
4. Commit the generated shells and push (see below).

Style notes for drill write-ups: short steps, no timings, no scaling or variations
section, no sources. Coaching keys stay to a handful of lines.

## Changing the password

Edit `build/.password`, run `python build/protect.py`, commit, push. Everyone will need
the new password; devices that remembered the old one get the form again.

## Publishing

The repo belongs to the `musint` GitHub account. With the GitHub CLI:
`gh auth switch -u musint`, `git push origin main`, then switch back. Pages rebuilds
in about a minute.

## What the gate is and is not

It keeps casual visitors and search engines out and keeps the page content out of the
public repo and page source. It is not strong security: the password is short and
anyone who has it can share it. Never put player names, family contacts, or coach
phone numbers on the site, even behind the gate.

Requires Python 3 with the `cryptography` package for the build step.
