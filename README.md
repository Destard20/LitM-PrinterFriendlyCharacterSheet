# Legend in the Mist - Printer-Friendly Character Sheets

A collection of lightweight, single-file HTML character sheets and pre-rendered PDFs for the **Legend in the Mist** tabletop roleplaying game.

Available in **English** (`en/`) and **Italian** (`it/`).

## 📂 Repository Structure

Each language folder has a `PDF/` folder (ready to print) and an `HTML/` folder (open in a browser, including the web-fillable versions):

| | English | Italiano |
|---|---|---|
| Character sheet, PDF | [`en/PDF/CharacterSheet/`](en/PDF/CharacterSheet) | [`it/PDF/SchedaPersonaggio/`](it/PDF/SchedaPersonaggio) |
| Character sheet, HTML | [`en/HTML/CharacterSheet/`](en/HTML/CharacterSheet) | [`it/HTML/SchedaPersonaggio/`](it/HTML/SchedaPersonaggio) |
| Action cards, PDF | [`en/PDF/ActionCards/`](en/PDF/ActionCards) | [`it/PDF/CarteAzione/`](it/PDF/CarteAzione) |
| Action cards, HTML | [`en/HTML/ActionCards/`](en/HTML/ActionCards) | [`it/HTML/CarteAzione/`](it/HTML/CarteAzione) |
| Fellowship card, PDF | [`en/PDF/Fellowship/`](en/PDF/Fellowship) | [`it/PDF/Compagnia/`](it/PDF/Compagnia) |
| Fellowship card, HTML | [`en/HTML/Fellowship/`](en/HTML/Fellowship) | [`it/HTML/Compagnia/`](it/HTML/Compagnia) |

**Character sheet**:
* One file per paper size: **A4** or **Letter** (on Letter the writing lines are slightly closer together, so both pages fit).
* **Standard** (`LitM_HeroSheet_EN_A4.html`, PDF): features the stylized scratchmarks (`彡`) inside checkboxes.
* **No Scratchmarks** (`…_NoScratchmarks.html`, PDF `… (A4, No Scratchmarks).pdf`): a minimalist variant with clean, empty checkboxes.
* **Web-Fillable** (`LitM_WebFillable_HeroSheet_EN_A4.html`): fill it in the browser, with text fields and clickable checkboxes.

**Action cards**: a page of 9 reminder cards at standard trading-card size (63 × 88 mm, like Magic or Pokémon cards), with dashed cut lines. On each card, write an action (e.g. *Attack*), the power tags you usually use for it (e.g. *Sword*, *Mighty*), its weakness tags, and some notes.
* One file per paper size: **A4** or **Letter**.
* **Standard** (`LitM_ActionCards_EN_A4.html`, PDF) with scratchmarks, or **No Scratchmarks** (`…_NoScratchmarks.html`, PDF) with empty checkboxes.
* **Web-Fillable** (`LitM_WebFillable_ActionCards_EN_A4.html`): type the action, tags and notes in the browser, tick the checkboxes, then print (see *Printing*). Text isn't saved, so print before closing the page.

**Fellowship card** (*Carta Compagnia*): the group's shared theme card. It has the Fellowship name (a power tag, with its scratch box), 6 power tags with scratch boxes, 2 weakness tags, the Quest, the Abandon / Improve / Milestone tracks, and boxes for Special Improvements and Notes.
* One file per paper size: **A4** or **Letter**.
* **Full page** (`LitM_Fellowship_EN_A4.html`, PDF `… (A4).pdf`), or **2 per page** (`…_2PerPage.html`, PDF `… (A4, 2 per Page).pdf`): the same card at half size, twice per sheet, with a dashed cut line across the middle.
* Each with scratchmarks, or **No Scratchmarks** (`…_NoScratchmarks.html`, PDF) with empty checkboxes.
* **Web-Fillable** (`LitM_WebFillable_Fellowship_EN_A4.html`, full page): type in the browser, tick the scratch boxes and track circles, then print. Text isn't saved, so print before closing the page.

**Source** (only needed to change the sheets, see *Editing the sheets* below):
* `src/`: the templates, the language files (`src/lang/en.json`, `src/lang/it.json`) and the fonts (`src/fonts/`).
* `build.py`: generates every HTML file and PDF in `en/` and `it/` from `src/`, and warns about any leftover file there that it no longer produces.
* `pdf-manifest.json`: written by `build.py`; remembers which HTML each PDF was printed from.
* `.github/workflows/build.yml`: runs `build.py` on GitHub automatically, then uploads to itch.io (see *Automatic builds* and *Publishing to itch.io* below).

## 📖 How to Use

### Printing PDFs
Download and print the `.pdf` file corresponding to your preferred language and variant.

### Using HTML Sheets
1. Open any `.html` template in a modern web browser.
2. For Web-Fillable sheets, type directly into the fields and toggle checkboxes as needed.
3. Open the browser's print dialog (`Ctrl + P` or `Cmd + P`).
4. The sheets ask the browser to print their backgrounds. If box titles still have a line through them, enable **"Print Background Graphics"** (or "Background colors and images") in the print settings.

### Printing
Print PDFs at 100% scale ("Actual size", not "Fit to page"). For action cards printed from HTML, use these settings to get cards at the exact size:
* **Paper size:** the one in the file name (A4 or Letter).
* **Margins:** None.
* **Scale:** 100% / "Actual size" (not "Fit to page").
* **Background graphics:** On.

