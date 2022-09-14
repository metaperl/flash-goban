# Flash Goban

Make Anki flashcards from (KaTrain) goban positions

![image](https://user-images.githubusercontent.com/21293/190183717-2f2839b6-0a28-49e0-b594-842c5b39da1f.png)


# How does it work?

1. Open up Anki (after proper installation, see below)
2. Open up Flash-Goban
3. Open up a game in KaTrain
5. Scroll through until you see a position where you could've done much better
6. alt-tab to Flash-Goban and click "make flashcard"
7. A flashcard is made where the front of the flashcard is the game position with no move analysis and the back of the flashcard is the game position with move analysis



# Installation

## Download and install the Anki flashcard software

https://apps.ankiweb.net/

### Download and install the Anki plugin Anki-connect

https://github.com/FooSoft/anki-connect#installation

BE AWARE: this opens up port 8765 on your local machine. I know of no security issues but CAVEAT EMPTOR.

## Clone this repo

## Install Python on your machine

# Usage

1. Open a shell
2. Startup the Anki flashcard software
3. Set your `PYTHONPATH` to `.`
4. change directory to the flash-goban cloned repo
5. type `python main.py` to start up Flash Goban
6. Review a game in KaTrain
7. When you see a position you want to remember, ALT-TAB to Flash-Goban and click "Make Flashcard". You alt-tab and click "make flashcard' when the screen is showing the analysis



# FAQ

## Why not make a chrome plugin for this?

It actually was impossible as I discuss in [the FAQ for OGS Buddy](https://github.com/metaperl/ogs-buddy#faq).

# Related Work

## OGS Buddy

Make Anki flashcards from Online-Go.com goban positions - https://github.com/metaperl/ogs-buddy
