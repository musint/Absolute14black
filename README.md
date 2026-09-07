# Absolute 14 Black

Team site for Absolute Volleyball Club 14 Black, 2026 to 2027 season.
Published with GitHub Pages at https://musint.github.io/Absolute14black/

## Layout

- `index.html` : home page (coaches, small group workouts)
- `workouts/YYYY-MM-DD.html` : one practice plan page per workout
- `assets/style.css` : shared styles
- `build/build_plan.py` : generates a workout page from a drill JSON export and a schedule
- `build/drills-YYYY-MM-DD.json` : the drill write-ups used by that workout (exported from the coaching sheet's Drill Library tab)

## Adding a workout

1. Export the drills you need from the Drill Library tab to `build/drills-YYYY-MM-DD.json`
   (keys: id, name, format, entry, focus, setup, how, variations, keys, source).
2. Copy the schedule block at the top of `build/build_plan.py`, edit date, blocks, and notes.
3. Run `python build/build_plan.py` and commit the generated page.
4. Add a session card to `index.html` under Small Group Workouts.

No player names or family contact details go on these pages. They are public.
