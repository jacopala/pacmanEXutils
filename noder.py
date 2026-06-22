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
    os.makedirs(outFolderPath, exist_ok=True)
except FileExistsError:
    print("Error: Output folder already exists!")
else:
    # data holder
    pkgInfo = {
        "name":"",
        "description":"",
        "dependencies":"",
        "dependents":""
    }

    while True:
        # extract each file's data
        pkgInfo["name"]=packages.readline().rstrip('\n')
        pkgInfo["description"]=descriptions.readline().rstrip('\n')
        pkgInfo["dependencies"]=dependencies.readline().rstrip('\n')
        pkgInfo["dependents"]=dependents.readline().rstrip('\n')

        if pkgInfo["name"]=="":
            break
        
        explicitInstall=subprocess.run(["pacman", "-Qqe", pkgInfo["name"]], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
        
        # surround packages with [[]] for formatting and separate with commas for neatness
        if pkgInfo["dependencies"] != "None":
            dependenciesItemized = ", ".join(f"[[{pkg}]]" for pkg in pkgInfo["dependencies"].split())
        if pkgInfo["dependents"] != "None":
            dependentsItemized = ", ".join(f"[[{pkg}]]" for pkg in pkgInfo["dependents"].split())

        with open(outFolderPath+'/'+pkgInfo["name"]+'.md', "w", encoding="utf-8") as newFile:
            print("Created:", pkgInfo["name"], "    E =", explicitInstall)
            newFile.writelines([
                    '### '+pkgInfo["description"],
                    "\n\nRequires:\n",
                    dependenciesItemized,
                    "\nRequired by:\n",
                    dependentsItemized,
                    "\n#explicitInstall" if explicitInstall else "\n#depInstall"
                    ])
finally:
    packages.close()
    descriptions.close()
    dependencies.close()
    dependents.close()
