# importing webdriver from selenium
from lib2to3.pgen2 import driver
from weakref import finalize


import tempfile

import os
import os.path
import sys
import traceback

import time
from loguru import logger
import flash_goban.anki_connect

import random

from traitlets import HasTraits, Int, Unicode, default, Any    
from traitlets.config import Application
from pathlib import Path

import pyautogui
pyautogui.PAUSE = 0.2


SOUND_EFFECTS = True
DECK_NAME = 'flash-goban'
TEMP_DIR = Path(tempfile.mkdtemp(prefix='flashcard-images'))

logger.debug(f"{TEMP_DIR=}")


def play_reflect():
    if SOUND_EFFECTS:
        from playsound import playsound

        # sounds = """camera-shutter-click-01 camera-shutter-click-03
        #     camera-shutter-click-08 shutter-40453
        #     camera-shutter-pentax-k20d-38609
        #     analog-camera-shutter-96604
        #     """.split()
        sound = 'angel-reveal.wav'
        playsound(sound)
        time.sleep(5)

def play_camera_sound():
    if SOUND_EFFECTS:
        from playsound import playsound

        sounds = """camera-shutter-click-01 camera-shutter-click-03
            camera-shutter-click-08 shutter-40453
            camera-shutter-pentax-k20d-38609
            analog-camera-shutter-96604
            """.split()
        sound = random.choice(sounds) + '.mp3'
        playsound(sound)
        time.sleep(1)

def filename_from_url(url, append=None):
    parts = url.split("/")
    logger.debug(f"{parts=}")
    game_number = parts[-1]
    # import datetime module
    from datetime import datetime

    # consider date in string format
    my_date = datetime.now()

    # convert datetime format into %Y-%m-%d-%H:%M:%S
    # format using strftime
    filename = "{}-{}".format(
        game_number,
        my_date.strftime("%Y-%m-%d-%H-%M-%S"))

    if append:
        filename += f"-{append}"

    return filename

class UserData(HasTraits):

    home = Path(Path.home())
    user_dir = Path()

    @default('user_dir')    
    def _user_dir(self):
        _ = self.home / ("." + DECK_NAME)
        _.mkdir(exist_ok=True)
        return _

class UserInterface(HasTraits):
    '''The user's desktop.'''


    def alt_tab(self):
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        time.sleep(0.2)
        pyautogui.keyUp('alt')

    def toggle_ai(self):
        # pressing 'e' does not work!
        # pyautogui.press('e')
        x, y = pyautogui.locateCenterOnScreen('top-moves.png', confidence=0.75)
        # logger.debug(f"located top moves at {top_left=}")

        pyautogui.click(x, y)

    def create_deck(self):
        try:
            flash_goban.anki_connect.create_deck(DECK_NAME)
        except Exception as e:
            logger.exception(f"""
                Could not create or connect to Anki software:
                1. Is the Anki flashcard software running?
                2. Have you installed the Anki-connect Flashcard plugin?

                """
            )
            sys.exit()



    def take_screenshot(self, filename):

        pyautogui.screenshot(filename)
        play_camera_sound()
        

    def make_flashcard(self):
        card = {
            'front': {
                'text': '?',
                'image': '',
            },
            'back': {
                'text': '? ',
                 'image': '',
            }
        }

        for side in "front back".split():

            if side == 'back':
                play_reflect()

            tmp_name = f'{side}.png'
            _ = TEMP_DIR / tmp_name
            card[side]['image'] = _
 
            logger.debug(_)
            self.take_screenshot(_)
            self.toggle_ai()

        try:
            os.sync()
        except AttributeError:
            time.sleep(2)

        logger.debug(f"The extracted and generated {card=}   ")

        flash_goban.anki_connect.make_card(
            DECK_NAME,
            card['front']['text'],
            card['back']['text'],
            card['front']['image'],
            card['back']['image']
        )
             

class FlashGoban(Application):
    """Tool that makes a flashcard of a Go position in KaTrain."""

    ui = UserInterface()

    def start(self):
        self.ui.create_deck()
        self.ui.alt_tab()
        self.ui.make_flashcard()
        self.ui.alt_tab()

 

if __name__ == '__main__':
    FlashGoban.launch_instance()
    
