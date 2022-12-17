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
SECONDS_FOR_COMPLETION_NOTIFICATION = 1


# Creating the back of the flashcard requires selecting "Top Moves"
# from the KaTrain UI either via image recognition or by pressing the
# letter 'e'. Both of these have proven problematic on Windows as
# discussed here - https://github.com/metaperl/flash-goban/issues/1
# and I dont know the status of other platforms because I dont have them.

# There is a fix for Windows to allow automatic pressing of the letter 'e'
# in a robust fashion, but I dont recommend it because then you dont get
# the benefits of manual flashcard creation which are:
# 1. you get reminded to copy the URL of the game you are watching to the clipboard
# so you have a record of where the position came from
# 2. You dont get a brief period to stare at the right answer as a form of memory improvement

# That being said, manual flashcard creation is a PITA with a bunch of going here and
# going there that you may not want to do. If you want to avoid the PITA, set to False

MANUAL_BACK_OF_CARD = True