#!/usr/bin/env python3
import os
import argparse
from datetime import datetime


def rename_files(directory, dry_run=True):
    directory = os.path.abspath(os.path.expanduser(directory))
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    single_name_limit = 36
    month_codes = "123456789ABC"
    files_by_month = {}
    for filename in os.listdir(directory):
        src = os.path.join(directory, filename)
        if os.path.isfile(src):
            modified = os.path.getmtime(src)
            date = datetime.fromtimestamp(modified)
            folder = f"{date.year % 10}{month_codes[date.month - 1]}"
            files_by_month.setdefault(folder, []).append((modified, filename))

    rename_plan = []
    for folder, files in sorted(files_by_month.items()):
        files.sort(key=lambda item: item[0])
        width = 1 if len(files) < single_name_limit else max(
            2, len(_base36(len(files) - 1))
        )

        for i, (_, filename) in enumerate(files):
            _, ext = os.path.splitext(filename)
            new_name = _base36(i).rjust(width, "0") + ext
            src = os.path.join(directory, filename)
            dst = os.path.join(directory, folder, new_name)
            rename_plan.append((filename, folder, new_name, src, dst))

    for filename, folder, new_name, _, dst in rename_plan:
        if os.path.lexists(dst):
            raise FileExistsError(f"Destination already exists: {dst}")

    for filename, folder, new_name, src, dst in rename_plan:
        if dry_run:
            print(f"[dry-run] Would rename: '{filename}' -> '{folder}/{new_name}'")
        else:
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                os.rename(src, dst)
                print(f"Renamed: '{filename}' -> '{folder}/{new_name}'")
            except Exception as e:
                print(f"Error renaming '{filename}': {e}")


def _base36(number):
    characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if number == 0:
        return "0"
    result = ""
    while number:
        number, remainder = divmod(number, len(characters))
        result = characters[remainder] + result
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show or apply file renames (local use).")
    parser.add_argument("directory", nargs="?", default=".",
                        help="Target directory (default: current working directory)")
    parser.add_argument("--apply", action="store_true", help="Actually perform renames")
    args = parser.parse_args()

    try:
        rename_files(args.directory, dry_run=not args.apply)
    except Exception as e:
        print(f"Failed: {e}")