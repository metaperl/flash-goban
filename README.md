# Flash Goban

Make Anki flashcards from (KaTrain) goban positions

![flash-goban4](https://user-images.githubusercontent.com/21293/190810634-b885e3a0-af1a-44e9-a2b1-f1018db7dc90.png)


# How does it work?

here is a video example - 
https://youtu.be/4B0VT44Aof4

1. Open up Anki (after proper installation, see below)
1. Open up a game in KaTrain
1. Scroll through until you see a position where you could've done much better
1. invoke Flash-Goban 
1. A flashcard is made where the front of the flashcard is the game position with no move analysis and the back of the flashcard is the game position with move analysis


# Installation

## Download and install the Anki flashcard software

https://apps.ankiweb.net/

### Download and install the Anki plugin Anki-connect

https://github.com/FooSoft/anki-connect#installation

BE AWARE: this opens up port 8765 on your local machine. I know of no security issues but CAVEAT EMPTOR.

## Clone this repo

## Install Python on your machine

On Windows, I prefer to use Python from the Microsoft store.

## Sound Effects

you may not be able to get the camera sound effects (made when taking screenshots) to work on your platform.

if so, set  `SOUND_EFFECTS` to `False` to turn them off. 

# Optional: build an executable

you may get tired of opening up a command shell, cd'ing to the repo and then invoking `python main.py` all the time.

in this case, you can create an executable as follows:

    pip install pyinstaller
    pyinstaller make-exe.spec

Then you will find an executable in `$repo/dist/main` that you can put a shortcut on your desktop to so that you can invoke in one-click.

Because flash-goban finds the kaTrain window by using Alt-TAB, just make sure to have the katrain window up when you click on the icon for your executable.

here is a video of using the executable: https://youtu.be/tr42FXu1pe8

# Usage

1. Set your `PYTHONPATH` to `.`. Ideally you would do this in your environment settings once.
2. Startup the Anki flashcard software
3. Open up a shell
4. change directory to the flash-goban cloned repo
5. Review a game in KaTrain
5. When you see a position you want to remember, ALT-TAB to Flash-Goban and click "Make Flashcard". You alt-tab and click "make flashcard' when the screen is showing the analysis
6. type `python main.py` to start up Flash Goban




# FAQ

## Why not make a chrome plugin for this?

It actually was impossible as I discuss in [the FAQ for OGS Buddy](https://github.com/metaperl/ogs-buddy#faq).

# Related Work

## OGS Buddy

Make Anki flashcards from Online-Go.com goban positions - https://github.com/metaperl/ogs-buddy
