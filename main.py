# importing webdriver from selenium
from lib2to3.pgen2 import driver
from weakref import finalize


import tempfile

import os.path
import sys
import traceback

import time
from loguru import logger
import flash_goban.anki_connect



from traitlets import HasTraits, Int, Unicode, default, Any    
from traitlets.config import Application
from pathlib import Path

import pyautogui
pyautogui.PAUSE = 0.2


DECK_NAME = 'flash-goban'
TEMP_DIR = tempfile.mkdtemp(prefix='flashcard-images', dir='.')
logger.debug(f"{TEMP_DIR=}")


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

    screenshot_count = Int()

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

            tmp_name = f'{self.screenshot_count}-{side}.png'
            self.screenshot_count += 1
            _ = os.path.join(TEMP_DIR, tmp_name)
            card[side]['image'] = _
 
            logger.debug(_)
            pyautogui.screenshot(_)
            self.toggle_ai()


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
    
