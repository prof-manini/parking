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
WIDTH = 600
HEIGHT = 400
WINDOW_TITLE = "Pannello posti liberi"
THICKNESS = 2

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
        d = {s.zone:s.active for s in self.game.sensors}
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
        self.header = "PARCHEGGIO ISTITUTO DI ISTRUZIONE LA ROSA BIANCA"
        self.footer = "CAVALESE - "
        self.time = time.strftime("%H:%M")

        # coppie (numero di posti liberi, stringa colore)

        self.zone1 = list((10, "WHITE"))
        self.zone2 = list((20, "RED"))
        self.zone3 = list(( 5, "GREEN"))

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
       print(data)
       #work with information

    def draw(self):

        pygame.font.init()
        self.headerFont = pygame.font.SysFont('Times New Roman', 20)
        self.zoneFont = pygame.font.SysFont('Comics Sans', 32)

        blit = self.screen.blit
        lines = pygame.draw.lines

        self.screen.fill(opt.LIGHTBLUE)
        self.headerSurface = self.headerFont.render(self.header, False, opt.WHITE)
        blit(self.headerSurface,(35,25))
        lines(self.screen, opt.WHITE, False, [(0,70),(WIDTH,70)], THICKNESS)
        lines(self.screen, opt.WHITE, False, [(0,HEIGHT - 70),(WIDTH,HEIGHT -70)], THICKNESS)
        render = self.zoneFont.render
        blit(render("ZONA 1", False, opt.WHITE), (110, 135))
        blit(render("ZONA 2", False, opt.WHITE), (110, 190))
        blit(render("ZONA 3", False, opt.WHITE), (110, 245))

        self.freePlaces = pygame.font.SysFont('Comics Sans', 32)

        fmt = "         %s         "
        render = self.freePlaces.render
        blit(render(fmt % (self.zone1[0]), False, (255,128,0), opt.BLACK), (230,135))
        blit(render(fmt % (self.zone2[0]), False, (255,128,0), opt.BLACK), (230,190))
        blit(render(fmt % (self.zone3[0]), False, (255,128,0), opt.BLACK), (230,245))

        # Anche qui i colori sono stati inseriti per provare il
        # codice.  Nel programma vero dovranno cambiare in base al
        # numero di posti liberi.

        pygame.draw.circle(self.screen, opt.GREEN, (450,145), 12, 0)
        pygame.draw.circle(self.screen, opt.GREEN, (450,200), 12, 0)
        pygame.draw.circle(self.screen, opt.RED, (450,255), 12, 0)
        self.footerFont = pygame.font.SysFont('Comics Sans', 32)
        self.footerSurface = self.footerFont.render(self.footer+self.time, False, opt.WHITE)
        self.screen.blit(self.footerSurface,(170,355))
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
