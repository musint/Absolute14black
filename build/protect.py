"""Wrap the site's pages in the team password gate.

Usage: python build/protect.py
Reads every plaintext page under build/src/ (which is not committed), encrypts
its <title> and <body> with a key derived from the team password, and writes a
shell page to the same relative path at the repo root. The shell holds the
masthead, the password form, the encrypted payload, and assets/gate.js.

Password: the SITE_PASSWORD environment variable, else build/.password (not
committed). Matching is case-insensitive, so the password is stored uppercased.
Salt: build/salt.txt, created once and committed, so a device that unlocked an
earlier build stays unlocked after a rebuild.
"""
from __future__ import annotations

import base64
import html
import json
import os
import re
import secrets
import sys

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "build", "src")
ITERATIONS = 250_000

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' fill='%230a0a0b'/%3E"
           "%3Ctext x='32' y='47' font-family='Arial Narrow,Arial,sans-serif' font-weight='900' "
           "font-size='40' fill='white' text-anchor='middle'%3E14%3C/text%3E%3C/svg%3E")
FONTS = ("https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,400;0,700;1,400"
         "&family=Big+Shoulders+Display:wght@700;900&display=swap")


def read_password() -> str:
    pw = os.environ.get("SITE_PASSWORD", "").strip()
    if not pw:
        path = os.path.join(ROOT, "build", ".password")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                pw = f.read().strip()
    if not pw:
        sys.exit("No password. Set SITE_PASSWORD or create build/.password (one line).")
    return pw.upper()


def load_salt() -> bytes:
    path = os.path.join(ROOT, "build", "salt.txt")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return base64.b64decode(f.read().strip())
    salt = secrets.token_bytes(16)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(base64.b64encode(salt).decode() + "\n")
    return salt


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS)
    return kdf.derive(password.encode("utf-8"))


def split_page(source: str) -> tuple[str, str]:
    title = re.search(r"<title>(.*?)</title>", source, re.S)
    body = re.search(r"<body[^>]*>(.*)</body>", source, re.S)
    if not title or not body:
        raise ValueError("page needs a <title> and a <body>")
    return html.unescape(title.group(1).strip()), body.group(1).strip()


def encrypt_page(key: bytes, salt: bytes, title: str, body: str) -> str:
    iv = secrets.token_bytes(12)
    plain = json.dumps({"title": title, "body": body}, ensure_ascii=False).encode("utf-8")
    data = AESGCM(key).encrypt(iv, plain, None)
    return json.dumps({
        "v": 1,
        "iter": ITERATIONS,
        "salt": base64.b64encode(salt).decode(),
        "iv": base64.b64encode(iv).decode(),
        "data": base64.b64encode(data).decode(),
    })


def shell(payload_json: str, depth: int) -> str:
    rel = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Absolute 14 Black</title>
<meta name="description" content="Absolute Volleyball Club 14 Black team site. Coach password required.">
<meta name="theme-color" content="#0a0a0b">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>

<header class="mast">
  <div class="wrap">
    <p class="eyebrow">Absolute Volleyball Club</p>
    <p class="jersey" aria-label="14 Black"><span class="num">14</span><span class="team">Black</span></p>
    <p class="season"><b>Team site</b> &middot; 2026 to 2027</p>
  </div>
</header>

<main class="wrap">
  <form class="gate" id="gate" hidden>
    <h1 class="gate-title">Coaches Access</h1>
    <p class="gate-help">Enter the coach password to continue.</p>
    <input type="text" name="username" value="team" autocomplete="username" hidden tabindex="-1" aria-hidden="true">
    <label class="gate-label" for="pw">Password</label>
    <input class="gate-input" id="pw" name="password" type="password" autocomplete="current-password" autocapitalize="characters" spellcheck="false" required>
    <button class="btn" type="submit">Enter</button>
    <p class="gate-msg" id="msg" role="alert" hidden>That password didn't work. Try again.</p>
  </form>
  <noscript><p class="gate-help">This site needs JavaScript turned on to unlock.</p></noscript>
</main>

<script id="payload" type="application/json">{payload_json}</script>
<script src="{rel}assets/gate.js" defer></script>
</body>
</html>
"""


def main() -> None:
    password = read_password()
    salt = load_salt()
    key = derive_key(password, salt)
    written = []
    for dirpath, _, files in os.walk(SRC):
        for name in files:
            if not name.endswith(".html"):
                continue
            src_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(src_path, SRC)
            with open(src_path, encoding="utf-8") as f:
                title, body = split_page(f.read())
            depth = rel_path.count(os.sep)
            out = shell(encrypt_page(key, salt, title, body), depth)
            dest = os.path.join(ROOT, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
            written.append((rel_path.replace(os.sep, "/"), len(out)))
    if not written:
        sys.exit(f"No pages found under {SRC}")
    for path, size in written:
        print(f"protected {path} ({size} bytes)")


if __name__ == "__main__":
    main()
