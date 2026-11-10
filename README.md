# Legend in the Mist - Printer-Friendly Character Sheets

A collection of lightweight, single-file HTML character sheets and pre-rendered PDFs for the **Legend in the Mist** tabletop roleplaying game.

Available in **English** (`en/`) and **Italian** (`it/`).

## 📂 Repository Structure

| | English | Italiano |
|---|---|---|
| Character sheet | [`en/CharacterSheet/`](en/CharacterSheet) | [`it/SchedaPersonaggio/`](it/SchedaPersonaggio) |
| Action cards | [`en/ActionCards/`](en/ActionCards) | [`it/CarteAzione/`](it/CarteAzione) |

**Character sheet** (`LitM_HeroSheet_<EN|IT>…`):
* **Standard** (`LitM_HeroSheet_EN.html`): features the stylized scratchmarks (`彡`) inside checkboxes. Also as PDF.
* **No Scratchmarks** (`…_NoScratchmarks.html`): a minimalist variant with clean, empty checkboxes. Also as PDF.
* **Web-Fillable** (`LitM_WebFillable_HeroSheet_EN.html`): fill it in the browser, with text fields and clickable checkboxes.

**Action cards** (`LitM_ActionCards_<EN|IT>_<A4|Letter>…`): a page of 9 reminder cards at standard trading-card size (63 × 88 mm, like Magic or Pokémon cards), with dashed cut lines. On each card, write an action (e.g. *Attack*), the power tags you usually use for it (e.g. *Sword*, *Mighty*), its weakness tags, and some notes.
* One file per paper size: **A4** or **Letter**.
* With scratchmarks, or with empty checkboxes (`…_NoScratchmarks.html`).

**Source** (only needed to change the sheets, see *Editing the sheets* below):
* `src/`: the templates and the language files (`src/lang/en.json`, `src/lang/it.json`).
* `build.py`: generates every HTML file in `en/` and `it/` from `src/`.

## 📖 How to Use

### Printing PDFs
Download and print the `.pdf` file corresponding to your preferred language and variant.

### Using HTML Sheets
1. Open any `.html` template in a modern web browser.
2. For Web-Fillable sheets, type directly into the fields and toggle checkboxes as needed.
3. Open the browser's print dialog (`Ctrl + P` or `Cmd + P`).
4. **Important Settings:** Enable **"Print Background Graphics"** (or "Background colors and images") in the settings so borders and shaded headers render correctly.

### Printing Action Cards
To get cards at the exact size, use these print settings:
* **Paper size:** the one in the file name (A4 or Letter).
* **Margins:** None.
* **Scale:** 100% / "Actual size" (not "Fit to page").
* **Background graphics:** On.

Cut along the dashed lines. The lines continue into the page margins, so you can still see them after the first cuts.

## 🛠️ Editing the sheets

The HTML files in `en/` and `it/` are **generated**: don't edit them directly, or your changes will be overwritten by the next build. Instead:

1. Change the layout in a template in `src/` (`hero_sheet.html`, `hero_sheet_web.html`, `action_cards.html`, `action_card.html`), or the wording in `src/lang/<language>.json`.
2. Run `python3 build.py` (Python 3, nothing to install). It rewrites every sheet, for every language.
3. Commit both the `src/` change and the regenerated files.
4. Re-export the PDFs from the browser if the character sheet changed.

Templates use `{{key}}` placeholders, filled from the language file. If a template uses a key that a language file doesn't have, the build stops and names it.

### Adding a language
1. Copy `src/lang/en.json` to `src/lang/<code>.json` (e.g. `es.json`).
2. Translate the values; keep the keys. Set `_code` (used in file names, e.g. `ES`), `_folder_sheet` and `_folder_cards` (the output folder names), and `lang` (the HTML language code, e.g. `es`).
3. Run `python3 build.py`. The new language appears in its own folder (e.g. `es/`).

## 📜 Credits & Acknowledgments

This project stands on the shoulders of existing fantastic designs for the game:

* **Original Structure:** The layout, fields, and core structure are directly based on the official [Legend in the Mist RPG - Character Sheet](https://cdn.shopify.com/s/files/1/2508/6356/files/Legend_in_the_Mist_RPG_-_Character_Sheet.pdf) provided by Son of Oak Game Studio.
* **Layout Inspiration:** The portrait-style organization and flow were inspired by the community-made [Legend in the Mist - Portrait Character Sheet](https://www.drivethrurpg.com/en/product/534731/legend-in-the-mist-portrait-character-sheet) available on DriveThruRPG.
* **AI Assistance:** The HTML/CSS coding and formatting adjustments were generated with the assistance of Google's Gemini AI.

---
*Created by @Destard for the TTRPG community. May your rolls be high and your stories unforgettable!*