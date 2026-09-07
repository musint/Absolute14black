"""Generate a practice plan page for the Absolute 14 Black site.

Usage: python build/build_plan.py, then python build/protect.py
Writes the plaintext page to build/src/workouts/<DATE>.html. protect.py then
wraps it in the password gate at workouts/<DATE>.html. Plaintext sources are not
committed. Even behind the gate: no player names, no contact details.

Content is curated here (concise), not dumped from the Drill Library.
"""
from __future__ import annotations

import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------
# Session facts. Edit for a new workout.
# ----------------------------------------------------------------------------
DATE = "2026-09-07"
TITLE = "Monday, September 7"
EYEBROW = "Small group workout"
TIME = "10am to 12pm"
PLACE = "Absolute Volleyball Club, San Rafael"
MAPS = "https://maps.google.com/?q=2145+Francisco+Blvd+E,+San+Rafael,+CA+94901"
FACTS = [
    ("Who", "Outside hitters and two setters."),
    ("Attending", "Madi, Sofie, Zara, Kareena, Liva, Nola, Rose, Elia, Devon, Amber, Miah"),
    ("Coaches", "Christen Hamilton and Song Mu"),
    ("Focus", "Two tracks, ball control and hitting, with a cross-court game to finish."),
]

# ----------------------------------------------------------------------------
# Drill write-ups. "how" is a list of steps (ordered=True renders 1, 2, 3),
# "keys" is a short list of coaching keys.
# ----------------------------------------------------------------------------
DRILLS = {
    "OS-10": {
        "name": "Thirty-Two (3v3 Two-Touch)",
        "setup": "3v3",
        "how": [
            "3v3. Setters in middle back, hitters in left back and right back.",
            "Only two touches to get the ball over: every dig is also the set.",
            "Middle back digs: dig-set to either pin. A pin digs: dig-set to the opposite pin, high enough to hit.",
            "All attacks go to the pins. No tipping. Free ball entry to the winning side, games to 15.",
        ],
        "keys": [
            "Good first touch: better the ball, move it forward and high.",
            "Attack with no fear. Every digger is a hitter a heartbeat later.",
            "Talk: \"mine\" before the pass, then name the attacker and call \"cover\".",
        ],
    },
    "BC-01": {
        "name": "One Arm Small Touch Progression",
        "setup": "Partners",
        "how": [
            "Partners line up across from each other, about 10 ft apart.",
            "Tosser holds the free hand up as the target. Passer drives the ball to the partner's head or hand.",
            "Passer calls \"mine\" plus the partner's name on every contact. Tosser counts and gives feedback.",
            "Doubles as ball control and hand-eye training: stay in a small controlled space, don't let the rally drift deep.",
            "40 right arm, 40 left arm, 20 right arm on one leg, 20 left arm on one leg, "
            "40 to yourself (right, left, two arms, then alternate), then 20 V-touches.",
        ],
        "keys": [
            "Play the ball on the flat inside of the forearm, elbow externally rotated.",
            "Watch the ball hit the platform on every rep.",
            "Arm never bends. Hold the finish toward the partner's hand.",
            "Balance both feet before every contact. Pass with the legs, not an arm swing.",
            "Keep the shoulder relaxed. A tight shoulder kills the drive.",
        ],
    },
    "BC-07": {
        "name": "Gopher 3s",
        "setup": "Trios",
        "how": [
            "Trios between the 10 ft line and the net. Two tossers on the net, passer at the 10 ft line.",
            "Passer shuffles toward tosser 1, who tosses a ball forward. Passer plays a tilt pass, "
            "dropping the shoulder closest to the target so the ball angles back past the target's outside hand.",
            "Target raises the outside hand high and calls good or bad on each rep.",
            "About 20 left and 20 right, then rotate the next passer in.",
            "Two-ball version: each tosser has a ball and tosses diagonally as the passer shuffles away. "
            "Passer tilts it back to the same tosser.",
        ],
        "keys": [
            "Drop the inside shoulder to tilt the ball back. Do not swing the platform.",
            "Quiet platform: the angle comes from posture, not from chopping the arms.",
            "Aim past the target's opposite outside hand.",
        ],
    },
    "BC-09": {
        "name": "Russian Push",
        "setup": "Trios",
        "how": [
            "One passer between two tossers, one at the 10 ft line and one at the end line, each with a ball.",
            "Face the first tosser, back up off the ball, and free-ball pass to their forehead.",
            "Turn and shuffle back to face the other tosser, back up again, and pass the second ball the same way.",
            "Keep alternating for 45 to 90 seconds, then rotate.",
        ],
        "keys": [
            "Beat the ball back: set and balanced before it arrives, never pass on the move.",
            "Hands away from the hips between contacts. Platform out early and quiet, legs push the ball.",
            "Drop the inside shoulder to angle the ball back to target. Call the ball and the target every rep.",
        ],
    },
    "BC-12": {
        "name": "Directional Passing",
        "setup": "Stations",
        "how": [
            "Three dots: left corner, middle of the court (target), and middle back at the 15 ft line (target).",
            "Three lines: target catching, passer at the left net, and a ball line at the coach.",
            "Ball line throws antenna-high at the target. The passer pursues, reads, and passes to the dot, "
            "runs to right front to cover, then joins the target line. Target catches and runs to the back of the throwing line.",
            "About 45 seconds per slot. Run from left front, middle front, and right front, then the three back-row slots. "
            "Mix platform and hand reps.",
        ],
        "keys": [
            "Run fast to the dot and arrive at a target. Don't just send the ball somewhere.",
            "Always finish in cover: outside foot on the line, belly to target.",
            "Call \"mine\" and say what you are going to do. Forehead over the knee, hands away from the hips.",
        ],
    },
    "AT-01": {
        "name": "Hitting Progression",
        "setup": "Partners and coach toss",
        "ordered": True,
        "how": [
            "Transition footwork: outsides play off-blocker defense, step-cross hop to the cone, turn, and approach. "
            "Right sides jump and block, transition behind the cone, and approach. Middles swing block, transition around the far cone, and approach.",
            "Wall rotation: hitting shoulder to the wall, right knee up, elbow back, left arm high. "
            "Rotate forward, elbow high, hand under the ponytail, snap at the top, pull back and repeat.",
            "Kneeling wrist snap: right knee on a line, elbow back, hit the ball straight out of the hand so it comes back "
            "on your right side. Hand finishes no lower than the knee.",
            "Standing self-toss topspin: toss with the hitting hand rolling the fingers off the ball, elbow back immediately, "
            "snap straight down so it comes back to you. Then the thumb-up version, catching with the left hand.",
            "Jump and chuck through the net: face right front, reach back, jump with the elbow back, rotate in the air, "
            "and throw the ball through the net as a line drive. No chicken wings.",
            "Partners across the net: self toss with a full draw, left, right-left shuffle, snap under the net, then above the net to the partner.",
            "Under-net low-toss snap: coach tosses low, shuffle up with elbows back, hit under the net. "
            "Restrain the swing-through and work the snap. Feet all the way to the ball.",
            "Flamengo two step: coach tosses about a 1.5 tempo. Wait for the peak, then go on the last two steps with pace. "
            "Bicep to the ear, smooth swing, finish with the arm up.",
            "Full approach: timing step down, coach tosses about a 1.5 tempo. Wait for the peak, last two steps urgent. "
            "Rounds: straight on, fingers down, then thumb up to area 1. Everybody hits 4 per variation.",
        ],
        "keys": [
            "Body before arm: hips fire first, torso rotates, the arm comes last. Tighten the core as you swing.",
            "Load like a center fielder throwing home: elbow even with the shoulders, thumb pointing at your head. Bicep to the ear on the swing.",
            "More wrist than arm, hand loose. Hit quick, not hard. Listen for the splat.",
            "Hit the bottom of the ball for topspin. Fingers down is topspin, thumb up is the cut.",
            "Feet all the way to the ball. Wait for the peak of the toss, then go on the last two steps. Better late than early.",
            "Hit tall and land on two feet with knees out. Smooth before power.",
        ],
    },
    "TP-12": {
        "name": "Left v Left (Be Left)",
        "setup": "5v5",
        "how": [
            "5v5, competitive. Three back-row defenders and a setter in each back row, "
            "one blocker at left front matched to the cross-court hitter, no middle. Extra players wait off the court on their side.",
            "Coach enters a free ball. That side passes, sets, and the left front hits cross-court. "
            "The other side digs the hard cross, sets, and counters with its own left front cross. Play it out.",
            "Games to 5. Win the game and your side rotates: everyone moves one spot, a waiting player comes in, "
            "and a new hitter is at left front. Lose and your side stays put.",
            "To win the drill, a side has to rotate all the way through its players. First side to complete the full rotation wins.",
        ],
        "keys": [
            "Hitters hunt the hard cross and beat the single block over or around.",
            "Diggers sit deep cross. The swing geometry makes the seam and angle predictable.",
            "Every game counts. The side that stays put has to earn its way out.",
            "Keep swings controlled at this age. Soften the entry if pace runs high.",
        ],
    },
}

