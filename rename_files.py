import os

def rename_files(directory):
    # List all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()  # Sort files alphabetically

    # Define the new naming scheme
    prefixes = list(range(10)) + [chr(ord('A') + i) for i in range(26)]

    for i, filename in enumerate(files):
        if i < len(prefixes):
            new_name = f"{prefixes[i]}_{filename}"
            os.rename(
                os.path.join(directory, filename),
                os.path.join(directory, new_name)
            )
            print(f"Renamed '{filename}' to '{new_name}'")

if __name__ == "__main__":
    # Replace with the path to your Samba-mounted directory
    target_directory = "/path/to/your/samba/mount"
    rename_files(target_directory)
