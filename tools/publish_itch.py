#!/usr/bin/env python3
"""Upload the built sheets to the itch.io page with butler (itch's upload tool).

    python3 tools/publish_itch.py --dry-run   # show what would be uploaded
    python3 tools/publish_itch.py             # upload (needs butler + BUTLER_API_KEY)
    python3 tools/publish_itch.py --force     # upload even channels that didn't change

Each butler "channel" is one download on the itch page:
  * every PDF gets its own channel, so it downloads directly as a PDF;
  * each language's HTML/ folder is one channel, which itch serves as a zip.

Run `python3 build.py --pdf` first. The GitHub Action does both automatically.
Environment:
  BUTLER_API_KEY  the itch.io API key (https://itch.io/user/settings/api-keys)
  ITCH_TARGET     user/page to upload to (default: destard20/litm-printerfriendlysheets)
  BUTLER          path to the butler executable (default: butler on PATH)
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (reuse the paper sizes and naming rules)

DEFAULT_TARGET = "destard20/litm-printerfriendlysheets"
# itch tags a download as a game for an operating system if its channel name contains these.
PLATFORM_WORDS = ("win", "linux", "mac", "osx", "android")


def channels() -> list:
    """(channel, path) for every download, following the names build.py gives the files."""
    result = []
    for lang_file in sorted(build.LANG_DIR.glob("*.json")):
        data = json.loads(lang_file.read_text(encoding="utf-8"))
        lang = lang_file.stem
        out = ROOT / lang
        sheet_pdf = out / "PDF" / data["_folder_sheet"]
        cards_pdf = out / "PDF" / data["_folder_cards"]
        no_scratch = build.NO_SCRATCH_PDF

        result.append((f"{lang}-character-sheet", sheet_pdf / f"{data['title_sheet']}.pdf"))
        result.append((f"{lang}-character-sheet-no-scratchmarks", sheet_pdf / f"{data['title_sheet']} ({no_scratch}).pdf"))
        for paper in build.PAPERS:
            p = paper.lower()
            result.append((f"{lang}-action-cards-{p}", cards_pdf / f"{data['title_cards']} ({paper}).pdf"))
            result.append((f"{lang}-action-cards-{p}-no-scratchmarks",
                           cards_pdf / f"{data['title_cards']} ({paper}, {no_scratch}).pdf"))
        result.append((f"{lang}-html", out / "HTML"))
    return result


def check(chans: list) -> None:
    problems = []
    for channel, path in chans:
        bad = [w for w in PLATFORM_WORDS if w in channel]
        if bad:
            problems.append(f"channel '{channel}' contains '{bad[0]}', which itch would read as an OS name")
        if not path.exists():
            problems.append(f"missing {path.relative_to(ROOT)} (run: python3 build.py --pdf)")
        elif path.is_dir():
            others = [f for f in path.rglob("*") if f.is_file() and f.suffix != ".html"]
            if others:
                problems.append(f"{path.relative_to(ROOT)} has non-HTML files, e.g. {others[0].relative_to(ROOT)}")
    if problems:
        sys.exit("error:\n  " + "\n  ".join(problems))


def version() -> str:
    """e.g. 2026-11-10-3be15b3: the date plus the commit, shown as the version on itch."""
    # The current commit, which in the GitHub Action includes the bot's "regenerate" commit.
    try:
        sha = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        sha = os.environ.get("GITHUB_SHA", "")[:7] or "local"
    return f"{datetime.date.today().isoformat()}-{sha}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload the sheets to itch.io with butler.")
    parser.add_argument("--dry-run", action="store_true", help="only print what would be uploaded")
    parser.add_argument("--force", action="store_true", help="upload every channel, even if unchanged")
    args = parser.parse_args()

    target = os.environ.get("ITCH_TARGET", DEFAULT_TARGET)
    chans = channels()
    check(chans)

    butler = os.environ.get("BUTLER") or shutil.which("butler") or "butler"
    if not args.dry_run:
        if not os.environ.get("BUTLER_API_KEY"):
            sys.exit("error: BUTLER_API_KEY is not set (create one at https://itch.io/user/settings/api-keys)")
        if not shutil.which(butler):
            sys.exit("error: butler not found; install it from https://itch.io/docs/butler/ or set BUTLER")

    ver = version()
    print(f"{'Would upload' if args.dry_run else 'Uploading'} {len(chans)} downloads to {target} (version {ver})")
    for channel, path in chans:
        cmd = [butler, "push", str(path), f"{target}:{channel}", "--userversion", ver]
        if not args.force:
            cmd.append("--if-changed")
        print(f"  {channel:42} <- {path.relative_to(ROOT)}{'/' if path.is_dir() else ''}")
        if not args.dry_run:
            subprocess.run(cmd, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
