#!/usr/bin/env/python3

import pygame
import numpy as np

pygame.init()
bg_image = pygame.image.load("Assets/PixelArt.png")
window_width = 800
window_height = 640
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Gameee")

x = 50
y = 500
width = 32
height = 64
speed = 5

jumping = False
jump_count = 10

clock = pygame.time.Clock()
# pygame.mixer.music.load('Assets/muzyczka.wav')
running = True

# pygame.mixer.music.play(-1)
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if jumping:
        print(y)
        if jump_count >= -10:
            direction = 1
            if jump_count < 0:
                direction = -1
            y -= (jump_count ** 2) * 0.5 * direction
            jump_count -= 1

        else:
            jumping = False
            jump_count = 10
    else:
        if keys[pygame.K_SPACE]:
            jumping = True

        if keys[pygame.K_DOWN] and y < window_height - height - speed:
            y += speed

    if keys[pygame.K_RIGHT] and x < window_width - width - speed:
        x += speed

    if keys[pygame.K_LEFT] and x > speed:
        x -= speed



    # print(y,y_speed)

    window.fill((0, 0, 0))
    window.blit(bg_image, (0, 0))

    pygame.draw.rect(window, (255, 0, 0), (x, y, width, height))

    pygame.display.update()

    clock.tick(40)
pygame.quit()

