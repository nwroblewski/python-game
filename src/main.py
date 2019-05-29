from src.Engine.Game import Game
from src.Assets import settings
from src.Entities.Player import Player
from src.Engine.CameraLayeredUpdates import CameraLayeredUpdates
import pygameMenu
import pygame
from pygameMenu.locals import *
from pygame import *
from src.World.LevelGenerator import LevelGenerator

def main(levelGenerator):
    levelGenerator.load(1)
    game.run(window)


def main_background():
    window.blit(bg, (0, 0))


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Fortnite")
    platforms = pygame.sprite.Group()
    player = Player(platforms, (2*settings.TILE_SIZE, settings.WINDOW_HEIGHT - settings.TILE_SIZE))
    entities = CameraLayeredUpdates(player, pygame.Rect(0, 0, settings.LEVEL_WIDTH, settings.LEVEL_HEIGHT))
    levelGenerator = LevelGenerator(platforms, entities)

    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

    bg = pygame.image.load(settings.SPRITES_PATH + "bg.jpg")
    bg = pygame.transform.scale(bg, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

    game = Game(player, entities, bg)

    main_menu = pygameMenu.Menu(window, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT, pygameMenu.fonts.FONT_8BIT,
                                "Fortnite", bgfun=main_background, menu_alpha=20)
    main_menu.add_option("Single player", main, levelGenerator)
    main_menu.add_option("Join server", main, levelGenerator)
    main_menu.add_option("Exit", PYGAME_MENU_EXIT)

    while True:
        game.clock.tick(settings.FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()

        main_menu.mainloop(events)
