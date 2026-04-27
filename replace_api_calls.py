import os
import glob
import re

directory = "/home/dpl_moises/knowflow/Frontend/KnowFlow/src/pages/"
files = glob.glob(os.path.join(directory, "*.vue"))

for filepath in files:
    with open(filepath, "r") as f:
        content = f.read()
    
    new_content = re.sub(r"api\.get\('/", "api.get('", content)
    new_content = re.sub(r"api\.post\('/", "api.post('", new_content)
    new_content = re.sub(r"api\.put\('/", "api.put('", new_content)
    new_content = re.sub(r"api\.delete\('/", "api.delete('", new_content)
    new_content = re.sub(r"api\.patch\('/", "api.patch('", new_content)
    
    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        print(f"Updated {filepath}")

print("Done.")
