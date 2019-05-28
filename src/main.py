#!/usr/bin/python3.7
from Assets import settings
#from Engine.LevelGenerator import LevelGenerator
import pygame
from pygame import *
import pygameMenu                # This imports classes and other things
from pygameMenu.locals import *  # Import constants (like actions)

window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

def main():
    #bg = pygame.image.load(settings.SPRITES_PATH + 'bg.jpg')
    clock = pygame.time.Clock()

    platforms = pygame.sprite.Group()
    player = Player(platforms, (2*settings.TILE_SIZE, settings.WINDOW_HEIGHT - settings.TILE_SIZE))
    entities = CameraLayeredUpdates(player, pygame.Rect(0, 0, settings.LEVEL_WIDTH, settings.LEVEL_HEIGHT))

    LevelGenerator(platforms, entities, 1)

    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return
        
        entities.update()

        window.fill((0, 0, 0))
        entities.draw(window)
        pygame.display.update()
        clock.tick(settings.FPS)


class LevelGenerator():
    def __init__(self, platforms, entities, level):
        self.tiles = [pygame.image.load(settings.SPRITES_PATH + 'tile1.png'),
                pygame.image.load(settings.SPRITES_PATH + 'tile2.png')]

        for ind, val in enumerate(self.tiles):
            rect = val.get_rect()
            if not (rect.width == settings.TILE_SIZE and rect.height == settings.TILE_SIZE):
                self.tiles[ind] = pygame.transform.scale(self.tiles[ind], (settings.TILE_SIZE, settings.TILE_SIZE))

        f = open(settings.LEVELS_PATH + str(level), "r")
        x = 0
        y = 0
        for line in f.readlines():
            for char in line:
                if(char == "1"):
                    Platform(self.tiles[1], (x, y), platforms, entities)
                x += settings.TILE_SIZE
            x = 0
            y += settings.TILE_SIZE

class CameraLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + settings.WINDOW_WIDTH/2
            y = -self.target.rect.center[1] + settings.WINDOW_HEIGHT/2
            self.cam += (pygame.Vector2((x,y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width - settings.WINDOW_WIDTH), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height - settings.WINDOW_HEIGHT), min(0 , self.cam.y))
    
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        self.lostsprites = []
        dirty = self.lostsprites
        #self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)

class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        self.init_images()
        super().__init__(self.char, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT, pos)
        self.vel = pygame.Vector2((0,0))
        self.onGround = False
        self.jump_strength = settings.PLAYER_JUMP_STRENGTH
        self.platforms = platforms
        self.speed = settings.PLAYER_SPEED
        self.walk_count = 0

        #self.char = pygame.image.load(settings.SPRITES_PATH + 'standing.png')

    def init_images(self):
        self.char = pygame.image.load(settings.SPRITES_PATH + 'standing.png')
        self.walk_right = [pygame.image.load(settings.SPRITES_PATH + 'R1.png'),
            pygame.image.load(settings.SPRITES_PATH + 'R2.png'),
            pygame.image.load(settings.SPRITES_PATH + 'R3.png'),
            pygame.image.load(settings.SPRITES_PATH + 'R4.png'),
            pygame.image.load(settings.SPRITES_PATH + 'R5.png'),
            pygame.image.load(settings.SPRITES_PATH + 'R6.png'),
            pygame.image.load(settings.SPRITES_PATH + 'R7.png'),
            pygame.image.load(settings.SPRITES_PATH + 'R8.png'),
            pygame.image.load(settings.SPRITES_PATH + 'R9.png')]
        self.walk_left = [pygame.image.load(settings.SPRITES_PATH + 'L1.png'),
            pygame.image.load(settings.SPRITES_PATH + 'L2.png'),
            pygame.image.load(settings.SPRITES_PATH + 'L3.png'),
            pygame.image.load(settings.SPRITES_PATH + 'L4.png'),
            pygame.image.load(settings.SPRITES_PATH + 'L5.png'),
            pygame.image.load(settings.SPRITES_PATH + 'L6.png'),
            pygame.image.load(settings.SPRITES_PATH + 'L7.png'),
            pygame.image.load(settings.SPRITES_PATH + 'L8.png'),
            pygame.image.load(settings.SPRITES_PATH + 'L9.png')]

        for ind, val in enumerate(self.walk_right):
            rect = val.get_rect()
            if not (rect.width == settings.PLAYER_WIDTH and rect.height == settings.PLAYER_HEIGHT):
                self.walk_right[ind] = pygame.transform.scale(self.walk_right[ind], (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))

        for ind, val in enumerate(self.walk_left):
            rect = val.get_rect()
            if not (rect.width == settings.PLAYER_WIDTH and rect.height == settings.PLAYER_HEIGHT):
                self.walk_left[ind] = pygame.transform.scale(self.walk_left[ind], (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))

        rect = self.char.get_rect()
        if not (rect.width == settings.PLAYER_WIDTH and rect.height == settings.PLAYER_HEIGHT):
            self.char = pygame.transform.scale(self.char, (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))

    def anim(self, direction):
        self.walk_count = self.walk_count % 27
        if direction == "left":
            self.image = self.walk_left[self.walk_count // 3]
            self.walk_count += 1
        elif direction == "right":
            self.image = self.walk_right[self.walk_count // 3]
            self.walk_count += 1
        elif direction == "stand":
            self.image = self.char

    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        space = pressed[K_SPACE]

        if space or up:
            if self.onGround:
                self.vel.y = -self.jump_strength
        if left:
            self.vel.x = -self.speed
            self.anim("left")
        if right:
            self.vel.x = self.speed
            self.anim("right")
        if not self.onGround:
            self.vel.y += settings.PLAYER_GRAVITY
            if self.vel.y > settings.MAX_FALLING_SPEED: self.vel.y = settings.MAX_FALLING_SPEED
            #print('Predkosc vel.y: ' + str(self.vel.y))
        if not(left or right):
            self.vel.x = 0
            self.anim("stand")
        self.rect.left += self.vel.x
        self.collide(self.vel.x, 0, self.platforms)
        self.rect.top += self.vel.y
        self.onGround = False
        self.collide(0, self.vel.y, self.platforms)
    
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                #if isinstance(p, ExitBlock):                       # CHECKPOINT?
                #    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

class Platform(Entity):
    def __init__(self, image, pos, *groups, width = settings.TILE_SIZE, height = settings.TILE_SIZE):
        super().__init__(image, width, height, pos, *groups)

def main_background():
    window.blit(bg, (0,0))

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Fortnite")
    bg = pygame.image.load(settings.SPRITES_PATH + "bg.jpg")
    bg = pygame.transform.scale(bg, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    main_menu = pygameMenu.Menu(window, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT, pygameMenu.fonts.FONT_8BIT, "Fortnite", bgfun=main_background, menu_alpha=20) # -> Menu object
    main_menu.add_option("Start the game", main)
    main_menu.add_option("Host coop", main)
    main_menu.add_option("Join coop", main)
    main_menu.add_option("Exit", PYGAME_MENU_EXIT)
    clock = pygame.time.Clock()

    while True:
        clock.tick(settings.FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()

        main_menu.mainloop(events)
