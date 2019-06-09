import pygame
import pygame.locals
import socket
import select
import random
import time
from src.Assets import settings

def get_constants(prefix):
    """Create a dictionary mapping socket module constants to their names."""
    return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )

class GameClient():
  def __init__(self, entities, window, bg, addr="127.0.0.1", serverport=8080):
    families = get_constants('AF_')
    types = get_constants('SOCK_')
    protocols = get_constants('IPPROTO_')
    # Create a TCP/IP socket
    self.sock = socket.create_connection((addr, serverport))
    self.sock.setblocking(0)
    print ('Family  :', families[self.sock.family])
    print ('Type    :', types[self.sock.type])
    print ('Protocol:', protocols[self.sock.proto])

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

  def parse_msg(self, msg):
    print("Received msg: ", msg)
    position = msg.split('|')[-1]
    x, sep, y = position.partition(',')
    self.players[0].rect.left = int(x)
    self.players[0].rect.top = int(y)

  def run(self):
    running = True
    clock = pygame.time.Clock()    
    EOL = b'|'
    epoll = select.epoll()
    epoll.register(self.sock.fileno(), select.EPOLLIN | select.EPOLLOUT)
    print("Waiting...")
    try:
      # Initialize connection to server
      connection = self.sock
      request = b''
      response = b'c|'
      connection.send(response)
      while running:
        clock.tick(settings.FPS)

        events = epoll.poll()
        for fileno, event in events:
          if event & select.EPOLLIN:
            request = connection.recv(32)
            self.parse_msg(request.decode())
          elif event & select.EPOLLOUT:
            connection.send(response)
            print("Epollout: ", response.decode())

        self.players[0].update_relative_position(self.players[0].rect.right + self.entities.cam.x)
        self.screen.blit(self.bg, (0,0))
        self.entities.draw(self.screen)
        pygame.display.update()

        response = b'u|'

        for event in pygame.event.get():
          if event.type == pygame.QUIT or event.type == pygame.locals.QUIT:
            running = False
            break
          elif event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_UP:
              response = b'uu|'
            elif event.key == pygame.locals.K_LEFT:
              response = b'ul|'
            elif event.key == pygame.locals.K_RIGHT:
              response = b'ur|'
            elif event.key == pygame.locals.K_ESCAPE:
              return
            pygame.event.clear(pygame.locals.KEYDOWN)
    finally:
      response = 'd|'
      epoll.unregister(self.sock.fileno())
      epoll.close()
      self.sock.close()
      print("Epoll unregistered, Socket closed")
