# Flatpak Manager Lite
### An extremely light, Python-only, front-end for Flatpak
After a recent escapade into Slackware I thought it would be fun to get Flatpak working, which wasn't difficult. The annoying part came when I tried to compile Gnome-Software, KDE-Discover and a few others just to find out they either required SystemD, or had far too many dependancies for me to feel safe. Not to mention the amount of time it took compiling just to find out it needed something I couldn't get. So I decided to make a simple front-end in Python. 

> This whole project is a single file. 
![image](https://github.com/RileyMeta/FlatpakManagerLite/assets/32332593/6f68b8e1-0f9b-4cb8-8bba-a754f43144fe)


## What this app can do
- Pull the current list of available apps from Flathub
- Display in list-form all of the apps, including
- - Their Icon
- - Their Name
- - Their Description
- - Flatpak ID (used only for (un)installing/upgrades)
- A Search bar to find specific packages
- An *unfinished toggle for Default and Alpha-numeric sorting
- Auto-invocation of Flatpak Commands through Python Subprocesses
- - An auto-Install button
- - An auto-Uninstall button
- - An auto-Update button

## Build from Source

1. Make sure you have all the Requirements installed

1. Clone this Repo

1. cd into the directory 

1. make sure to run with python**3** 

```bash
git clone https://github.com/RileyMeta/FlatpakManagerLite
cd FlatpakManagerLite/
python3 FlatpakManagerLite.py
```

## Build Requirements
- Python3
- Pip
- - Pyqt5
- - requests (Python Module for Flathub API)
- - (optional) Pyinstall (for building Binaries)

## Run Requirements
- Python3
- PyQT5
- (Slackware) - python3-pyqt-distutils
- Flatpak

## Included Binary
The included Binary was created with [Pyinstaller](https://pyinstaller.org/en/stable/)

## Known Issues: 
- It takes a while to load (This is an issue with GTK, I haven't tried to fix it yet)
- Switching back to Sort by Name does nothing.
- You can't cancel anything once it's started (unless you close the app)
- Status Text in the bottom left doesn't update or clear
- App Freezes when installing larger apps (Parallelization is not enabled)

> If you open the front-end via a terminal you can watch the flatpak commands at work. 

## Goals: 
- [x] ~~Improve Loading Times (Impliment Lazy Loading)~~
- [ ] Fix Canberra-GTK-Module issues
- [ ] Add additional sorting options in the combobox
- [ ] Add a Cancel button
- [x] ~~Add a default time-out for status text to auto-clear~~
- [ ] Add a Status Bar for Installations?
- [ ] Add Parallelization for multiple simultaneous downloads? (Might not be possible)
- [x] ~~Improve Visual Design of App~~ (Darkmode Added)
