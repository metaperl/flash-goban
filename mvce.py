"""This program ALT-TABs to the KaTrain application. It then:
1. Takes a screenshot of the screen as it is.
2. presses the key 'e' so that KaTrain shows the top moves.
3. Takes a screenshot of the screen with the top moves.

BUG: step '2' above does not work. Even though the script successfully
alt-tabs, it does not successfully get KaTrain to detect that 'e' has
been pressed, even though it should.

USAGE: open up KaTrain, then alt-tab to your console. Then type python main.py

INSTALL: `pip install pyautogui pymsgbox pendulum pydirectinput`
"""

import time
import uuid

import pyautogui
import pymsgbox
import pendulum
import pydirectinput

pyautogui.PAUSE = 0.2


def toggle_ai_by_key():
    # pressing 'e' does not work!
    # pyautogui.press('e')
    time.sleep(1)
    # pyautogui.press('e')
    pydirectinput.press('e')


def alt_tab():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    time.sleep(0.2)
    pyautogui.keyUp('alt')


def main():
    alt_tab()
    prefix = pendulum.now().to_time_string().replace(':', '-')
    for i, side in enumerate("front back".split()):
        tmp_name = f'{prefix}-{side}.png'
        pyautogui.screenshot(tmp_name)
        toggle_ai_by_key()
    pymsgbox.alert(f"screenshots taken with prefix {prefix}")


if __name__ == '__main__':
    main()
