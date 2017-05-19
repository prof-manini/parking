# -*- coding: utf-8 -*-

# File panel.py contenente la classe panel (pannello posti liberi), il metodo
# main e le classi per la gestione della comunicazione tra processi via socket.
import pygame
import random
import os
import argparse
import settings as opt
import logging
import sys
import time

# eventuali globali
WIDTH = 600
HEIGHT = 400
TITLE = "Pannello posti liberi"
THICKNESS = 2

#*****************

# classe Panel
class Panel:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption(TITLE)
        self.running = True
        self.zone1 = list() #lista compredente due elementi, il primo è il numero di posti liberi ed il secondo è la stringa contenente il colore
        self.zone2 = list()
        self.zone3 = list()

    def events(self):
        for event in pygame.event.get():
            # QUIT
            if (event.type == pygame.QUIT or
                event.type == pygame.KEYDOWN and
                event.key in [pygame.K_q, pygame.K_ESCAPE]):
                self.running = False
                break

    def update(self):
        pass

    def draw(self):
        self.screen.fill(opt.LIGHTBLUE)
        pygame.font.init()
        self.headerFont = pygame.font.SysFont('TimesNewRoman', 20)
        self.headerSurface = self.headerFont.render("PARCHEGGIO ISTITUTO D'ISTRUZIONE LA ROSA BIANCA", False, opt.WHITE)
        self.screen.blit(self.headerSurface,(35,25))
        pygame.draw.lines(self.screen, opt.WHITE, False, [(0,70),(WIDTH,70)], THICKNESS)
        pygame.draw.lines(self.screen, opt.WHITE, False, [(0,HEIGHT - 70),(WIDTH,HEIGHT -70)], THICKNESS)


        pygame.display.flip()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()



# main
def main():
    p = Panel()
    p.run()


if __name__ == "__main__":
    sys.exit(main())



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
