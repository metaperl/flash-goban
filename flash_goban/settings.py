"""
Settings to configure the behavior of Flash Goban
"""

# Should we make sound effects when taking screenshots and
# indicating that a flashcard has been made?
# If it doesnt work on your platform, then set to False
SOUND_EFFECTS = True

# After a flashcard is created, a cute little window pops up
# notifying you of this. The window closes after N seconds,
# where N is the number below
SECONDS_FOR_COMPLETION_NOTIFICATION = 2

# The back of the flashcard contains
# (1) a screenshot of the game position with top moves
# (2) [optional] a URL to the game the position came from

# If you set MANUAL_BACK_OF_CARD to False, then:
# 1 - the screenshot will be taken of the back automatically
# and pressing 'e' to select Top Moves may or may not work
# as discussed here - https://github.com/metaperl/flash-goban/issues/1
# 2 - you have an option to copy the game-url to the clipboard

# If you set MANUAL_BACK_OF_CARD to True then:
# 1 - You get prompted for copying the game Url to the clipboard
# 2 - You may or may not be prompted to select Top Moves based on
# the value of AUTOMATICALLY_SELECT_TOP_MOVES

# The default settings are what I like:
# I get prompted to copy the game-url to the back of the flashcard
# I dont have to fuss with selecting top moves manually.

MANUAL_BACK_OF_CARD = True
MANUAL_SELECT_TOP_MOVES = False
