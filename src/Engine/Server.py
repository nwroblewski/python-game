import socket
import select
import sys
import pickle
from src.Assets import settings
import pygame
import pygame.locals
from threading import Lock, Thread, active_count

class Server(object):
  def __init__(self, entities, collisionDetector, enemies, address = 'localhost', port=50000):
    self.lock = Lock()
    self.enemies = []
    self.sock_in = self.init_tcp_server(address, port)
    self.sock_out = self.init_tcp_server(address, port + 10)
    self.players = {}   # fileno (player_id) -> pos (2-length tuple)
    self.running = True
    
  def init_tcp_server(self, address, port):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind((address, port))
    tcp_socket.listen(1)
    tcp_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    return tcp_socket

  def run(self):
    in_thread = Thread(target=self.run_in)
    out_thread = Thread(target=self.run_out)
    in_thread.start()
    out_thread.start()
    print(f"{active_count()} threads are running")

    while True:
      for e in pygame.event.get():
        if e.type == pygame.locals.QUIT or (e.type == pygame.locals.KEYDOWN and e.key == pygame.locals.K_ESCAPE):
          self.running = False
          return

  def register_player(self, fileno):
    print(f"Registering player {fileno}")
    self.lock.acquire()
    self.players[fileno] = settings.STARTING_POS
    self.lock.release()
    
  def unregister_player(self, fileno):
    self.lock.acquire()
    del self.players[fileno]
    self.lock.release()
    print(f"Player {fileno} disconnected")

  def update_position(self, addr, pos):
    self.lock.acquire()
    self.players[addr] = pos
    self.lock.release()

  def parse_msg(self, msg, fileno):
    msg_list = msg.split('|')[0:-1]

    for msg in msg_list:
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

  def run_in(self):
    epoll = select.epoll()
    epoll.register(self.sock_in.fileno(), select.EPOLLIN)
    try:
      connections = {}
      while self.running:
        events = epoll.poll(1)
        for fileno, event in events:
            if fileno == self.sock_in.fileno():
              connection, address = self.sock_in.accept()
              #connection.setblocking(0)
              epoll.register(connection.fileno(), select.EPOLLIN)
              connections[connection.fileno()] = connection
              self.register_player(connection.fileno())
              connection.send(str(connection.fileno()).encode())
            elif event & select.EPOLLIN:
              msg = connections[fileno].recv(256)
              self.parse_msg(msg.decode(), fileno)
            elif event & select.EPOLLHUP:
              epoll.unregister(fileno)
              connections[fileno].close()
              self.unregister_player(fileno)
              del connections[fileno]

    finally:
      epoll.unregister(self.sock_in.fileno())
      epoll.close()
      self.sock_in.shutdown(socket.SHUT_RDWR)
      self.sock_in.close()
      print("TCP server (IN) closed")

  def encode_positions(self):
    result = ""
    self.lock.acquire()
    for player_id, pos in self.players.items():
      print(f"Player {player_id} pos:{pos[0]},{pos[1]}")
      result += f"{player_id}+{pos[0]},{pos[1]}|"
    self.lock.release()
    return result.encode()

  def run_out(self):
    epoll = select.epoll()
    epoll.register(self.sock_out.fileno(), select.EPOLLOUT | select.EPOLLIN)
    try:
      connections = {}
      while self.running:
        events = epoll.poll(1)
        for fileno, event in events:
            if fileno == self.sock_out.fileno():
              connection, address = self.sock_out.accept()
              #connection.setblocking(0)
              epoll.register(connection.fileno(), select.EPOLLOUT)
              connections[connection.fileno()] = connection
              #connection.send(str(connection.fileno()).encode())
            elif event & select.EPOLLOUT:
              response = self.encode_positions()
              try:
                connections[fileno].send(response)
                #pickle.dumps(self.enemies)
              except BrokenPipeError:
                print("Its ok, just did not delete connection on time")
                epoll.unregister(fileno)
                connections[fileno].close()
                epoll.unregister(fileno)
                del connections[fileno]
            elif event & select.EPOLLHUP:
              epoll.unregister(fileno)
              connections[fileno].close()
              epoll.unregister(fileno)
              del connections[fileno]

    finally:
      epoll.unregister(self.sock_out.fileno())
      epoll.close()
      self.sock_out.shutdown(socket.SHUT_RDWR)
      self.sock_out.close()
      print("TCP server (OUT) closed")
