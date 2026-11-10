#!/usr/bin/env python3
"""Upload the built sheets to the itch.io page with butler (itch's upload tool).

    python3 tools/publish_itch.py --dry-run   # show what would be uploaded
    python3 tools/publish_itch.py             # upload (needs butler + BUTLER_API_KEY)
    python3 tools/publish_itch.py --force     # upload even channels that didn't change

Each butler "channel" is one download on the itch page:
  * the PDFs of PDF_LANGUAGES with scratchmarks (character sheet and action cards, A4 and
    Letter), one channel each, so they download directly as PDFs;
  * for every language in ZIP_LANGUAGES, one channel with all its HTML files (printable,
    no-scratchmarks and web-fillable), which itch serves as a zip.
Everything else stays available on GitHub.

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
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (reuse the paper sizes and naming rules)

DEFAULT_TARGET = "destard20/litm-printerfriendlysheets"
# itch tags a download as a game for an operating system if its channel name contains these.
PLATFORM_WORDS = ("win", "linux", "mac", "osx", "android")

PDF_LANGUAGES = ("en",)       # languages (src/lang/<code>.json) whose PDFs get their own download
ZIP_LANGUAGES = ("en", "it")  # languages that get a zip with all their HTML files


def channels(stage: Path) -> list:
    """(channel, path) for every download, following the names build.py gives the files.

    The HTML zips are assembled in `stage`, a temporary folder, so they hold only HTML files."""
    result = []
    for lang in PDF_LANGUAGES:
        data = json.loads((build.LANG_DIR / f"{lang}.json").read_text(encoding="utf-8"))
        pdf = ROOT / lang / "PDF"
        for paper in build.PAPERS:
            # The A4 sheet keeps the channel name it had before Letter existed, so itch updates
            # that download instead of adding a new one.
            sheet = f"{lang}-character-sheet" + ("" if paper == "A4" else f"-{paper.lower()}")
            result.append((sheet, pdf / data["_folder_sheet"] / f"{data['title_sheet']} ({paper}).pdf"))
        for paper in build.PAPERS:
            result.append((f"{lang}-action-cards-{paper.lower()}",
                           pdf / data["_folder_cards"] / f"{data['title_cards']} ({paper}).pdf"))
        for paper in build.PAPERS:
            result.append((f"{lang}-fellowship-{paper.lower()}",
                           pdf / data["_folder_fellowship"] / f"{data['title_fellowship']} ({paper}).pdf"))

    for lang in ZIP_LANGUAGES:
        html_dir = ROOT / lang / "HTML"
        html_stage = stage / f"{lang}-html"
        for html in sorted(html_dir.rglob("*.html")):
            dest = html_stage / html.relative_to(html_dir)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(html, dest)
        result.append((f"{lang}-html", html_stage))
    return result


def check(chans: list) -> None:
    problems = []
    for channel, path in chans:
        bad = [w for w in PLATFORM_WORDS if w in channel]
        if bad:
            problems.append(f"channel '{channel}' contains '{bad[0]}', which itch would read as an OS name")
        if path.is_dir():
            if not any(path.rglob("*.html")):
                problems.append(f"no HTML files for channel '{channel}' (run: python3 build.py)")
        elif not path.exists():
            problems.append(f"missing {path.relative_to(ROOT)} (run: python3 build.py --pdf)")
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
    with tempfile.TemporaryDirectory(prefix="litm-itch-") as stage:
        return publish(Path(stage), target, args)


def show(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else f"{path.name}/ ({len(list(path.rglob('*.html')))} HTML files)"


def publish(stage: Path, target: str, args) -> int:
    chans = channels(stage)
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
        print(f"  {channel:26} <- {show(path)}")
        if not args.dry_run:
            subprocess.run(cmd, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
