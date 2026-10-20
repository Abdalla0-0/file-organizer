import shutil
import sys
from pathlib import Path

folder = Path(input("Input Folder Name: "))
if not folder.is_dir():
    print("\033[1;31;4mthat's not a folder\033[0m")
    sys.exit()


for item in folder.iterdir():
    if item.is_dir():
        continue

    ext = item.suffix.lower().lstrip(".")
    name = (
        ext if ext else "other"
    )  # we create other n put them there if nothing matches

    tgt = folder / name
    tgt.mkdir(exist_ok=True)

    dest = tgt / item.name
    count = 1
    while dest.exists():
        destination = tgt / f"{item.stem}({count}){item.suffix}"
        count += 1

    shutil.move(str(item), str(tgt / item.name))
    print(f"Moved {item.name} -> {name}/")
