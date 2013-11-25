"""
maptile.py - Definition of a map tile. Every map is divided into a grid of
tiles. Tiles can hold an enemy or a tower.
"""

import pygame
import os

"""
Constants used to define the type of map tile this is.
"""
PLOT = 0 # A tower can be built on this tile, and no enemy can access it
PATH = 1 # Enemies can access this tile, and no tower can be built on it
START = 2 # Enemies spawn from this tile, and nothing can be present on it
DESTINATION = 3 # Enemies go towards this tile, and nothing can be present on it

class Tile:

    """
    This is the sprite associated with this tile.
    """
    sprite = None
    
    def __init__(self, character, x, y):
        self.x = x
        self.y = y
        self.visited = False # Used in searches
        # Decode the character for the type of the plot
        if(character == "."):
            self.type = PATH
        elif(character == "S"):
            self.type = START
        elif(character == "E"):
             self.type = DESTINATION
        else:
            self.type = PLOT # By default we can build towers on it

    """
    Add the sprite associated with this tile to the group.
    """
    def getSprite(self, group, size):
        if(self.sprite == None): # Generate the sprite from an image
            self.sprite = pygame.sprite.Sprite(group)
            name = None # The name of the image to use
            if(self.type == PATH):
                name = "path.png"
            elif(self.type == START):
                name = "start.png"
            elif(self.type == DESTINATION):
                name = "end.png"
            else: # Buildable tile by default
                name = "plot.png"
            # The os.path.join() function is used for cross platform compatibility
            self.sprite.image = pygame.image.load(os.path.join("images", name)).convert()
            self.sprite.image = pygame.transform.scale(self.sprite.image, size)
            # Set the position of the sprite using a rectangle
            width = self.sprite.image.get_width()
            height = self.sprite.image.get_height()
            spriterect = pygame.Rect(self.x*width, self.y*height, width, height)
            self.sprite.rect = spriterect
        # Add the sprite to the sprite group
        group.add(self.sprite)
        
    def isPlot(self):
	return self.type == PLOT
# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
                
