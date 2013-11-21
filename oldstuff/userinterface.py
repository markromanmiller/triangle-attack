"""
userinterface.py - Handles the game's user interface (UI) and draws it to the
screen.
"""

import os

"""
The size of the font to use in the user interface
"""
FONT_SIZE = 25

"""
The number of pixels of padding to use between the font
and the screen.
"""
FONT_PADDING = 10

"""
The color of the font (this is an RGB value)
"""
FONT_COLOR = (255, 255, 255)

"""
The color used for the background behind the font.
"""
FONT_BACKGROUND = (255, 255, 255)

"""
The number of pixels between two lines of text on the screen.
"""
FONT_LINESPACE = 4

import pygame

class UserInterface:

    def __init__(self):
        # Define a font object to use
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join("UI", "larabie.ttf"), FONT_SIZE, )
        self.gamestate = True # The game is running
	self.hasWon = False;

    def update(self, gamedata):
        # We save a surface containing the text we want to show.
        self.score = self.font.render("Score: " + str(gamedata.score),
                                      True, FONT_COLOR)
        self.lives = self.font.render("Lives: " + str(gamedata.lives),
                                      True, FONT_COLOR)
        self.resources = self.font.render("Resources: " + str(gamedata.resources),
                                          True, FONT_COLOR)
        self.defeat = self.font.render("You have been defeated!", True,
                                       FONT_COLOR)
	self.currentLevel = self.font.render("Level: " + str(gamedata.mapNumber),
				       True, FONT_COLOR)
	self.nextLevel = self.font.render("Great Job! Moving on to next level...", True,
				       FONT_COLOR)

    def draw(self, surface):
        # Draw the score in the upper left corner
        surface.blit(self.score, (FONT_PADDING, FONT_PADDING))
        # Put the number of lives below the score
        surface.blit(self.lives, (FONT_PADDING, FONT_SIZE+FONT_PADDING+FONT_LINESPACE))
        # Put the resources in the top right corner
        surface.blit(self.resources, (surface.get_width()-FONT_PADDING-self.resources.get_width(),
                                      FONT_PADDING))
	surface.blit(self.currentLevel, (surface.get_width()- FONT_PADDING-self.currentLevel.get_width(),
                                      FONT_SIZE + FONT_PADDING + FONT_LINESPACE))

	if(self.hasWon):
	    surface.blit(self.nextLevel, ((surface.get_width()-self.nextLevel.get_width())/2,
                                       (surface.get_height()-self.nextLevel.get_height())/2))
        # If the game has ended, show a defeat message
        if(not self.gamestate):
            surface.blit(self.defeat, ((surface.get_width()-self.defeat.get_width())/2,
                                       (surface.get_height()-self.defeat.get_height())/2))

    def showDefeat(self):
        self.gamestate = False # The game is 

    def showWin(self):
	self.hasWon = True #Has won the current level
        
# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
        
