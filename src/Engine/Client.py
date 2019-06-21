import pygame
import pygame.locals
import socket
import select
import random
import time
from src.Assets import settings
from threading import Thread, Lock, active_count

class Client():
  def __init__(self, player, players, enemies, lock, addr="localhost", port=50000):
    self.lock = lock
    self.enemies = enemies
    self.me = player
    self.players = players
    self.init_connections(addr, port)
    self.running = True

  def init_connections(self, address, port):
    self.sock_out = socket.create_connection((address, port))
    self.id = self.sock_out.recv(4).decode()

    self.sock_in = socket.create_connection((address, port + 10))

  def run(self):
    out_thread = Thread(target=self.run_out)
    in_thread = Thread(target=self.run_in)
    out_thread.start()
    in_thread.start()
    print(f"{active_count()} threads are running")

  def run_out(self):
    try:
      while self.running:
        self.sock_out.sendall(f"u{self.me.rect.x},{self.me.rect.y}|".encode())
        time.sleep(0.01)
    finally:
      self.sock_out.send(b'd|')
      self.sock_out.shutdown(socket.SHUT_RDWR)
      self.sock_out.close()
      print("TCP socket (OUT) closed")

  def decode_positions(self, data):
    players_list = data.split('|')[0:-1]

    self.lock.acquire()
    self.players.clear()  # probably faster than searching for absent players, could receive delete info from server instead

    for player in players_list:
      player_data = player.split('+')
      if(len(player_data) == 2):
        player_id = player_data[0]
        player_pos = player_data[1].split(',')
        self.players[player_id] = tuple([int(x) for x in player_pos])
  
    self.lock.release()

  def run_in(self):
    try:
      while self.running:
        data = self.sock_in.recv(1024)
        self.decode_positions(data.decode())
        time.sleep(0.01)

        #self.lock.acquire()
        #for id, pos in self.players.items():
        #  print(f"Player {id} pos: {pos}")
        #self.lock.release()

    finally:
      self.sock_in.shutdown(socket.SHUT_RDWR)
      self.sock_in.close()
      print("TCP socket (IN) closed")

