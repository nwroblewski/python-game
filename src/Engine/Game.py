import pygame as pg
from src.Assets import settings

class Game:

    def __init__(self, window_width, window_height):
        self.window = pg.display.set_mode((settings.WINDOW_WIDTH,settings.WINDOW_HEIGHT))
        pg.display.set_caption("Gameee")
        self.clock = pg.time.Clock()
        self.running = True

    def new_game(self):
        
    def run(self):
        self.playing = True
        self.clock.tick(settings.FPS)










