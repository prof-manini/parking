# File panel.py contenente la classe panel (pannello posti liberi), il metodo
# main e le classi per la gestione della comunicazione tra processi via socket.
import pygame
import random
import os
import argparse
import settings as opt
import logging
import time

# eventuali globali
WIDTH = 300
HEIGHT = 250
TITLE = ""



#*****************

# classe Panel
class Panel:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption()
        self.header
        self.displayZone1
        self.displayZone2
        self.displayZone3
        self.displayInfo

    def events():
        pass

    def update():
        pass

    def draw():
        pass



import socket
class PanelSocketServer():

    def __init__(self,  game, host="", port=8000):
        try:
            self.game = game
            port = random.randint(2000, 9000)
            with open("port_panel.txt", "w") as file:
                file.write("%d\n" % port)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((host, int(port)))
            self.sock.listen(5)
            print("SocketServer running on port %d" % port)
        except socket.error:
            raise Exception("SocketServer: error creating socket")

    def _get_sensors_state(self):
        d = {s.oid:s.active for s in self.game.sensors}
        return [(k,v) for k,v in sorted(d.items())]

    def run(self):
        while 1:
            channel, client = self.sock.accept()
            info("server got connection from %s", str(client))
            ss = [v and "X" or "_"
                  for _,v in self._get_sensors_state()]
            o = " ".join(ss)
            channel.send(o)
            channel.close()

#
class PanelSocketClient():

    def __init__(self, host="", port=8000):
        self.host = host
        self.port = int(port)

    def get_data(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            raise Exception("SocketClient: error creating socket")
            sys.exit(1)
        self.sock.connect((self.host, self.port))
        data = self.sock.recv(1024)
        self.sock.close()
        return data
