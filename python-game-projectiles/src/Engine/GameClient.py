import pygame
import pygame.locals
import socket
import select
import random
import time
from src.Assets import settings

class GameClient():
  def __init__(self, entities, window, bg, addr="127.0.0.1", serverport=9009):
    self.clientport = random.randrange(8000, 8999)
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind to localhost - set to external ip to connect from other computers
    self.conn.bind(("127.0.0.1", self.clientport))
    self.addr = addr
    self.serverport = serverport
    
    self.read_list = [self.conn]
    self.write_list = []
    
    self.entities = entities
    self.screen = window
    self.setup_pygame()
    self.players = []
    self.bg = bg

  def add_player(self, player):
    self.players.append(player)
    player.rect = player.image.get_rect(topleft=settings.STARTING_POS)
  
  def setup_pygame(self):    
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.locals.QUIT,
                              pygame.locals.KEYDOWN])
    #pygame.key.set_repeat(50, 50)
    
  def run(self):
    running = True
    clock = pygame.time.Clock()
    
    try:
      # Initialize connection to server
      self.conn.sendto(b'c', (self.addr, self.serverport))
      while running:
        clock.tick(settings.FPS)
        
        # select on specified file descriptors
        readable, writable, exceptional = (
            select.select(self.read_list, self.write_list, [], 0)
        )
        for f in readable:
          if f is self.conn:
            msg, addr = f.recvfrom(32)
            self.screen.blit(self.bg, (0,0))  # Draw the background
            for position in msg.decode().split('|'):
              x, sep, y = position.partition(',')
              try:
                print(int(x))
                print(int(y))
                #self.entities.update()
                self.player[0].rect.left = int(x)
                self.player[0].rect.top = int(y)
                self.player[0].update_relative_position(self.player[0].rect.right + self.entities.cam.x)
              except:
                pass  # If something goes wrong, don't draw anything.
            

        for event in pygame.event.get():
          if event.type == pygame.QUIT or event.type == pygame.locals.QUIT:
            running = False
            break
          elif event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_UP:
              self.conn.sendto(b'uu', (self.addr, self.serverport))
            elif event.key == pygame.locals.K_LEFT:
              self.conn.sendto(b'ul', (self.addr, self.serverport))
            elif event.key == pygame.locals.K_RIGHT:
              self.conn.sendto(b'ur', (self.addr, self.serverport))
            elif event.key == pygame.locals.K_ESCAPE:
              return
            pygame.event.clear(pygame.locals.KEYDOWN)

        self.entities.draw(self.screen)
        pygame.display.update()
    finally:
      self.conn.sendto(b'd', (self.addr, self.serverport))