import sys
import traceback
import signal


from kivymd.app import MDApp

from katrain.core.constants import (
    OUTPUT_ERROR,
    OUTPUT_KATAGO_STDERR,
    OUTPUT_INFO,
    OUTPUT_DEBUG,
    OUTPUT_EXTRA_DEBUG,
    MODE_ANALYZE,
    HOMEPAGE,
    VERSION,
    STATUS_ERROR,
    STATUS_INFO,
    PLAYING_NORMAL,
    PLAYER_HUMAN,
    SGF_INTERNAL_COMMENTS_MARKER,
    MODE_PLAY,
    DATA_FOLDER,
    AI_DEFAULT,
)

from kivy.base import ExceptionHandler, ExceptionManager


#sys.path.append("c:\code\katrain")

print(sys.path)
# from katrain.__main__ import run_app

print(f"{sys.argv=}")

sys.argv.append('game.sgf')

from katrain.__main__ import KaTrainApp


def run_app():
    class CrashHandler(ExceptionHandler):
        def handle_exception(self, inst):
            ex_type, ex, tb = sys.exc_info()
            trace = "".join(traceback.format_tb(tb))
            app = MDApp.get_running_app()

            if app and app.gui:
                app.gui.log(
                    f"Exception {inst.__class__.__name__}: {', '.join(repr(a) for a in inst.args)}\n{trace}",
                    OUTPUT_ERROR,
                )
            else:
                print(f"Exception {inst.__class__}: {inst.args}\n{trace}")
            return ExceptionManager.PASS

    ExceptionManager.add_handler(CrashHandler())
    app = KaTrainApp()
    signal.signal(signal.SIGINT, app.signal_handler)
    gui = app.build()
    return app, gui

app, gui = run_app()
print(f"{app=}, {gui=}")

gui.start()

import time
time.sleep(50)