# (section label, [drill ids])
PLAN = [
    ("Warmup", ["OS-10"]),
    ("Track 1: Ball control", ["BC-01", "BC-07", "BC-09", "BC-12"]),
    ("Track 2: Hitting", ["AT-01"]),
    ("Game", ["TP-12"]),
]

# ----------------------------------------------------------------------------


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def render_list(items: list[str], ordered: bool = False) -> str:
    tag = "ol" if ordered else "ul"
    lis = "\n".join(f"      <li>{esc(i)}</li>" for i in items)
    return f"    <{tag}>\n{lis}\n    </{tag}>"


def render_drill(drill_id: str) -> str:
    d = DRILLS[drill_id]
    parts = [f'<div><h4>How to run</h4>\n{render_list(d["how"], d.get("ordered", False))}\n</div>']
    if d.get("keys"):
        parts.append(f'<div><h4>Coaching keys</h4>\n{render_list(d["keys"])}\n</div>')
    body = "\n".join(parts)
    return (
        f'<details class="drill" id="{drill_id.lower()}">\n'
        f'  <summary>\n'
        f'    <span class="dname">{esc(d["name"])}<span class="tags">{esc(drill_id)} &middot; {esc(d["setup"])}</span></span>\n'
        f'  </summary>\n'
        f'  <div class="dbody">\n{body}\n  </div>\n'
        f'</details>'
    )


def render_page(plan_html: str, facts_html: str) -> str:
    title = esc(TITLE)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} workout · Absolute 14 Black</title>
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
    <span><a href="../">Absolute 14 Black</a> &middot; 2026 to 2027 &middot; <a href="#" data-lock>Sign out</a></span>
  </div>
</footer>

</body>
</html>
"""


def build() -> str:
    out = []
    for label, ids in PLAN:
        rows = "\n".join(render_drill(i) for i in ids)
        out.append(f'<div class="block"><h3>{esc(label)}</h3>\n{rows}\n</div>')
    facts = "\n".join(f"    <dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in FACTS)
    return render_page("\n".join(out), facts)


if __name__ == "__main__":
    page = build()
    dest = os.path.join(ROOT, "build", "src", "workouts", f"{DATE}.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print(f"wrote {os.path.relpath(dest, ROOT)} ({len(page.encode('utf-8'))} bytes)")
