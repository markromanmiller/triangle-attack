import time
import pygame
import os
import tower

class LightningTower(tower.Tower):
    DEFAULT_RECHARGE_TIME = 0.05 #this is a float in seconds
    
    def __init__(self, x, y, group, size, image):
        self.defaultRechargeTime = LightningTower.DEFAULT_RECHARGE_TIME
        self.timeOfLastFire = 0;
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.transform.scale(image, size)
        self.size = size
        self.sprite.rect = pygame.Rect(x, y, size[0], size[1])
        group.add(self.sprite)
        self.laserRange = 150
        self.damage = 1
        self.charged = False
        self.channel = None
        self.sound = pygame.mixer.Sound(os.path.join("images", "lightning_tower_shoot.wav"))

    def fire(self, enemies):
        shortestDistance = self.laserRange**2 #this is pixels squared
        closestEnemy = []
        (myX, myY) = self.sprite.rect.center
        for enemy in enemies:
            (enemyX, enemyY) = enemy.sprite.rect.center
            currentDistance = (myX-enemyX)**2 + (myY-enemyY)**2
            if currentDistance < shortestDistance:
                closestEnemy.append(enemy)
        for e in closestEnemy:
            e.takeDamage(self.damage)
            self.timeOfLastFire = time.time()
        if closestEnemy != []:
            self.playSound()
        return closestEnemy
    
    def playSound(self):
        if (self.channel == None or not(self.channel.get_busy())):
            self.channel = self.sound.play()
    
