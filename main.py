from src.Engine.Game import Game
from src.Assets import settings
from src.Entities.Player import Player
from src.Engine.CameraLayeredUpdates import CameraLayeredUpdates
import pygameMenu
import pygame
from pygameMenu.locals import *
from pygame import *
from src.World.LevelGenerator import LevelGenerator
from src.Engine.CollisionDetector import CollisionDetector
from src.Engine.Server import Server
from src.Entities.Enemy import Enemy
from src.Entities.BigEnemy import BigEnemy


def start_single(levelGenerator):
    if 'game' not in globals():
        levelGenerator.load(1)
        game = Game(player, entities, collisionDetector, bg, window)
    game.run()
    player.reset()

def start_multi():
    if 'game' not in globals():
        levelGenerator.load(1)
        game = Game(player, entities, collisionDetector, bg, window)
        game.start_communication()
    game.run()
    player.reset()

def start_server():
    if 'server' not in globals():
        server = Server(entities, collisionDetector, [])
    server.run()

def multi_menu():
    multiplayer_menu = pygameMenu.Menu(window, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT, pygameMenu.fonts.FONT_8BIT, "Multiplayer", bgfun=main_background, menu_alpha=20)
    multiplayer_menu.add_option("Connect", start_multi)
    multiplayer_menu.add_option("Back to main menu", PYGAME_MENU_BACK)
    return multiplayer_menu

def server_menu():
    serv_menu = pygameMenu.Menu(window, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT, pygameMenu.fonts.FONT_8BIT, "Server menu", bgfun=main_background, menu_alpha=20)
    serv_menu.add_option("Host server", start_server)
    serv_menu.add_option("Back to main menu", PYGAME_MENU_BACK)
    return serv_menu

def main_background():
    window.blit(bg, (0, 0))
    # pass

def create_menus():
    m = multi_menu()
    s = server_menu()
    main_menu = pygameMenu.Menu(window, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT, pygameMenu.fonts.FONT_8BIT,
                                "Fortnite", bgfun=main_background, menu_alpha=20)
    main_menu.add_option("Singleplayer", start_single, levelGenerator)
    main_menu.add_option("Multiplayer", m)
    main_menu.add_option("Host server", s)
    main_menu.add_option("Exit", PYGAME_MENU_EXIT)
    return main_menu


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Fortnite")
    platforms = pygame.sprite.Group()
    player = Player((settings.TILE_SIZE, settings.WINDOW_HEIGHT - settings.TILE_SIZE))
    enemies = [Enemy((3500, 70)), Enemy((250, 70)), BigEnemy((3700, 150))]
    entities = CameraLayeredUpdates(player)
    levelGenerator = LevelGenerator(platforms, entities)

    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

    bg = pygame.image.load(settings.SPRITES_PATH + "bg.jpg")
    bg = pygame.transform.scale(bg, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    bg.fill((58, 64, 65))
    collisionDetector = CollisionDetector(platforms, entities, levelGenerator, enemies)
    collisionDetector.add_player(player)

    menu = create_menus()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()

        menu.mainloop(events)
