import tower
import lightningtower
import pygame
import rechargetower

class TowerManager:
    def __init__(self, size):
        self.size = size
        self.towers = []
        self.spritegroup = pygame.sprite.Group()
        self.attacks = [] # set for attacks: list [tower, enemy, time]

    def drawSprites(self, surface):
        self.spritegroup.draw(surface)
    
    def drawAttacks(self, surface):
        for attack in self.attacks:
            tX, tY = attack[0].sprite.rect.center
            eX, eY = attack[1].sprite.rect.center
            bR = self.size[0] / 20 * 3
            lR = self.size[0] / 20 * 2
            colors = ((127, 127, 127), (255, 255, 255))
            if isinstance(attack[0], tower.Tower):
                colors = ((0, 127, 58), (0, 255, 116))
            if isinstance(attack[0], lightningtower.LightningTower):
                colors = ((0, 110, 127), (0, 220, 255))
            elif isinstance(attack[0], rechargetower.RechargeTower):
                colors = ((127, 127, 127), (255, 255, 255))

            pygame.draw.circle(surface, colors[0], (tX, tY), bR)
            pygame.draw.circle(surface, colors[0], (eX, eY), bR)
            pygame.draw.line(surface, colors[0], (tX, tY), (eX, eY), bR)
            pygame.draw.circle(surface, colors[1], (tX, tY), lR)
            pygame.draw.circle(surface, colors[1], (eX, eY), lR)
            pygame.draw.line(surface, colors[1], (tX, tY), (eX, eY), lR)
            
            attack[2] -= 1
        for attack in self.attacks:
            if attack[2] < 0:
                self.attacks.remove(attack)
    
    def addNewTower(self, index, position):
        (x, y) = position
        x *= self.size[0]
        y *= self.size[1]
        position = (x, y)
        if(index == 0):
            self.addTower(position)
        elif(index == 1):
            self.addRechargeTower(position)
        elif(index == 2):
            self.addLightningTower(position)

    def addTower(self, coordinates):
        self.towers.append(tower.Tower(coordinates[0], coordinates[1],
                                                 self.spritegroup, self.size))
    
    def addLightningTower(self, coordinates):
        self.towers.append(lightningtower.LightningTower(coordinates[0],coordinates[1],
            self.spritegroup, self.size))

    def addRechargeTower(self, coordinates):
        self.towers.append(rechargetower.RechargeTower(coordinates[0],coordinates[1],
        self.spritegroup, self.size))
    def update(self, enemies):
        
        for t in self.towers:
            target = None
            if isinstance(t, rechargetower.RechargeTower):
                target = t.fire(self.towers)
            elif t.canFire():
                target = t.fire(enemies)
            if target != None and target != [None]:
                for enemy in target:
                    self.attacks.append([t, enemy, 20])
    
    def endLevel(self):
        for i in range(len(self.towers)):
            self.towers[0].delete()
            del self.towers[0]
        self.towers = []
        self.attacks = []
           
