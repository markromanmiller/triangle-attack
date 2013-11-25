import time
import pygame
import os

class Tower:

    DEFAULT_RECHARGE_TIME = 1.0 #this is a float in seconds
    
    def __init__(self, x, y, group, size, image):
        self.defaultRechargeTime = Tower.DEFAULT_RECHARGE_TIME
        self.timeOfLastFire = 0;
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.transform.scale(image, size)
        self.size = size
        self.sprite.rect = pygame.Rect(x, y, size[0], size[1])
        group.add(self.sprite)
	self.laserRange = 2*size[0]
	self.damage = 100
	self.charged = False
        self.sound = pygame.mixer.Sound(os.path.join("images", "tower_shoot.wav"))
    
    def charge(self, extraDamage, extraRange):
	if not self.charged :
	    self.damage *= extraDamage
	    self.laserRange += extraRange
	    self.charged = True


    def canFire(self):
        return (time.time() - self.defaultRechargeTime > self.timeOfLastFire)
    
    def fire(self, enemies):
        shortestDistance = self.laserRange**2 #this is pixels squared
        closestEnemy = None
        (myX, myY) = self.sprite.rect.center
        for enemy in enemies:
            (enemyX, enemyY) = enemy.sprite.rect.center
            currentDistance = (myX-enemyX)**2 + (myY-enemyY)**2
            if currentDistance < shortestDistance:
                shortestDistance = currentDistance
                closestEnemy = enemy
        if closestEnemy != None:
            closestEnemy.takeDamage(self.damage)
            self.timeOfLastFire = time.time()
            self.sound.play()
        return [closestEnemy]
    
    def delete(self):
        self.sprite.kill()
