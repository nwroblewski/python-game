import pygame


class Projectile:

    # TODO add fancy projectile animation here
    def __init__(self, x, y, radius, direction):
        self.init_images()
        self.x = x
        self.y = y
        self.radius = radius
        self.direction = direction
        self.velocity = 7 * direction

    def init_images(self):
            pass

    def draw(self, window):
        pygame.draw.circle(window, pygame.Color("red"), (self.x, self.y), self.radius)

    def update(self):
        self.x += self.velocity
