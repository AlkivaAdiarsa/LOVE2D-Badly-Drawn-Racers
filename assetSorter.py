import json
import os

"""
how to use:
first do CD to the extracted folder, then run this script. It will read the sprite.json file, find the sounds list, and rename the files accordingly. Make sure to have a backup of your files before running the script, just in case something goes wrong.
"""

# 1. Load the mapping file
try:
    with open('sprite.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: 'sprite.json' not found. Make sure you are running this script inside the extracted folder.")
    exit()

# 2. Find the sounds list (it can be at the root or nested)
sounds = data.get('sounds', [])
images = data.get('images', [])

# 3. Rename files
renamed_count = 0

# Helper to rename from Scratch style entries
def rename_entry(entry, filename_key, name_key, ext_key, default_ext):
    global renamed_count
    old_name = entry.get(filename_key)
    original_name = entry.get(name_key)
    if not old_name or not original_name:
        return

    extension = entry.get(ext_key, default_ext)
    new_name = f"{original_name}.{extension}"

    if os.path.exists(old_name):
        try:
            os.rename(old_name, new_name)
            print(f"Renamed: {old_name} -> {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"Failed to rename {old_name}: {e}")
    else:
        print(f"File not found: {old_name} (Check if it's already renamed or in a subfolder)")

for sound in sounds:
    # Scratch 3 uses 'md5ext' for the filename and 'name' for the display name
    rename_entry(sound, 'md5ext', 'name', 'dataFormat', 'wav')

for image in images:
    # Scratch 3 uses 'md5ext' and 'name' for image assets too
    # Some project JSON has 'format' for image type
    rename_entry(image, 'md5ext', 'name', 'format', 'png')

print(f"\nFinished. Renamed {renamed_count} files.")
