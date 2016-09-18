# LyricChecker
A Python GUI application that implements Tkinter to display the number of "expletives" in each song of an album. This list was compiled by Google for a previous project.

This script is still currently in testing stages, so though it is fully functional, it may still have problems and revisions necessary. The GUI is brand new and is expected to have some fixing/improvements to be made, but appears to be fully functional as well.

# Usage

For macOS:
- Open Terminal
- Browse to the [directory-name]/dist
- Run LyricChecker.app

For Windows:
- Ensure Python is installed on your machine. Automated install may be added in the future. Python can be installed from https://www.python.org/downloads/
- Run 'dir [path-to-directory]' in a Console window
- Run 'py main.py' in the same Console window

For Linux:
- Instructions need to be added

# Usage Warning
This script rips off of AZLyrics in order to read lyrics. AZLyrics has measures in place to blacklist your IP address for a good amount of time if you submit too many failed URL requests in a certain amount of time.
This given, caution should be used while both testing and using this software; if the program does not find lyrics for your desired album, ***there is a parsing error: do not attempt more than once without code revision.***
I am not responsible for the misuse of this script by any people, though my intent is to prevent this problem from happening in the first place.

# Ideas
- Catch for artist title parsing error for AZLyrics
- Better interface (Tkinter has been implemented - further work needed?)
- Windows executable application (py2exe support)
- Mobile/web integration?
