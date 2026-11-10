#!/usr/bin/env python3
"""Download the fonts that build.py embeds into every sheet.

    python3 tools/fetch_fonts.py

You only need this to change fonts or add character sets (e.g. "cyrillic" for a
new language); the downloaded files are committed in src/fonts/, so build.py
works offline.

All fonts are under the SIL Open Font License, from Google Fonts:
  * EB Garamond: all text (regular, bold, italic). Only the "latin" character set
    (English, Italian and most Western European languages); add "latin-ext" to
    SUBSETS below for e.g. Polish or Czech.
  * Noto Sans Symbols 2 and Noto Sans Symbols: the tag/theme icons and the scissors,
    trimmed to just those characters (⚔ is only in the first Noto Sans Symbols).
  * Noto Sans JP: the 彡 scratchmark, trimmed to just that character.

Writes src/fonts/*.woff2, the licences, and src/fonts/fonts.json, which tells
build.py which file is which.
"""
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "fonts"

# Google Fonts only serves woff2 to browsers it recognises, so look like one.
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
CSS_API = "https://fonts.googleapis.com/css2"
LICENSE_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/{dir}/OFL.txt"

SYMBOLS = "♦▽☘♛✂"   # from Noto Sans Symbols 2
SWORDS = "⚔"         # Noto Sans Symbols 2 doesn't have it; Noto Sans Symbols does
SCRATCH = "彡"

SUBSETS = ["latin"]

# (family name used in the CSS, Google Fonts family spec, subsets to keep or None for a text= subset,
#  text to subset to, file name prefix, licence folder in github.com/google/fonts/ofl)
FONTS = [
    ("EB Garamond", "EB Garamond:ital,wght@0,400;0,700;1,400", SUBSETS, None, "EBGaramond", "ebgaramond"),
    ("LitM Symbols", "Noto Sans Symbols 2", None, SYMBOLS, "NotoSansSymbols2-subset", "notosanssymbols2"),
    ("LitM Symbols", "Noto Sans Symbols", None, SWORDS, "NotoSansSymbols-subset", "notosanssymbols"),
    ("LitM Scratch", "Noto Sans JP:wght@700", None, SCRATCH, "NotoSansJP-subset", "notosansjp"),
]

FACE = re.compile(r"(?:/\*\s*(?P<subset>[\w-]+)\s*\*/\s*)?@font-face\s*\{(?P<body>[^}]*)\}")


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def prop(body: str, name: str) -> str:
    m = re.search(rf"{name}\s*:\s*([^;]+);", body)
    return m.group(1).strip() if m else ""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.woff2"):
        old.unlink()
    faces = []
    for css_family, spec, subsets, text, prefix, license_dir in FONTS:
        query = {"family": spec, "display": "block"}
        if text:
            query["text"] = text
        css = get(f"{CSS_API}?{urllib.parse.urlencode(query)}").decode("utf-8")
        for m in FACE.finditer(css):
            subset, body = m.group("subset"), m.group("body")
            if subsets is not None and subset not in subsets:
                continue
            style, weight = prop(body, "font-style") or "normal", prop(body, "font-weight") or "400"
            url = re.search(r"url\(([^)]+)\)", body).group(1)
            same = next((f for f in faces if f["url"] == url), None)
            if same:  # a variable font: one file covers several weights
                weights = sorted({int(w) for w in same["weight"].split()} | {int(weight)})
                same["weight"] = f"{weights[0]} {weights[-1]}"
                continue
            name = f"{prefix}-{weight}{'-italic' if style == 'italic' else ''}{'-' + subset if subset else ''}.woff2"
            (OUT / name).write_bytes(get(url))
            faces.append({
                "url": url,
                "family": css_family,
                "file": name,
                "weight": weight,
                "style": style,
                "unicode_range": prop(body, "unicode-range"),
            })
            print("  ", name)
        (OUT / f"LICENSE-{prefix.split('-')[0]}.txt").write_bytes(get(LICENSE_URL.format(dir=license_dir)))
    for face in faces:
        del face["url"]
    (OUT / "fonts.json").write_text(json.dumps(faces, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(faces)} font files and src/fonts/fonts.json")


if __name__ == "__main__":
    main()