Cut along the dashed lines. The lines continue into the page margins, so you can still see them after the first cuts.

## 🛠️ Editing the sheets

The HTML and PDF files in `en/` and `it/` are **generated**: don't edit them directly, or your changes will be overwritten by the next build. Instead, change the layout in a template in `src/` (`hero_sheet.html`, `hero_sheet_web.html`, `action_cards.html`, `action_card.html`, `action_card_web.html`, `action_card_web.css`, `fellowship.html`, `fellowship_spread.html`, `fellowship_web_spread.html`, `fellowship_web.css`), or the wording in `src/lang/<language>.json`.

### Automatic builds (GitHub)
When a change to `src/` or `build.py` is pushed to `main`, a GitHub Action rebuilds every HTML file and the PDFs that changed, and commits them back as **github-actions[bot]**. Pull afterwards (`git pull`) before pushing again.

You can also start it by hand on any branch: **Actions** tab → **Build sheets** → **Run workflow**.

### Building locally
* `python3 build.py`: HTML only (Python 3, nothing to install).
* `python3 build.py --pdf`: HTML, plus the PDFs whose HTML changed.
* `python3 build.py --pdf-all`: HTML, plus every PDF.

PDFs are printed with a headless browser. It uses Chrome, Edge, Chromium or Brave if one is installed (Edge comes with Windows), and falls back to Firefox if `geckodriver` is installed. To pick the browser yourself, set `LITM_BROWSER` to the path of a Chrome, Edge, Chromium or Brave executable. PDFs change on every print (they contain a timestamp), so `pdf-manifest.json` keeps track of which ones are already up to date.

Commit the `src/` change together with the regenerated files (or just push `src/` and let the GitHub Action do the rest).

The fonts (see *Credits*) are embedded into every sheet by `build.py`, so the sheets and PDFs look the same on every computer, with nothing to install. To change fonts or add character sets, edit and run `tools/fetch_fonts.py`, which downloads them from Google Fonts into `src/fonts/`.

Templates use `{{key}}` placeholders, filled from the language file. If a template uses a key that a language file doesn't have, the build stops and names it.

### Adding a language
1. Copy `src/lang/en.json` to `src/lang/<code>.json` (e.g. `es.json`).
2. Translate the values; keep the keys. Set `_code` (used in file names, e.g. `ES`), `_folder_sheet`, `_folder_cards` and `_folder_fellowship` (the output folder names), and `lang` (the HTML language code, e.g. `es`).
3. Run `python3 build.py`. The new language appears in its own folder (e.g. `es/`).

### Publishing to itch.io
The [itch.io page](https://destard20.itch.io/litm-printerfriendlysheets) is updated by the same GitHub Action, after each build on `main`, using itch's upload tool [butler](https://itch.io/docs/butler/). It uploads:
* the English PDFs with scratchmarks: character sheet, action cards and full-page Fellowship card, A4 and Letter (one download each);
* one zip per language (`en-html`, `it-html`) with all of that language's HTML files: standard, no-scratchmarks and web-fillable.

`PDF_LANGUAGES` and `ZIP_LANGUAGES` in `tools/publish_itch.py` control which languages go to itch. Files that didn't change are skipped.

One-time setup:
1. Create an API key at <https://itch.io/user/settings/api-keys>.
2. Save it as a repository secret named `BUTLER_API_KEY` (GitHub repo → **Settings** → **Secrets and variables** → **Actions**, or `gh secret set BUTLER_API_KEY`).

Without the secret, the Action just skips the upload. To upload by hand: **Actions** → **Build sheets** → **Run workflow** (on `main`; tick *Upload every file* to re-upload unchanged files too). Locally, `python3 tools/publish_itch.py --dry-run` shows what would be uploaded.

itch.io has no API for the page text, screenshots or devlogs: edit those on itch.io directly.

## 📜 Credits & Acknowledgments

This project stands on the shoulders of existing fantastic designs for the game:

* **Original Structure:** The layout, fields, and core structure are directly based on the official [Legend in the Mist RPG - Character Sheet](https://cdn.shopify.com/s/files/1/2508/6356/files/Legend_in_the_Mist_RPG_-_Character_Sheet.pdf) provided by Son of Oak Game Studio.
* **Layout Inspiration:** The portrait-style organization and flow were inspired by the community-made [Legend in the Mist - Portrait Character Sheet](https://www.drivethrurpg.com/en/product/534731/legend-in-the-mist-portrait-character-sheet) available on DriveThruRPG.
* **Fonts:** [EB Garamond](https://fonts.google.com/specimen/EB+Garamond) for all text, [Noto Sans Symbols 2](https://fonts.google.com/noto/specimen/Noto+Sans+Symbols+2) and [Noto Sans Symbols](https://fonts.google.com/noto/specimen/Noto+Sans+Symbols) for the icons, and [Noto Sans JP](https://fonts.google.com/noto/specimen/Noto+Sans+JP) for the 彡 scratchmark. All are under the [SIL Open Font License](https://openfontlicense.org); the licence texts are in `src/fonts/`.
* **AI Assistance:** The HTML/CSS, the build scripts and the formatting were made with the assistance of AI tools.

---
*Created by @Destard for the TTRPG community. May your rolls be high and your stories unforgettable!*