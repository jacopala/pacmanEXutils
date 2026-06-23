pacman utilities written in Python

flnode.py:
uses output of "pacman -Qi" to extract information about packages to form markdown(.md) files to be used with Obsidian to create package databases

noder.py: [deprecated]
original version of flnode that uses generated .txt files

Included in each file:
Description, Dependencies/dependents (in double brackets), and a tag for explicit installations/dep installations
