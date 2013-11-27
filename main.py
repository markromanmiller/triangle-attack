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
import selectionbar

"""
The dimensions for the screen. These should remain constant.
"""
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

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
def firstSetup():
    global firstScreen 
    firstScreen = True
    # Set the title of the game.
    pygame.display.set_caption(TITLE)
    # Set up a new window.
    global ScreenSurface
    ScreenSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    global UI
    UI = userinterface.UserInterface()
    global image
    image = pygame.image.load(os.path.join("game_assets", "title.png")).convert()
    global GameClock
    GameClock = pygame.time.Clock()
    global GameState
    GameState = True

def setup():
   
    # Set up the map
    global Map
    # Set up the starting game data
    global Data
    Data = gamedata.GameData()
    # Set up the UI
    Map = gamemap.GameMap("map1", ScreenSurface)
    # Initialize the enemy manager
    global EnemyManager
    EnemyManager = enemymanager.EnemyManager(Map.getTileSize(), 15)
    # initialize the tower manager
    global TowerManager
    TowerManager = towermanager.TowerManager(Map.getTileSize(), ScreenSurface)
    # start mixer, load song
    global SoundManager
    SoundManager = soundmanager.SoundManager()
    global SelectionBar
    SelectionBar = selectionbar.SelectionBar(Map.getTileSize())
    global selectedTower
    selectedTower = None


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
    global firstScreen
    if(event.type == pygame.MOUSEBUTTONDOWN):
        handleMouseEvent(event)
    elif not(firstScreen):
        EnemyManager.spawnEnemy(event, Map.getStartingTile())

def handleMouseEvent(event):
    global firstScreen
    if firstScreen:
        setup()
        firstScreen = False
        return
    e = SelectionBar.handleMouseEvent(event)
    global selectedTower
    if(e == -1 and event.pos[1] < SCREEN_WIDTH and selectedTower != None):
        (mapX, mapY) = Map.getTileCoordinates(event.pos)
        if(not(Map.tiles[mapX][mapY].isPlot()) or Data.resources < SelectionBar.prices[selectedTower]):
            return
        if (mapX, mapY) in TowerManager.towerPositions:
            return
        Data.lose(SelectionBar.prices[selectedTower])
        TowerManager.addNewTower(selectedTower, (mapX, mapY))
    else:
        selectedTower = e

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
    global firstScreen
    if firstScreen:
        return
    global GameState
    if(GameState):
        # Update the enemies
        val = EnemyManager.update(Map)
        Data.lives -= val[0]
        Data.earn(val[1])
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
        EnemyManager.newLevel()
        makeMap(Data.mapNumber)
    

"""
Draws all game objects to the screen. This is called once
per game loop.
"""
def draw():
    if firstScreen:
        global image
        ScreenSurface.blit(image, (0, 0))
        return
    # Draw the map
    Map.draw(ScreenSurface)
    # Draw the enemies
    EnemyManager.draw(ScreenSurface)
    # Draw the towers
    TowerManager.drawSprites(ScreenSurface)
    TowerManager.drawAttacks(ScreenSurface)
    # Draw the UI
    UI.draw(ScreenSurface)
    SelectionBar.draw(ScreenSurface)
    

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
firstSetup()
main()
