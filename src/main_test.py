from src.Engine.Game import Game
from src.Assets import settings
from src.Entities.Player import Player
from src.Engine.CameraLayeredUpdates import CameraLayeredUpdates
import pygameMenu
import pygame
from pygameMenu.locals import *  # Import constants (like actions)
from pygame import *
from src.World.LevelGenerator import LevelGenerator


def main():

    LevelGenerator(platforms, game.entities, 1)

    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return

        game.entities.update()

        window.fill((0, 0, 0))
        game.entities.draw(window)
        pygame.display.update()
        game.clock.tick(settings.FPS)


def main_background():
    window.blit(bg, (0, 0))


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Fortnite")
    platforms = pygame.sprite.Group()
    player = Player(platforms, (2*settings.TILE_SIZE, settings.WINDOW_HEIGHT - settings.TILE_SIZE))
    entities = CameraLayeredUpdates(player, pygame.Rect(0, 0, settings.LEVEL_WIDTH, settings.LEVEL_HEIGHT))
    game = Game(player, entities)

    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

    bg = pygame.image.load(settings.SPRITES_PATH + "bg.jpg")
    bg = pygame.transform.scale(bg, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

    main_menu = pygameMenu.Menu(window, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT, pygameMenu.fonts.FONT_8BIT,
                                "Fortnite", bgfun=main_background, menu_alpha=20)  # -> Menu object
    main_menu.add_option("Start the game", main)
    main_menu.add_option("Host coop", main)
    main_menu.add_option("Join coop", main)
    main_menu.add_option("Exit", PYGAME_MENU_EXIT)

    while True:
        game.clock.tick(settings.FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()

        main_menu.mainloop(events)
