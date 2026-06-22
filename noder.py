#!/usr/bin/env python
# {
# Purpose of this program:
# Converting package list into Obsidian-compatible .md files that are properly linked
# Strategy:
#   Retrieve information such as:
#       1. Package name
#       2. Description
#       3. Dependencies
#       4. Dependents
#   Then organize into a .md file that Obsidian can read and link with
#       e.g.

#   7zip.md
#   File archiver for extremely high compression
#
#   Requires:
#       [[sh]], [[libgcc]], [[libstdc++]], [[glibc]]
#   Required by:
#       [[goverlay]], [[lutris]], [[unityhub]]
# }
import os
import shutil
import subprocess

# set file names
# pacman -Qq
packagesFile = "paks.txt"
# pacman -Qi | grep 'Description'| sed 's/.*: //g'
descriptionFile = "desc.txt"
# pacman -Qi | grep 'Depends On'| sed 's/.*: //g'
dependenciesFile = "deps.txt"
# pacman -Qi | grep 'Required By'| sed 's/.*: //g'
dependentsFile = "for.txt"

outFolderPath = "./PackageList"

# open respective files
packages = open(packagesFile, "rt")
descriptions = open(descriptionFile, "rt")
dependencies = open(dependenciesFile, "rt")
dependents = open(dependentsFile, "rt")

try:
    os.mkdir(outFolderPath)
except FileExistsError:
    print("Error: Output folder already exists!")

# data holder
fileInfo = {
    "name":"",
    "description":"",
    "dependencies":"",
    "dependents":""
}

while True:
    # extract each file's data
    fileInfo["name"]=packages.readline().rstrip('\n')
    fileInfo["description"]=descriptions.readline().rstrip('\n')
    fileInfo["dependencies"]=dependencies.readline().rstrip('\n')
    fileInfo["dependents"]=dependents.readline().rstrip('\n')
    explicitInstall=subprocess.run(["pacman", "-Qqe",fileInfo["name"]]).returncode==0
    
    # surround packages with [[]] for formatting and separate with commas for neatness
    if fileInfo["dependencies"] != "None":
        dependenciesItemized = ", ".join(f"[[{pkg}]]" for pkg in fileInfo["dependencies"].split())
    if fileInfo["dependents"] != "None":
        dependentsItemized = ", ".join(f"[[{pkg}]]" for pkg in fileInfo["dependents"].split())

    with open(outFolderPath+'/'+fileInfo["name"]+'.md', "w", encoding="utf-8") as newFile:
        print("Created file for:", fileInfo["name"], "    E =", explicitInstall)
        newFile.writelines([
                '### '+fileInfo["description"],
                "\n\nRequires:\n",
                dependenciesItemized,
                "\nRequired by:\n",
                dependentsItemized
                ])

    if fileInfo["name"]=="":
        break

packages.close()
descriptions.close()
dependencies.close()
dependents.close()
