pacman utilities written in Python

noder.py:
uses the output of "pacman -Qi" to extract information about each package, then converts them into markdown(.md) files compatible with Obsidian's format to allow the cool visual linking between dependencies

Included in each file:
Description, Dependencies/dependents (in double brackets), and a tag for explicit installations/dep installations
