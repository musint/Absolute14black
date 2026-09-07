"""Generate a practice plan page for the Absolute 14 Black site.

Usage: python build/build_plan.py
Reads build/drills-<DATE>.json (exported from the coaching sheet's Drill Library)
and writes workouts/<DATE>.html. Public page: no player names, no contact details.
"""
from __future__ import annotations

import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------
# Schedule for this workout. Edit this block for a new session.
# ----------------------------------------------------------------------------
DATE = "2026-09-07"
TITLE = "Monday, September 7"
EYEBROW = "Small group workout"
TIME = "10am to 12pm"
PLACE = "Absolute Volleyball Club, San Rafael"
MAPS = "https://maps.google.com/?q=2145+Francisco+Blvd+E,+San+Rafael,+CA+94901"
FACTS = [
    ("Who", "Invited players preparing for 14s tryouts. Free and optional."),
    ("Coaches", "Christen Hamilton and Song Mu"),
    ("Bring", "Water, knee pads, court shoes. Please arrive 10 minutes early."),
    ("Focus", "A ball control block, then the hitting progression, then a cross-court game to finish."),
]
OPENER = ("10:00", "Check in, roll call, dynamic warmup", 5)
CLOSER = ("11:55", "Wrap up", 5)
TOTAL_MIN = 120

# (block label, [(clock, drill id, minutes, session note)])
BLOCKS = [
    ("Warmup", [
        ("10:05", "OS-10", 15,
         "Warmup game. 10 players in two groups of five: each group fields 3v3 with two waiting, and we use the "
         "exchange version (all three rotate off each time the ball crosses) so the two waiting come in every rally. "
         "Setters and middles start in middle back, pins in left back and right back. Two touches only, no tips, "
         "free ball to the winning side, games to 15 or cap at time. Talk every ball: mine, name the attacker, cover."),
    ]),
    ("Ball control", [
        ("10:20", "BC-01", 12,
         "Five pairs. Beginner series (toss and play) for about 4 minutes to groove arm shape, then advanced "
         "(both play) for the rest. If short on time skip skaters, keep V-touches. Watch: flat inside forearm, "
         "arm never bends, see the contact, pass with the legs, balance both feet before every contact."),
        ("10:32", "BC-07", 10,
         "Trios between the 10 ft line and the net, tossers on the net side. Three trios plus one extra who joins as "
         "a second tosser and rotates in. One ball first: 30 seconds tilting left, 30 seconds tilting right, rotate the "
         "passer. Add two-ball only for trios that are clean. Key: drop the inside shoulder to tilt, quiet platform, "
         "aim past the target's outside hand."),
        ("10:42", "BC-09", 10,
         "Same trios. One tosser at the 10 ft line, one at the end line, each with a ball. 60 seconds continuous per "
         "middle player, rotate so everyone goes twice. Key: beat the ball back, get set and balanced before contact, "
         "hands away from the hips between balls, pass to the forehead. Quicken the cadence only for players who reset cleanly."),
        ("10:52", "BC-12", 13,
         "Stations as one group. Coach Christen enters the ball, Coach Song at the T watching cover. Start with the back "
         "slots (LB, MB, RB) at 45 seconds each, add LF, MF, RF if reads are clean. Mix platform and hand reps. Key: run "
         "hard to the dot and arrive at a target, finish in cover every rep (outside foot on the line, belly to target), "
         "call mine. Water break after."),
    ]),
    ("Hitting", [
        ("11:05", "AT-01", 35,
         "Mostly pins, so run stages 1 to 9 in order. Footwork stations: outside and right side lines, middle station "
         "for the middles. Wall rotation, kneeling snap, self toss topspin, jump and chuck: about 3 minutes each. "
         "Partners across the net: 5 minutes. Coach toss stages 7 to 9: one group of five with Coach Christen, the other "
         "with Coach Song, 4 hits per variation so lines stay short. Smooth over power the whole way, listen for the "
         "splat, bicep to the ear, wait for the peak then go on the last two steps."),
    ]),
    ("Game", [
        ("11:40", "TP-12", 15,
         "Closing game, 5v5, group against group. Three back-row defenders plus a setter in each back row, one blocker "
         "at left front, no middle. Coach free ball entry, left front hits cross-court, the other side digs, sets, and "
         "counters cross. Make-it-take-it, 3-point games, best of three, then mirror as right v right if time. Keep "
         "swings controlled and soften the entry if pace runs high."),
    ]),
]

# ----------------------------------------------------------------------------

def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def pre(s: str) -> str:
    """Escape text and keep its line breaks (rendered with white-space: pre-line)."""
    return esc(s.strip())


