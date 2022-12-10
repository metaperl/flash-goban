# importing webdriver from selenium

import os
import os.path
import random
import sys
import tempfile
import time
from pathlib import Path

import pyautogui
import pymsgbox
import pyperclip
from loguru import logger
from traitlets import HasTraits, default
from traitlets.config import Application

import flash_goban.anki_connect

pyautogui.PAUSE = 0.2

SOUND_EFFECTS = True
DECK_NAME = 'flash-goban'
TEMP_DIR = Path(tempfile.mkdtemp(prefix='flashcard-images'))
SECONDS_FOR_COMPLETION_NOTIFICATION = 3

logger.debug(f"{TEMP_DIR=}")

sound_path = Path('sounds')
image_path = Path('images')


def notify_completion():
    import pymsgbox

    milliseconds = SECONDS_FOR_COMPLETION_NOTIFICATION * 1000

    pymsgbox.alert("""Flashcard created.
    
    You are now a step closer to 1 dan!
    
    Play. Review. Flash-goban. This is the path to shodan.
    
    Continue your study!
    """, timeout=milliseconds)


def play_reflect():
    if SOUND_EFFECTS:
        from playsound import playsound

        # sounds = """camera-shutter-click-01 camera-shutter-click-03
        #     camera-shutter-click-08 shutter-40453
        #     camera-shutter-pentax-k20d-38609
        #     analog-camera-shutter-96604
        #     """.split()
        sound = sound_path / '177872__jorickhoofd__heavy-gong.wav'
        playsound(str(sound))


def _playsound(filename):
    if SOUND_EFFECTS:
        from playsound import playsound
        sound = sound_path / filename
        playsound(str(sound))


def play_camera_sound():
    if SOUND_EFFECTS:
        from playsound import playsound

        sounds = """camera-shutter-click-01 camera-shutter-click-03
            camera-shutter-click-08 shutter-40453
            camera-shutter-pentax-k20d-38609
            analog-camera-shutter-96604
            """.split()
        sound = sound_path / (random.choice(sounds) + '.mp3')
        playsound(str(sound))


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


def take_screenshot(filename):
    pyautogui.screenshot(filename)
    play_camera_sound()


def perhaps_record_game_url(card):
    """Examine clipboard and potentially add it to the flashcard.

    If the clipboard text looks like a game URL, then ask the user if he wants it on the front/back of the card
    (so you can go download the game and review it).
    """

    clipboard_text = pyperclip.paste()
    logger.debug(f"clipboard text={clipboard_text}")
    if clipboard_text.startswith('http'):
        confirm_message = f"""Should the flashcard indicate that
        this game position came from {clipboard_text}?"""
        response = pymsgbox.confirm(text=confirm_message, buttons='yes no abort'.split())
        if response == 'yes':
            card['back']['text'] == clipboard_text
        if response == 'abort':
            sound_file = 'zapsplat_technology_cb_radio_male_says_abort_speaker_pov_57190.mp3'
            _playsound(sound_file)
            sys.exit(255)


class UserInterface(HasTraits):
    '''The user's desktop.'''

    def alt_tab(self):
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        time.sleep(0.2)
        pyautogui.keyUp('alt')

    def toggle_ai_by_key(self):
        # pressing 'e' does not work!
        # pyautogui.press('e')
        time.sleep(1)
        logger.debug("we are pressing 'e'")
        pyautogui.press('e')
        logger.debug("we pressed 'e'!")

    def toggle_ai(self):

        file_name = 'top-moves.png'
        top_moves = image_path / file_name
        x, y = pyautogui.locateCenterOnScreen(str(top_moves), confidence=0.75)
        logger.debug(f"located top moves at {x},{y}")

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

        perhaps_record_game_url(card)

        for i, side in enumerate("front back".split()):
            tmp_name = f'{side}.png'
            _ = TEMP_DIR / tmp_name
            card[side]['image'] = _

            logger.debug(_)
            take_screenshot(_)
            self.toggle_ai()
            # self.toggle_ai_by_key()

        try:
            os.sync()
        except AttributeError:
            pass

        logger.debug(f"The extracted and generated {card=}   ")

        flash_goban.anki_connect.make_card(
            DECK_NAME,
            card['front']['text'],
            card['back']['text'],
            card['front']['image'],
            card['back']['image']
        )

        notify_completion()
        play_reflect()


class FlashGoban(Application):
    """Tool that makes a flashcard of a Go position in KaTrain."""

    ui = UserInterface()

    def start(self):
        self.ui.create_deck()
        self.ui.alt_tab()
        self.ui.make_flashcard()


def cli() -> None:
    FlashGoban.launch_instance()


if __name__ == '__main__':
    cli()
