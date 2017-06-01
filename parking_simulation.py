# -*- coding:utf-8 -*-

import pygame
import random
import os
import argparse
import settings as opt
import logging
from panel import PanelSocketServer

info = logging.info
debug = logging.debug
error = logging.error
warning = logging.warning

progname = os.path.basename(__file__)
collide = pygame.sprite.spritecollide

GAME = None

def setup_logging(opt):
    """Configure basic logging."""

    log_level = opt.verbose and logging.DEBUG or logging.INFO
    logging.basicConfig(level=log_level,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%d-%m %H:%M:%S',
        filename="parking.log",
        filemode='w')

    logger = logging.getLogger()
    logger.setLevel(log_level)

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)
    logger.addHandler(console)

def parse_args(args):
    """Parse command line ARGS. Return 'mapping' (from  argparse)."""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    add = parser.add_argument
    add("-v", "--verbose", action="store_true",
        help="Makes program more chatty.")
    add("--width", type=int, default=opt.WIDTH,
        help="Screen width.")
    add("--height", type=int, default=opt.HEIGHT,
        help="Screen height.")
    add("--fps", type=int, default=60,
        help="Screen update frequency.")
    add("--random-moves-interval", type=float, default=0.5,
        help="Time between consecutive random moves.")

    return parser.parse_args(args)

def do_options(args):
    opt.FPS = args.fps
    opt.WIDTH = args.width
    opt.HEIGHT = args.height
    opt.RANDOM_MOVES_INTERVAL = args.random_moves_interval

#
import socket
class SocketServer():

    def __init__(self,  game, host="", port=8000):
        try:
            self.game = game
            port = random.randint(2000, 9000)
            with open("port.txt", "w") as file:
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
class SocketClient():

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

def main(args):
    """Main program."""

    global GAME

    import threading
    import game
    import sys
    args = parse_args(args)    # parse command line arguments
    setup_logging(args)        # config logging
    do_options(args)

    try:
        pygame.init()
        GAME = g = game.Game()

        s = SocketServer(g)
        p = PanelSocketServer(g)
        pt = threading.Thread(target=p.run)
        pt.daemon = True

        pt.start()
        t = threading.Thread(target=s.run)
        t.daemon = True
        t.start()

        while g.running:
            g.start_new()
            g.run()
        debug("Quitting pygame...")

    finally:
        pygame.quit()
    return 0

if __name__ == "__main__":

    import sys
    args = sys.argv[1:]
    sys.exit(main(args))
