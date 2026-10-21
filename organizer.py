import re
import shutil
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\YourName\Documents\School").resolve()
OTHER = ROOT / "other"

if not ROOT.is_dir():
    print("ROOT is not a folder, check the path at the top")
    sys.exit()
OTHER.mkdir(exist_ok=True)


def split_words(text):
    return [w.lower() for w in re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+", text)]


def match_score(folder_name, item_name):
    """How well a folder name matches an item name (0 = no match)."""
    folder_lower = folder_name.lower()
    item_lower = item_name.lower()
    score = 0
    if folder_lower in item_lower:  # "maths" inside "maths_homework"
        score = len(folder_lower)
    for fw in split_words(folder_name):
        for iw in split_words(item_name):
            short, long = sorted((fw, iw), key=len)
            if len(short) >= 3 and long.startswith(
                short
            ):  # "prob" starts "probability"
                score = max(score, len(short))
    return score


def find_match(item):
    """Return the most relevant folder for this item, or None."""
    label = item.name if item.is_dir() else item.stem  # files: ignore the extension
    best = None
    best_key = (0, 0)
    for folder in ROOT.rglob("*"):
        if not folder.is_dir():
            continue
        if folder == OTHER or OTHER in folder.parents:
            continue
        if folder == item or item in folder.parents:
            continue
        score = match_score(folder.name, label)
        key = (score, len(folder.name))
        if score > 0 and key > best_key:
            best, best_key = folder, key
    return best


def move_to(item, folder):
    if item.parent == folder:
        print(f"'{item.name}' is already in {folder.name}/")
        return
    destination = folder / item.name
    count = 1
    while destination.exists():
        if item.is_dir():
            new_name = f"{item.name}({count})"
        else:
            new_name = f"{item.stem}({count}){item.suffix}"
        destination = folder / new_name
        count += 1
    shutil.move(str(item), str(destination))
    print(f"Moved {item.name} -> {folder.name}/{destination.name}")


for old in list(OTHER.iterdir()):
    match = find_match(old)
    if match:
        move_to(old, match)


raw = input("File or folder to save (Enter to skip): ").strip().strip('"')
if raw:
    item = Path(raw).resolve()
    if not item.exists():
        print("that file/folder doesn't exist")
        sys.exit()
    match = find_match(item)
    move_to(item, match if match else OTHER)
