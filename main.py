import os
import os.path
import platform
import random
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
import flash_goban.settings as cfg

pyautogui.PAUSE = 0.1

SOUND_EFFECTS = cfg.SOUND_EFFECTS
DECK_NAME = 'flash-goban'
TEMP_DIR = Path(tempfile.mkdtemp(prefix='flashcard-images'))


def seconds_to_milliseconds(s):
    return s * 1000


SECONDS_FOR_COMPLETION_NOTIFICATION = seconds_to_milliseconds(cfg.SECONDS_FOR_COMPLETION_NOTIFICATION)

logger.debug(f"{TEMP_DIR=}")

sound_path = Path('sounds')
image_path = Path('images')

GAME_URL = None


def notify_completion():
    pymsgbox.alert(f"""Flashcard created. Game URL recorded as {GAME_URL})
        
    Play. Review. Flash-goban. This is the path to shodan.
    
    Continue your study!
    """, timeout=SECONDS_FOR_COMPLETION_NOTIFICATION)


def press_top_moves_prompt():
    if not GAME_URL:
        game_url_message = \
            """There is no game URL currently on clipboard. You may copy the game url to the clipboard now."""
    else:
        game_url_message = \
            f"""Current game URL on clipboard is {GAME_URL}. If this is not correct, go ahead and copy the 
            correct one to the clipboard"""

    if cfg.MANUAL_SELECT_TOP_MOVES:
        select_top_moves_message = "Go ahead and select top moves. I guess you like working hard."
    else:
        select_top_moves_message = \
            "Make sure that the top moves are now highlighted. I tried my hardest to do it for you."

    pymsgbox.alert(f"""Front flashcard created. Now:
    
    1. {game_url_message}
    2. {select_top_moves_message}
    3. Once the screen looks like what you want on the back of the flashcard (i.e. KaTrain is showing top moves), 
    you may press 'OK' to continue, or meditate on the top move 
    until the max 30 second delay is over.
    """, timeout=seconds_to_milliseconds(30))


def play_reflect():
    if SOUND_EFFECTS:
        from playsound import playsound

        sounds = """
        108167__robinhood76__02111-screamy-applause.wav
        277021__sandermotions__applause-2.wav
        403057__vesperia94__hooray.wav
        220691__pep_molina__woohoo.mp3
        557126__melisandepope__manlyvoicealright.wav
        368841__skyraevoicing__alright-we-did-it-female-cheer-for-games.mp3
        46941__erh__i-s-alright-folks-f.wav
        565888__dundalkkirk__announcer-win.wav
        37215__simon_lacelle__ba-da-dum.wav
        672707__bugradio__correct-winner.wav
        """

        play_random_sound(sounds)


def _playsound(filename):
    if SOUND_EFFECTS:
        from playsound import playsound
        sound = sound_path / filename
        playsound(str(sound))

def play_random_sound(sounds):
    if SOUND_EFFECTS:
        from playsound import playsound

        sounds = sounds.split()

        sound = sound_path / (random.choice(sounds))
        logger.debug(f"Playing sound {sound}")
        playsound(str(sound))

def play_camera_sound():
    if SOUND_EFFECTS:
        from playsound import playsound

        sounds = """
        camera-shutter-click-01.mp3 
        camera-shutter-click-03.mp3
        camera-shutter-click-08.mp3
        shutter-40453.mp3
        camera-shutter-pentax-k20d-38609.mp3
        analog-camera-shutter-96604.mp3
        13658__ls__camera-click.mp3
        541760__philliparthur__camera-mirror-flip-down.wav
        541759__philliparthur__camera-mirror-flip-up.wav
        13659__ls__camera2.mp3
        656026__jacko4526__vintage-camera-shutter-firing.wav
        64448__nicstage__cameraopen.wav
        165689__paultjuh1984__powershot-g10-camera-on-open.wav
        """

        play_random_sound(sounds)


def alt_tab():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    time.sleep(0.2)
    pyautogui.keyUp('alt')


def press_letter_e():
    """Pressing the letter 'e' toggles 'Top Moves' in the KaTrain UI"""
    # pressing 'e' does not work!
    # pyautogui.press('e')
    logger.debug("we are pressing 'e'")

    if platform.system() == 'Windows':
        import pydirectinput
        pydirectinput.press('e')
    else:
        pyautogui.press('e')

    logger.debug("we pressed 'e'!")


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

    global GAME_URL

    clipboard_text = pyperclip.paste()
    logger.debug(f"clipboard text={clipboard_text}")
    if clipboard_text.startswith('http'):
        GAME_URL = clipboard_text
        card['back']['text'] = GAME_URL


class UserInterface(HasTraits):
    """The user's desktop."""

    def toggle_ai(self):

        file_name = 'top-moves.png'
        top_moves = image_path / file_name
        x, y = pyautogui.locateCenterOnScreen(str(top_moves), confidence=0.75)
        logger.debug(f"toggling AI: located top moves at {x},{y}")

        pyautogui.click(x, y)

    def create_deck(self):
        try:
            flash_goban.anki_connect.create_deck(DECK_NAME)
        except Exception:
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

        for i, side in enumerate("front back".split()):
            tmp_name = f'{side}.png'
            _ = TEMP_DIR / tmp_name
            card[side]['image'] = _

            logger.debug(_)
            take_screenshot(_)

            # If we just took the screenshot of the front, we now take the screenshot of the back
            # manually or automatically based on the configuration setting:
            if side == 'front':
                perhaps_record_game_url(card)

                if not cfg.MANUAL_SELECT_TOP_MOVES or not cfg.MANUAL_BACK_OF_CARD:
                    press_letter_e()

                if cfg.MANUAL_BACK_OF_CARD:
                    press_top_moves_prompt()
                    perhaps_record_game_url(card)

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
        alt_tab()
        self.ui.make_flashcard()


def cli() -> None:
    FlashGoban.launch_instance()


if __name__ == '__main__':
    cli()
