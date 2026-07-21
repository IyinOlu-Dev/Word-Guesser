# Word Guesser

A Wordle-style word guessing game with a desktop GUI, built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

Guess the hidden word within 6 tries. After each guess, each letter is colored to show how close you are:

- 🟩 **Green** — correct letter, correct position
- 🟨 **Yellow** — correct letter, wrong position
- ⬜ **Gray** — letter not in the word

All words in `words.txt` are common, everyday words — no obscure or technical terms.

## Download

Prebuilt executables for Windows, macOS, and Linux are available on the [Releases page](../../releases/latest). No Python installation required.

1. Go to the [latest release](../../releases/latest)
2. Download the zip for your OS:
   - `wordguesser-windows.zip`
   - `wordguesser-macos.zip`
   - `wordguesser-linux.zip`
3. **Extract the entire zip** to a folder — don't move just the executable on its own
4. Run the app from inside the extracted folder:
   - **Windows:** double-click `wordguesser-windows.exe`
   - **macOS:** open `wordguesser-macos.app` (if Gatekeeper blocks it, right-click → Open, or go to System Settings → Privacy & Security → "Open Anyway")
   - **Linux:** `chmod +x wordguesser-linux && ./wordguesser-linux`

> **Note:** the extracted folder includes an `_internal` folder alongside the executable — that's normal. It holds the bundled Python runtime and supporting libraries. Don't delete it or separate it from the executable.

> Some browsers or antivirus tools may flag the download as unrecognized/unsigned software. This is a common false positive for indie-built executables that aren't code-signed — the source is fully open in this repo if you'd like to verify it yourself.

## Running from source

Requires Python 3.14+ and [`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/IyinOlu-Dev/wordle.git
cd wordle/local
uv sync
uv run UI.py
```

A terminal-only version is also available:

```bash
uv run main.py
```

## Project structure

```
local/
├── UI.py          # CustomTkinter GUI and app entry point
├── engine.py       # Core game logic (length check, letter comparison)
├── main.py         # Terminal/CLI version of the game
├── words.txt        # Word list
├── icon.ico / icon.icns   # App icons (Windows / macOS)
└── pyproject.toml   # Project dependencies
```

## How it works

- `engine.py` contains `GameMechanics`, which validates guess length and compares the guess against the secret word, returning a color per letter (green/yellow/gray).
- `UI.py` builds the GUI: each guess is a row of single-letter entry boxes that auto-advance as you type, colored in place after submission, with a popup on win/loss.
- Words are loaded from `words.txt` and bundled into the executable at build time.

## Building executables

Executables are built automatically via GitHub Actions on every version tag push (`v*`), using PyInstaller in `--onedir` mode, then zipped per platform and published to [Releases](../../releases). See `.github/workflows/` for the build pipeline.

To build locally:

```bash
cd local
uv sync
uv run pyinstaller --onedir --windowed --add-data "words.txt:." --icon icon.icns UI.py
```

(Use `;` instead of `:` as the `--add-data` separator on Windows, and `icon.ico` instead of `icon.icns`.)

**LICENSE**

**MIT**
