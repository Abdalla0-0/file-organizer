# File Organizer

A Python command-line tool that moves a file or folder into the best-matching category folder, based on its name. It searches through nested folders, sends anything it can't match to an `other` folder, and re-checks `other` on every run in case a matching folder has been created since.

## Features

- **Name matching:** finds the most relevant folder for an item by comparing names, ignoring capital letters and file extensions.
- **Partial matches:** `prob_notes.pdf` goes to `Probability`, and `phys_lab.docx` goes to `Physics`.
- **camelCase and separators:** `sheetMathTut`, `sheet_math_tut` and `sheet math tut` are all read as separate words.
- **Nested folders:** looks inside folders within folders, however deep.
- **Fallback folder:** anything with no match goes to `other`, and `other` is re-checked at the start of every run.
- **No overwriting:** if a file with the same name already exists in the destination, the new one is saved as `notes(1).pdf`, `notes(2).pdf`, and so on.
- **Safe by design:** it never moves a folder into itself, and it tells you if an item is already where it belongs.

## How it works

1. You keep one main folder (`ROOT`) that holds all your category folders, for example `Maths`, `Physics` and `Probability`.
2. On every run, the script first looks at everything in `other` and moves anything that now has a matching folder.
3. It then asks for a file or folder to save. Press Enter to skip this and only re-check `other`.
4. It scores every folder in `ROOT` against the item's name. The folder with the longest matching piece wins, and if there is a tie the longer folder name wins.
5. The item is moved into the winning folder, or into `other` if nothing matched.

### Example

```
ROOT/
  Maths/
  Physics/
  Probability/
  other/
```

| Item you save        | Where it goes            |
| -------------------- | ------------------------ |
| `maths_homework.pdf` | `Maths/`                 |
| `prob_notes.pdf`     | `Probability/`           |
| `phys_lab.docx`      | `Physics/`               |
| `random.txt`         | `other/`                 |

If you later create a `random` folder and run the script again, `random.txt` moves from `other/` into `random/`.

## Requirements

- Python 3
- No extra packages. It only uses the standard library (`pathlib`, `shutil`, `re`, `sys`).

## Setup and usage

1. Download `organizer.py`.
2. Open it and set `ROOT` near the top to the folder that holds your category folders:

   ```python
   ROOT = Path(r"C:\Users\YourName\Documents\School").resolve()
   ```

3. Run it:

   ```
   python organizer.py
   ```

4. When asked, paste the full path of the file or folder you want to save, then press Enter. On Windows, the easiest way to get the path is to right-click the file and choose **Copy as path**. The quotes it adds are removed automatically.

   ```
   File or folder to save (Enter to skip): C:\Users\YourName\Downloads\maths_homework.pdf
   Moved maths_homework.pdf -> Maths/maths_homework.pdf
   ```

> **Warning:** this script moves real files and has no undo. Try it on a test folder with a few fake files before pointing `ROOT` at anything important.

## Limitations

- Matching is by name only. A file called `scan001.pdf` can't be matched to a folder.
- Names with no capitals and no separators, like `sheetmathtut`, are read as one long word and may not match.
- `ROOT` is set inside the code, so you have to edit the file to change it.
- The item to save has to exist already, and you have to give its full path.

## Ideas for the future

- **Match by file contents:** read the text inside PDFs, Word files and text files and score it against keywords for each folder, so files with unhelpful names get sorted correctly.
- **Run automatically:** watch an inbox folder (like Downloads) in the background so new files are sorted without giving a path.
- **Preview mode:** show what would be moved and ask for confirmation before moving anything.
- **Log file and undo:** record every move with the time, old location and new location, and use it to undo the last batch.
- **Fuzzier matching:** handle typos and abbreviations that aren't the start of a word.
- **Settings file:** move `ROOT` and other options out of the code into a config file.
- **Efficiency:** scan the folder tree once and cache it, instead of rescanning for every item, which would matter if the tree gets large. Cached folder lists can go stale when folders change, so the background-running version would need to refresh them.