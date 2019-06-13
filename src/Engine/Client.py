import pygame
import pygame.locals
import socket
import select
import random
import time
from src.Assets import settings
from threading import Thread, Lock, active_count

def get_constants(prefix):
    """Create a dictionary mapping socket module constants to their names."""
    return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )

#global running

class Client():
  def __init__(self, player, players, enemies, addr="127.0.0.1", tcp_port=8080, udp_port=9090):
    self.lock = Lock()
    self.enemies = enemies
    self.me = player
    self.players = players
    self.init_tcp_server(addr, tcp_port)
    self.init_udp_server(addr, udp_port)

  def init_tcp_server(self, address, port):
    families = get_constants('AF_')
    types = get_constants('SOCK_')
    protocols = get_constants('IPPROTO_')
    self.tcp_sock = socket.create_connection((address, port))
    self.id = self.tcp_sock.recv(4).decode()
    print("My player ID: " + self.id)
    #self.tcp_sock.setblocking(0)
    print ('Family  :', families[self.tcp_sock.family])
    print ('Type    :', types[self.tcp_sock.type])
    print ('Protocol:', protocols[self.tcp_sock.proto])

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

  def run_tcp(self):
    try:
      while True:#running:
        self.tcp_sock.sendall(f"u{self.me.rect.x},{self.me.rect.y}|".encode())
        time.sleep(0.01)
    finally:
      self.tcp_sock.send(b'd|')
      self.tcp_sock.shutdown(socket.SHUT_RDWR)
      self.tcp_sock.close()
      print("TCP socket closed")

  def decode_positions(self, data):
    players_list = data.split('|')[0:-1]

    for player in players_list:
      player_data = player.split('+')
      player_id = player_data[0]
      player_pos = player_data[1].split(',')
      self.players[player_id] = tuple([int(x) for x in player_pos])

  def run_udp(self):
    epoll = select.epoll()
    epoll.register(self.udp_socket.fileno(), select.EPOLLIN)
    try:
      while True:#running:
        events = epoll.poll()
        for fileno, event in events:
            if event & select.EPOLLIN:
              data = self.udp_socket.recv(256)
              self.decode_positions(data.decode())
            elif event & select.EPOLLHUP:
              epoll.unregister(fileno)

        #self.lock.acquire()
        #for id, pos in self.players.items():
        #  print(f"Player {id} pos: {pos}")
        #self.lock.release()

    finally:
      epoll.unregister(self.udp_socket.fileno())
      epoll.close()
      self.udp_socket.close()
      print("UDP server closed")
