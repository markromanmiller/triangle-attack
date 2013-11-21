import pygame
import os

class SoundManager:
    def __init__(self):
        mix = pygame.mixer
        mix.quit()
        mix.init(22050)
        mix.music.load(os.path.join("images", "level_bgm.ogg"))
        mix.music.play(-1)
