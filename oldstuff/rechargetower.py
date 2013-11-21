import time
import pygame
import os
import tower

class RechargeTower(tower.Tower):
    DEFAULT_RECHARGE_TIME =  10 #this is a float in seconds

    image = pygame.image.load(os.path.join("images", "recharge_tower.png"))
    
    def __init__(self, x, y, group, size):
        self.defaultRechargeTime = RechargeTower.DEFAULT_RECHARGE_TIME
        self.timeOfLastFire = 0;
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.transform.scale(RechargeTower.image, size)
        self.size = size
        self.sprite.rect = pygame.Rect(x, y, size[0], size[1])
        group.add(self.sprite)
    	self.laserRange = 100
	self.damage = 1.1
	self.charged = False

    def fire(self, enemies):
        shortestDistance = self.laserRange**2 #this is pixels squared
        closesttower = []
        (myX, myY) = self.sprite.rect.center
        for tower in enemies:
            (towerX, towerY) = tower.sprite.rect.center
            currentDistance = (myX-towerX)**2 + (myY-towerY)**2
            if currentDistance < shortestDistance:
		closesttower.append(tower)
        for e in closesttower:
            e.charge(self.damage, self.damage * 20)
            self.timeOfLastFire = time.time()
        return closesttower
