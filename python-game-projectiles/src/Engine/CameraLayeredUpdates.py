import pygame
from src.Assets import settings


class CameraLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size=pygame.Rect(0, 0, settings.LEVEL_WIDTH, settings.LEVEL_HEIGHT)):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + settings.WINDOW_WIDTH / 2
            y = -self.target.rect.center[1] + settings.WINDOW_HEIGHT / 2
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width - settings.WINDOW_WIDTH), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height - settings.WINDOW_HEIGHT), min(0, self.cam.y))

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        self.lostsprites = []
        dirty = self.lostsprites
        # self.lostsprites = []
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
