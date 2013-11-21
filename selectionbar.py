import os 
import pygame

"""
draws the selection bar under the field, where the player can choose towers to build
"""

class SelectionBar:
    
    """
    buffers
    """
    FONT_SIZE = 25
    PADDING = 50
    FONT_COLOR = (255, 255, 255)


    def __init__(self, size):
        self.font = pygame.font.Font(os.path.join("UI", "larabie.ttf"), SelectionBar.FONT_SIZE, )
        self.selections = ["tower", "recharge_tower", "lightning_tower"]
        self.prices = [100, 200, 250]
        self.images = []
        self.priceSurface = []
        self.rect = []
        for s in self.prices:
            self.priceSurface.append(self.font.render(str(s),True, SelectionBar.FONT_COLOR))
        for s in self.selections:
            drawn = pygame.transform.scale(pygame.image.load(os.path.join("images", s + ".png")), size)
            self.images.append(drawn)
        self.pad = -1
        for e in self.images:
            self.rect.append(pygame.Rect(((size[0]*10 / 2) - SelectionBar.PADDING + self.pad * 100), (700 - SelectionBar.PADDING * 2), size[0], size[1]))
            self.pad += 1

    def draw(self, surface):
        self.pad = -1
        if(self.images != None):
            for e in self.images:
                surface.blit(e, (((surface.get_width() / 2) - SelectionBar.PADDING + self.pad * 100), ((surface.get_height()) - SelectionBar.PADDING * 2)))
                self.pad += 1
            self.pad = -1
            for s in self.priceSurface:
                surface.blit(s, (((surface.get_width() / 2) - SelectionBar.PADDING + self.pad * 100), ((surface.get_height()) - SelectionBar.PADDING * 2 )))
                self.pad += 1

    def handleMouseEvent(self, event):
        for enum, r in enumerate(self.rect):
            if r.collidepoint(event.pos):
                return enum
        return -1
