import socket
import select
import sys
from src.Assets import settings
import pygame
import pygame.locals
from threading import Lock, Thread, active_count

#global running

class Server(object):
  def __init__(self, entities, collisionDetector, address = '127.0.0.1', tcp_port=8080, udp_port=9090):
    self.lock = Lock()
    self.init_tcp_server(address, tcp_port)
    self.init_udp_server(address, udp_port)
    self.players = {}
    
  def init_tcp_server(self, address, port):
    self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.tcp_socket.bind((address, port))
    self.tcp_socket.listen(1)
    #self.tcp_socket.setblocking(0)
    self.tcp_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

  def init_udp_server(self, address, port):
    self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.udp_socket.bind((address, port))

  def run(self):
    #running = True
    tcp_thread = Thread(target=self.run_tcp)
    udp_thread = Thread(target=self.run_udp)
    tcp_thread.start()
    udp_thread.start()
    print(f"{active_count()} threads are running")

    while True:
      for e in pygame.event.get():
        if e.type == pygame.locals.QUIT or (e.type == pygame.locals.KEYDOWN and e.key == pygame.locals.K_ESCAPE):
          #running = False
          return

  def register_player(self, fileno):
    print(f"Registering player {fileno}")
    self.players[fileno] = settings.STARTING_POS
    
  def unregister_player(self, fileno):
    del self.players[fileno]
    print(f"Player {fileno} disconnected")

  def update_position(self, addr, pos):
    self.lock.acquire()
    self.players[addr] = pos
    self.lock.release()

  def parse_msg(self, msg, fileno):
    msg_list = msg.split('|')
    if len(msg_list) >= 2:
      msg = msg_list[-2]
    if len(msg) >= 1:
      cmd = msg[0]
      if cmd == 'u':  # Position Update
        if len(msg) >= 2 and fileno in self.players.keys():
          pos = msg[1:].split(',')
          self.update_position(fileno, pos)
      elif cmd == 'd':  # Player Quitting
        if fileno in self.players.keys():
          self.unregister_player(fileno)
      else:
        print("Unexpected: {0}".format(msg))

  def run_tcp(self):
    epoll = select.epoll()
    epoll.register(self.tcp_socket.fileno(), select.EPOLLIN)
    try:
      connections = {}
      while True:#running:
        events = epoll.poll()
        for fileno, event in events:
            if fileno == self.tcp_socket.fileno():
              connection, address = self.tcp_socket.accept()
              #connection.setblocking(0)
              epoll.register(connection.fileno(), select.EPOLLIN)
              connections[connection.fileno()] = connection
              self.register_player(connection.fileno())
              connection.send(str(connection.fileno()).encode())
            elif event & select.EPOLLIN:
              msg = connections[fileno].recv(32)
              self.parse_msg(msg.decode(), fileno)
            elif event & select.EPOLLHUP:
              epoll.unregister(fileno)
              connections[fileno].close()
              self.unregister_player(fileno)
              del connections[fileno]
        #self.lock.acquire()
        #for addr, pos in self.players.items():
        #  print(f"Player {addr} pos: {pos}")
        #self.lock.release()

    finally:
      epoll.unregister(self.tcp_socket.fileno())
      epoll.close()
      self.tcp_socket.shutdown(socket.SHUT_RDWR)
      self.tcp_socket.close()
      print("TCP server closed")

  def encode_positions(self):
    result = ""
    self.lock.acquire()
    for fileno, pos in self.players.items():
      result += f"{fileno}+{pos[0]},{pos[1]}|"
    self.lock.release()
    return result.encode()

  def run_udp(self):
    epoll = select.epoll()
    epoll.register(self.udp_socket.fileno(), select.EPOLLOUT)
    try:
      while True:#running:
        events = epoll.poll()
        for fileno, event in events:
            if event & select.EPOLLOUT:
              response = self.encode_positions()
              self.udp_socket.sendto(response, ('127.0.0.1', 9090))
            elif event & select.EPOLLHUP:
              epoll.unregister(fileno)

    finally:
      epoll.unregister(self.udp_socket.fileno())
      epoll.close()
      self.udp_socket.close()
      print("UDP server closed")
