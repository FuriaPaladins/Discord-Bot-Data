import os

## Search in this directory and all subdirectories for files with "'", and replace them with ""
for root, dirs, files in os.walk("."):
    for file in files:
        if "'" in file:
            os.rename(os.path.join(root, file), os.path.join(root, file.replace("'", '')))
            print(f"""Renaming {file} to {file.replace("'", '')}""")
