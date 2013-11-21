"""
gamedata.py - This is general data about the game (score, money, etc)
that is passed to the UI.
"""

"""
Default values for resources and number of lives.
"""
STARTING_RESOURCES = 200
STARTING_LIVES = 20

class GameData:

    """
    Constructor that initializes scores to their default values.
    """
    def __init__(self):
        self.score = 0
        self.resources = STARTING_RESOURCES
        self.lives = STARTING_LIVES
	self.mapNumber = 1
        