def load_drills() -> dict:
    path = os.path.join(ROOT, "build", f"drills-{DATE}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def mins(n: int) -> str:
    return f'<span class="mins">{n}<small>min</small></span>'


def render_marker(clock: str, label: str, n: int) -> str:
    return (f'<div class="marker"><span class="clock">{esc(clock)}</span>'
            f'<span>{esc(label)}</span>{mins(n)}<span></span></div>')


def render_drill(clock: str, d: dict, n: int, note: str) -> str:
    tags = " &middot; ".join(esc(t) for t in (d.get("format"), d.get("focus"), d.get("setup")) if t)
    parts = [f'<div class="note"><h4>Today</h4><p>{esc(note)}</p></div>']
    if d.get("how"):
        parts.append(f'<div><h4>How to run</h4><p class="pre">{pre(d["how"])}</p></div>')
    if d.get("variations"):
        parts.append(f'<div><h4>Scaling and variations</h4><p class="pre">{pre(d["variations"])}</p></div>')
    if d.get("keys"):
        parts.append(f'<div><h4>Coaching keys</h4><p class="pre">{pre(d["keys"])}</p></div>')
    if d.get("source"):
        parts.append(f'<p class="src">Source: {esc(d["source"])}</p>')
    body = "\n".join(parts)
    return (
        f'<details class="drill" id="{esc(d["id"]).lower()}">\n'
        f'  <summary>\n'
        f'    <span class="clock">{esc(clock)}</span>\n'
        f'    <span class="dname">{esc(d["name"])}<span class="tags">{esc(d["id"])} &middot; {tags}</span></span>\n'
        f'    {mins(n)}\n'
        f'  </summary>\n'
        f'  <div class="dbody">\n{body}\n  </div>\n'
        f'</details>'
    )


def render_page(plan_html: str, facts_html: str) -> str:
    title = esc(TITLE)
    favicon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
               "%3Crect width='64' height='64' fill='%230a0a0b'/%3E"
               "%3Ctext x='32' y='47' font-family='Arial Narrow,Arial,sans-serif' font-weight='900' "
               "font-size='40' fill='white' text-anchor='middle'%3E14%3C/text%3E%3C/svg%3E")
    fonts = ("https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,400;0,700;1,400"
             "&family=Big+Shoulders+Display:wght@700;900&display=swap")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} workout · Absolute 14 Black</title>
<meta name="description" content="Practice plan for the Absolute 14 Black small group workout on {title}, {esc(TIME)}, {esc(PLACE)}.">
<meta name="theme-color" content="#0a0a0b">
<meta property="og:title" content="{title} workout · Absolute 14 Black">
<meta property="og:description" content="Practice plan: {esc(TIME)} at {esc(PLACE)}.">
<meta property="og:type" content="article">
<link rel="icon" href="{favicon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>

<header class="mast small">
  <div class="wrap">
    <a class="back" href="../">&larr; Absolute 14 Black</a>
    <p class="jersey" aria-label="14 Black"><span class="num">14</span><span class="team">Black</span></p>
    <p class="eyebrow">{esc(EYEBROW)}</p>
    <h1 class="title">{title}</h1>
    <p class="season"><b>{esc(TIME)}</b> &middot; {esc(PLACE)}</p>
  </div>
</header>

<main class="wrap">
  <dl class="facts">
{facts_html}
  </dl>

  <section class="plan" aria-labelledby="plan-h">
    <h2 id="plan-h">The plan</h2>
    <p class="hint">Tap a drill to open how we run it and what we are coaching.</p>
{plan_html}
  </section>
</main>

<footer>
  <div class="wrap">
    <span>Absolute Volleyball Club &middot; <a href="{MAPS}">2145 Francisco Blvd E, San Rafael, CA 94901</a></span>
    <span><a href="../">Absolute 14 Black</a> &middot; 2026 to 2027</span>
  </div>
</footer>

</body>
</html>
"""


def build() -> str:
    drills = load_drills()
    out = [render_marker(*OPENER)]
    planned = OPENER[2] + CLOSER[2]
    for label, items in BLOCKS:
        block_min = sum(n for _, _, n, _ in items)
        planned += block_min
        rows = "\n".join(render_drill(c, drills[i], n, note) for c, i, n, note in items)
        out.append(f'<div class="block"><h3><span>{esc(label)}</span><span class="sum">{block_min} min</span></h3>\n{rows}\n</div>')
    out.append(render_marker(*CLOSER))
    out.append(f'<div class="total"><span>Total</span><span>{planned} min</span></div>')
    if planned != TOTAL_MIN:
        raise SystemExit(f"Plan totals {planned} min but the session is {TOTAL_MIN} min. Fix the schedule.")

    facts = "\n".join(f"    <dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in FACTS)
    return render_page("\n".join(out), facts)


if __name__ == "__main__":
    page = build()
    dest = os.path.join(ROOT, "workouts", f"{DATE}.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print(f"wrote {os.path.relpath(dest, ROOT)} ({len(page.encode('utf-8'))} bytes)")
