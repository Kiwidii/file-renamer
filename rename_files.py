#!/usr/bin/env python3
import os
import argparse
import re

def rename_files(directory , dry_run=True):
    # resolve and validate directory (default can be ".")
    directory = os.path.abspath(os.path.expanduser(directory))
    # directory = '/home/kiwidi/Dokumente/Temp/QR-Codes/1 Video von Katrin 8 Jahrbuch/56/'
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    # List all files in the directory (no subdirs)
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # sort by modification time (oldest first)
    files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)))

    # Define the new naming scheme (0-9 then A-Z)
    new_char = [str(i) for i in range(10)] + [chr(ord('A') + i) for i in range(26)]

    for i, filename in enumerate(files):
        root, ext = os.path.splitext(filename)      # keep extension in `ext`
        if len(new_char) > len(files):
            new_name = f"{new_char[i]}{ext}"
        else:
            new_name = f"{new_char[0]}{new_char[i]}{ext}"  # fallback prefix + ext

        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_name)
        if dry_run:
            print(f"[dry-run] Would rename: '{filename}' -> '{new_name}'")
        else:
            try:
                os.rename(src, dst)
                print(f"Renamed: '{filename}' -> '{new_name}'")
            except Exception as e:
                print(f"Error renaming '{filename}': {e}")

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