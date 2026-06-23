#!/usr/bin/env python
# File-Less version that uses subprocess instead of relying on pre-made .txt files
import os
import subprocess

outFolderPath = "./PackageList/"

# collect full output of 'pacman -Qi'
qiOutput = subprocess.run(
        "pacman -Qi",
        shell=True,
        capture_output=True,
        text=True
        ).stdout.strip().splitlines()

# store select lines to dict for each package, and append each dict to an array
pkg = {}
pkgs = []

for line in qiOutput:
    if line.startswith("Name"):
        pkg["name"]         = line[line.find(": ")+2:]
    elif line.startswith("Description"):
        pkg["description"]  = line[line.find(": ")+2:]
    elif line.startswith("Depends On"):
        pkg["dependencies"] = line[line.find(": ")+2:]
    elif line.startswith("Required By"):
        pkg["dependents"]   = line[line.find(": ")+2:]
    elif line.startswith("Install Reason"):
        pkg["explicit"]     = line[line.find(": ")+2:]=="Explicitly installed"
    if len(pkg)==5:
        pkgs.append(pkg)
        pkg = {}

os.makedirs(outFolderPath, exist_ok=True)

for pkg in pkgs:
    newFilePath = outFolderPath+pkg["name"]+".md"
    with open(newFilePath, "w", encoding="utf-8") as newFile:
        print("Creating:", pkg["name"])
        newFile.writelines([
            '### '+pkg["description"]+'\n',
            "Notes:\n",
            "\n\n\n",
            "## Dependencies\n",
            ", ".join(f"[[{dep}]]" for dep in pkg["dependencies"].split())+'\n',
            "## Required By\n",
            ", ".join(f"[[{dep}]]" for dep in pkg["dependents"].split())+'\n',
            "#explicit" if pkg["explicit"] else "#dependency"
            ])
