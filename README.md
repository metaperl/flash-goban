# Flash Goban
*The poor man's AI Sensei*

Make Anki flashcards from (KaTrain) goban positions. 


![flash-goban4](https://user-images.githubusercontent.com/21293/190810634-b885e3a0-af1a-44e9-a2b1-f1018db7dc90.png)


# How does it work?

Here is a video example - 
https://www.youtube.com/watch?v=RrvmPVQRJPo

We will go into detail in the "Usage" section. For now, let's just say:

1. Play a game
2. Download the SGF
3. Open up the SGF in KaTrain
4. Find a position where you could improve
5. Make a flashcard of the position
6. Review your flashcards on a regular basis to improve.

## A little more detail about taking the flashcards

Originally, this application made the flashcard for the front and back
automatically. However, [issues began to surface](https://github.com/metaperl/flash-goban/issues/1) 
with pressing "Top Moves" in the KaTrain user interface. Therefore, even
though flash-goban automatically makes the front of the flashcard, you
(currently) must select "Top Moves" by clicking or pressing `e` manually.

Thus, as of [this commit](https://github.com/metaperl/flash-goban/commit/fbaa1055f391fa834e926708fc80f25f3edab7d8)
we are now manually making the flashcard for the back.

# Installation

## Download and install the Anki flashcard software

https://apps.ankiweb.net/

### Download and install the Anki plugin Anki-connect

https://github.com/FooSoft/anki-connect#installation

BE AWARE: this opens up port 8765 on your local machine. I know of no security issues but CAVEAT EMPTOR.

## Clone this repo

https://github.com/metaperl/flash-goban

## Install Python on your machine

On Windows, I prefer to use [Python from the Python software foundation](https://www.python.org/). 
I had a brief run with Python from the Windows store as well as Chocolatey but neither worked so well.

### Then install poetry and deps

    shell> pip install poetry
    shell> poetry install
    shell> poetry shell
    
Then you can type `python main.py` to invoke the program. The program will then alt-tab to KaTrain
and make a screenshot. Then it will click "top moves" and make another screenshot and then make a 
flashcard.

You **MUST** have Anki up with Anki-connect for flashcards to 
work.

## Sound Effects

you may not be able to get the camera sound effects (made when taking screenshots) to work on your platform.

if so, set  `SOUND_EFFECTS` to `False` in `flash_goban/settings.py` to turn them off. 

## Configure the program

You may or may not want to customize the execution of Flash-Goban in 
`flash_goban/settings.py`.

## Optional: build an executable

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
5. Type `poetry shell`
5. Review a game in KaTrain, optionally copying the URL of the game to the clipboard
(it will be added to the back of the card so that you can find the game later.)
6. (in default mode) When you see a position you want to remember, ALT-TAB to Flash-Goban and invoke it... flash-goban will take a picture
without analysis and with analysis **and add the URL on the clipboard to the back of the card.**


# Developer Guide

May the source be with you.

# FAQ

## Why not make a chrome plugin for this?

It actually was impossible as I discuss in [the FAQ for OGS Buddy](https://github.com/metaperl/ogs-buddy#faq).

# Related Work

## OGS Buddy

Make Anki flashcards from Online-Go.com goban positions - https://github.com/metaperl/ogs-buddy

# Acknowledgements

"Abort sound" came from Zapsplat.com

# Contact

Email terrence.brannon@gmail.com

