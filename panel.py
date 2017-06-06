# -*- coding: utf-8 -*-

# File panel.py contenente la classe panel (pannello posti liberi), il
# metodo main e le classi per la gestione della comunicazione tra
# processi via socket.

import pygame
import random
import settings as opt
import logging
import sys
import time

info = logging.info

# eventuali globali
WIDTH = 350
HEIGHT = 250
WINDOW_TITLE = "Pannello posti liberi"
THICKNESS = 2
ZONEX = WIDTH - 300
ZONE1Y = 60
ZONE2Y = 115
ZONE3Y = 170
FMTX = 120
CIRCLEX = 260
# ******************************************************

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
            print("PanelSocketServer running on port %d" % port)
        except socket.error:
            raise Exception("PanelSocketServer: error creating socket")

    def _get_sensors_state(self):
        return [(s.zone,s.active) for s in self.game.sensors]

    def run(self):
        while 1:
            channel, client = self.sock.accept()
            info("server got connection from %s", str(client))
            ss = [str(str(k) + (v and 'x' or '_'))
                  for k,v in self._get_sensors_state()]
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
            raise Exception("PanelSocketClient: error creating socket")
            sys.exit(1)
        self.sock.connect((self.host, self.port))
        data = self.sock.recv(1024)
        self.sock.close()
        return data

#*************************************************************
# classe Panel
class Panel:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.running = True
        self.header = "ISTITUTO DI ISTRUZIONE LA ROSA BIANCA"
        self.footer = "CAVALESE - "
        self.time = time.strftime("%H:%M")

        # coppie (numero di posti liberi, colore)
        self.zone1 = list((0,opt.RED))
        self.zone2 = list((0,opt.RED))
        self.zone3 = list((0,opt.RED))

        with open("port_panel.txt") as file:
            self.port = int(file.read())
        self.client = PanelSocketClient(port=self.port)

    def events(self):
        for event in pygame.event.get():
            # QUIT
            if (event.type == pygame.QUIT or
                event.type == pygame.KEYDOWN and
                event.key in [pygame.K_q, pygame.K_ESCAPE]):
                self.running = False
                break

    def update(self):
       self.time = time.strftime("%H:%M")
       data = self.client.get_data()
       # reset list
       self.zone1[0] = 0
       self.zone1[1] = opt.RED
       self.zone2[0] = 0
       self.zone2[1] = opt.RED
       self.zone3[0] = 0
       self.zone3[1] = opt.RED

       # working with data
       for d in data.split(' '):
           if '0' in d[0]:
               if d[1] == '_':self.zone1[0] += 1
           elif '1' in d[0]:
               if d[1] == '_':self.zone2[0] += 1
           elif '2' in d[0]:
               if d[1] == '_':self.zone3[0] += 1

       if self.zone1[0] > 0:
           self.zone1[1] = opt.GREEN
       if self.zone2[0] > 0:
           self.zone2[1] = opt.GREEN
       if self.zone3[0] > 0:
           self.zone3[1] = opt.GREEN


    def draw(self):

        pygame.font.init()
        self.headerFont = pygame.font.SysFont('Times New Roman', 15)
        self.zoneFont = pygame.font.SysFont('Comics Sans', 25)

        blit = self.screen.blit
        lines = pygame.draw.lines

        self.screen.fill(opt.LIGHTBLUE)
        self.headerSurface = self.headerFont.render(self.header, False, opt.WHITE)
        blit(self.headerSurface,(25,10))
        lines(self.screen, opt.WHITE, False, [(0,35),(WIDTH,35)], THICKNESS)
        lines(self.screen, opt.WHITE, False, [(0,HEIGHT - 35),(WIDTH,HEIGHT - 35)], THICKNESS)
        render = self.zoneFont.render
        blit(render("ZONA 1", False, opt.WHITE), (ZONEX, ZONE1Y))
        blit(render("ZONA 2", False, opt.WHITE), (ZONEX, ZONE2Y))
        blit(render("ZONA 3", False, opt.WHITE), (ZONEX, ZONE3Y))

        self.freePlaces = pygame.font.SysFont('Comics Sans', 25)

        fmt = "         %s         "
        render = self.freePlaces.render
        blit(render(fmt % (self.zone1[0]), False, (255,128,0), opt.BLACK), (FMTX,ZONE1Y))
        blit(render(fmt % (self.zone2[0]), False, (255,128,0), opt.BLACK), (FMTX,ZONE2Y))
        blit(render(fmt % (self.zone3[0]), False, (255,128,0), opt.BLACK), (FMTX,ZONE3Y))

        pygame.draw.circle(self.screen, self.zone1[1], (CIRCLEX,ZONE1Y + 10), 12, 0)
        pygame.draw.circle(self.screen, self.zone2[1], (CIRCLEX,ZONE2Y + 10), 12, 0)
        pygame.draw.circle(self.screen, self.zone3[1], (CIRCLEX,ZONE3Y + 10), 12, 0)
        self.footerFont = pygame.font.SysFont('Comics Sans', 22)
        self.footerSurface = self.footerFont.render(self.footer+self.time, False, opt.WHITE)
        self.screen.blit(self.footerSurface,(105,HEIGHT - 25))
        # aggiorno il display
        pygame.display.flip()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

def main():
    try:
        p = Panel()
        p.run()
    finally:
        pygame.quit()

if __name__ == "__main__":
    sys.exit(main())
