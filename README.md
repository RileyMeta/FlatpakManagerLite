# Flatpak Manager Lite
### An extremely light, Python-only, front-end for Flatpak
After a recent escapade into Slackware I thought it would be fun to get Flatpak working, which wasn't difficult. The annoying part came when I tried to compile Gnome-Software, KDE-Discover and a few others just to find out they either required SystemD, or had far too many dependancies for me to feel safe. Not to mention the amount of time it took compiling just to find out it needed something I couldn't get. So I decided to make a simple front-end in Python. 

> This whole project is a single file. 
![image](https://github.com/RileyMeta/FlatpakManagerLite/assets/32332593/950d8fed-e1c3-471b-8e22-ba863564f17a)

## What this app can do
- Pull the current list of available apps from Flathub
- Display in list-form all of the apps, including
- - Their Icon
- - Their Name
- - Their Description
- - Flatpak ID (used only for (un)installing/upgrades)
- A Search bar to find specific packages
- An auto-Install button
- An auto-Uninstall button
- An auto-Update button
- An *unfinished toggle for Default and Alpha-numeric sorting

## Requirements / Dependancies
- Python3
- PyQT5
- requests (Python Module)

## Included Binary
The included Binary was created with [Pyinstaller](https://pyinstaller.org/en/stable/)

## Known Issues: 
- It takes a while to load (This is an issue with GTK, I haven't tried to fix it yet)
- Switching back to Sort by Name does nothing.
- You can't cancel anything once it's started (unless you close the app)

> If you open the front-end via a terminal you can watch the flatpak commands at work. 
