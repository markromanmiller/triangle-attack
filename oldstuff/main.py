"""
main.py - The entry point into the game. This runs the main game loop.
"""

import pygame
import sys
import gamemap
import os
import gamedata
import userinterface
import enemymanager
import towermanager
import time
import soundmanager

"""
The dimensions for the screen. These should remain constant.
"""
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

"""
The max number of frames per second for the game.
"""
MAX_FPS = 60

"""
The game clock
"""
GameClock = None

"""
The title of the game. This should remain constant.
"""
TITLE = "Attack of the Triangles"

"""
This performs initial setup of the game. Any global variables
should also be defined here (yes, I know most people say global
variables are bad, but there really isn't a simple solution).
"""
def setup():
   
    # Set the title of the game.
    pygame.display.set_caption(TITLE)
    # Set up a new window.
    global ScreenSurface
    ScreenSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set up the map
    global Map
    # Set up the starting game data
    global Data
    Data = gamedata.GameData()
    # Set up the UI
    global UI
    UI = userinterface.UserInterface()
    Map = gamemap.GameMap("map1", ScreenSurface)
    # Initialize the enemy manager
    global EnemyManager
    EnemyManager = enemymanager.EnemyManager(Map.getTileSize(), 10)
    # initialize the tower manager
    global TowerManager
    TowerManager = towermanager.TowerManager(Map.getTileSize())
    # start mixer, load song
    global SoundManager
    SoundManager = soundmanager.SoundManager()
    global GameClock
    GameClock = pygame.time.Clock()
    global GameState
    GameState = True


"""
Makes a new map
"""
def makeMap(nextMap):
    global Map
    Map = gamemap.GameMap("map" + str(nextMap), ScreenSurface)
"""
This handles a single pygame event.
"""
def handleEvent(event):
    if(event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
        handleKeyEvent(event)
    if event.type == pygame.QUIT:
        # Quit the program safely
        pygame.quit()
        sys.exit()
    else:
        EnemyManager.spawnEnemy(event, Map.getStartingTile())

"""
This is the main game loop, called as many times as
the computer allows.
"""
def main():
    while(1):
        #Handle the event queue
        event = pygame.event.poll()
        # The event queue returns an event of type NOEVENT if the queue is empty
        while(event.type != pygame.NOEVENT):
            handleEvent(event)
            event = pygame.event.poll()
        # Delete anything already on the surface.
        ScreenSurface.fill((0, 0, 0))
        update() # Update the game objects
        draw() # Draw all the game objects
        pygame.display.flip()

        # Maintain the max frame rate
        GameClock.tick(MAX_FPS)
       

"""
Handles any updating of game objects. This is called
once per game loop.
"""
def update():
    global GameState
    if(GameState):
        # Update the enemies
        livesLost = EnemyManager.update(Map)
        Data.lives -= livesLost
        # Update the Towers
        TowerManager.update(EnemyManager.enemies)
        # Update the UI
        UI.update(Data)
        # Check if the game is over
        if(Data.lives <= 0):
            GameState = False # The game is over
            UI.showDefeat()
	if(EnemyManager.isFinished()):
       	    UI.hasWon = True
            UI.draw(ScreenSurface)
            pygame.display.flip()
            TowerManager.endLevel()
            time.sleep(5)
            UI.hasWon = False
	    Data.mapNumber += 1
	    EnemyManager.maxWave += EnemyManager.maxWave
	    makeMap(Data.mapNumber)
    

"""
Draws all game objects to the screen. This is called once
per game loop.
"""
def draw():
    # Draw the map
    Map.draw(ScreenSurface)
    # Draw the enemies
    EnemyManager.draw(ScreenSurface)
    # Draw the towers
    TowerManager.drawSprites(ScreenSurface)
    TowerManager.drawAttacks(ScreenSurface)
    # Draw the UI
    UI.draw(ScreenSurface)
    

"""
Handles a single keyboard event (both key down and key up).
The event passed in is assumed to be a key event, or else
nothing happens.
"""
def handleKeyEvent(event):
    if(event.type == pygame.KEYDOWN):
        # If the escape key has been pressed, quit the game safely
        if(event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
    else:
        if(event.type == pygame.KEYUP):
            return # TODO: Add stuff for key up events here

pygame.init()
setup()
main()
