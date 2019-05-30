from src.Entities.entity import Entity
from src.Assets import settings


class Platform(Entity):
    def __init__(self, image, pos, *groups, width=settings.TILE_SIZE, height=settings.TILE_SIZE):
        super().__init__(image, width, height, pos, *groups)

class NextLevelPlatform(Platform):
    def __init__(self, image, pos, *groups, width=settings.TILE_SIZE, height = settings.TILE_SIZE):
        super().__init__(image, pos, *groups)

class GameOverPlatform(Platform):
    def __init__(self, image, pos, *groups, width=settings.TILE_SIZE, height = settings.TILE_SIZE):
        super().__init__(image, pos, *groups)
