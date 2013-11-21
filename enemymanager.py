"""
This module handles the spawning of enemies.
"""

import pygame
import enemy
import Queue



class EnemyManager:

    """
    The event ID for a event to spawn a basic enemy. When a
    basic enemy is scheduled to spawn, an event with this ID
    is posted to the event queue.
    """
    SPAWN_EVENT_BASIC = pygame.USEREVENT

    """
    The time (in milliseconds) at which the last spawning of
    a wave of enemies occurred.
    """
    last_wave_time = 0

    """
    The amount of time between waves.
    """
    wave_interval = 5000

    """
    The current wave to determine the strength of enemies
    """
    wave = 1

    """
    The number of basic enemies to spawn during a given wave.
    """
    basic_enemies = 1

    """
    The time between spawning two enemies during a wave. This
    is so that enemies don't overlap on the screen.
    """
    spawn_interval = 1000

    """
    The list of enemies in the game.
    """
    enemies = []

    """
    The time at which the last update occurred.
    """
    last_update_time = pygame.time.get_ticks()

    """
    The sprites of all enemies in the game.
    """
    spritegroup = pygame.sprite.Group()

    """
    The priority queue of enemies to be spawned. This queue is arranged
    on the scheduled time for an enemy to spawn. 
    """
    enemy_queue = Queue.PriorityQueue()

    """
    The last time something was spawned.
    """
    last_spawn_time = pygame.time.get_ticks()

    def newLevel(self):
	self.wave = 0
	self.maxWave += 1

    def __init__(self, size, maxWave):
        self.last_wave_time = pygame.time.get_ticks()
        self.last_update_time = pygame.time.get_ticks()
        self.size = size
	self.maxWave = maxWave
        

    """
    Updates the enemies and schedules waves, if necessary. This returns the number
    of enemies that have hit the destination.
    """
    def update(self, mapdata):
        retval = 0
	killed = 0
        # Update the enemies
        for curr in EnemyManager.enemies:
            curr.update(pygame.time.get_ticks()-self.last_update_time, mapdata)
            if(curr.dead() or curr.offscreen(mapdata)):
                EnemyManager.enemies.remove(curr)
                killed += 1
                curr.sprite.kill() # Remove the sprite from the sprite group
            if(curr.atDestination(mapdata)):
                try:
                    EnemyManager.enemies.remove(curr)
                    curr.sprite.kill()
                    retval += 1
                except ValueError as e:
                    pass
        self.last_update_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        # Spawn enemies that need to be spawned
        spawning = True
        while(spawning and not EnemyManager.enemy_queue.empty()):
            current_enemy = EnemyManager.enemy_queue.get()
            if(current_enemy[0] > current_time): # Then we don't need to spawn yet
                EnemyManager.enemy_queue.put(current_enemy)
                spawning = False
            else:
                EnemyManager.enemies.append(current_enemy[1])

        
        # If enough time has passed, and we're not spawning a wave, spawn a wave
        if((current_time - EnemyManager.last_wave_time >= EnemyManager.wave_interval) and (self.wave < self.maxWave)):
            # Spawn a wave!
	    self.wave += 1
            start = mapdata.getStartingTile()
            size = mapdata.getTileSize()
            EnemyManager.last_wave_time = current_time
            for index in range(0, EnemyManager.basic_enemies):
                new_enemy = enemy.Enemy(start[0], start[1], EnemyManager.spritegroup, size, self.wave)
                scheduled_time = index*EnemyManager.spawn_interval+current_time
                EnemyManager.enemy_queue.put((scheduled_time, new_enemy))
            # Increase the difficulty!
	    if(self.wave % 5 == 1):
                EnemyManager.basic_enemies += 1
        return retval, killed

    """
    Checks to see if all enemies are removed from the field
    """
    def isFinished(self):
	return (self.wave >= self.maxWave and len(self.enemies) == 0)

    """
    Draw all enemies in the game to the screen.
    """
    def draw(self, surface):
        EnemyManager.spritegroup.draw(surface)

    """
    Given a pygame event from the event queue, spawn an enemy (if necessary).
    The coordinates are the x and y coordinates of the starting tile (a tuple).
    """
    def spawnEnemy(self, event, coordinates):
        if(event.type == EnemyManager.SPAWN_EVENT_BASIC):
            EnemyManager.enemies.append(enemy.Enemy(coordinates[0], coordinates[1],
                                                 EnemyManager.spritegroup, self.size, self.wave))


# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
        

