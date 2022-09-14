# importing webdriver from selenium
from lib2to3.pgen2 import driver
from weakref import finalize
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import tempfile

import os.path
import sys
import traceback

import time
from loguru import logger
import ogs_buddy.anki_connect


# Here Chrome will be used
from autoselenium import Driver

from traitlets import HasTraits, Int, Unicode, default, Any    
from traitlets.config import Application
from pathlib import Path

import PySimpleGUI as sg


DECK_NAME = 'ogs-buddy'
TEMP_DIR = tempfile.mkdtemp()

def move_upper_right(window):
    screen_width, screen_height = window.get_screen_dimensions()
    win_width, win_height = window.size
    x, y = (screen_width - win_width), 0
    window.move(x, y)


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

    @default('user_data'):
    def _user_dir(self):
        _ = self.home / ("." + DECK_NAME)
        _.mkdir(exist_ok=True)
        return _



class BrowserWindow(HasTraits):
    """Web browser window controlled by this application through Selenium."""

    driver = Any()
    url = Unicode("https://online-go.com/game/46749656")

    def begin(self):
            self.driver.get(self.url)
            self.remove_ogs_logo()
            logger.info("The Anki app must be up and running with anki-connect plugin for OGS Buddy to work its magic.")
            self.create_deck()


    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def remove_ogs_logo(self):
        elem = self.driver.find_element(By.CLASS_NAME, 'ogs-nav-logo')
        self.driver.execute_script("""
var element = arguments[0];
element.parentNode.removeChild(element);
""", elem)

    def toggle_ai(self):
        actions = self.action_chains
        actions.send_keys('I')
        actions.perform()

    def create_deck(self):
        try:
            ogs_buddy.anki_connect.create_deck(DECK_NAME)
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
                'image': '?',
            },
            'back': {
                'text': '',
                 'image': '?',
            }
        }
        for side in "back front".split():
            current_url=self.driver.current_url
            logger.debug(f"{current_url=}")
            _ = os.path.join(TEMP_DIR, filename_from_url(self.driver.current_url, append=f"{side}.png"))
            card[side]['image'] = _
            if side == 'back':
                card[side]['text'] = f'<a href="{self.driver.current_url}">{self.driver.current_url}</a>'
            logger.debug(_)
            self.driver.save_screenshot(_)
            self.toggle_ai()


        logger.debug(f"The extracted and generated {card=}   ")

        ogs_buddy.anki_connect.make_card(
            DECK_NAME,
            card['front']['text'],
            card['back']['text'],
            card['front']['image'],
            card['back']['image']
        )

    def move_next_to_browser(self, window):
        window_size = self.driver.get_window_size()
        logger.debug(f"{window_size=}")
        window.move(window_size['width'], 300)


class GUI(HasTraits):
    """User interface to faciliate interacting with the BrowserWindow."""

    browser_window = BrowserWindow()

    def gui_loop(self):
        sg.theme('DarkAmber')   # Add a touch of color
        # All the stuff inside your window.
        layout = [ 
                    [sg.Text(' ' * 60)],
                    [sg.Button('BookmarkAsHome')],
                    [sg.Text(' ' * 60)],
                    [sg.Button('MakeFlashCard'), sg.Button('Exit')],
                    [sg.Text('')]
                    ]

        # Create the Window
        window = sg.Window('OGS BUDDY', layout, finalize=True)

        # Move this GUI next to the browser window
        self.browser_window.move_next_to_browser(window)

        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            print(f'{event} entered ', values)

            if event == 'MakeFlashCard': # if user closes window or clicks cancel
                self.browser_window.make_flashcard()
            if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
                break

        window.close()

             

class OGSBuddy(Application):
    """Tool that opens a BrowserWindow that a user controls via a GUI."""

    browser_window = BrowserWindow()
    gui = GUI()

    def start(self):
        with Driver('chrome') as driver:
            self.gui.browser_window = self.browser_window
            self.browser_window.driver = driver
            self.browser_window.begin()
            self.gui.gui_loop()

if __name__ == '__main__':
    OGSBuddy.launch_instance()
    
