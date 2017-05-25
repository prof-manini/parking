import time
import random
import pickle
import pygame
import settings as opt
import car
import car_sensor
import stairs
from vec import Vec2d as Vector

collide = pygame.sprite.spritecollide

import logging
info = logging.info
debug = logging.debug
error = logging.error
warning = logging.warning

#
class Game:

    def __init__(self):
        pygame.init()
        window_size = [opt.WIDTH,opt.HEIGHT]
        self.screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        pygame.display.set_caption(opt.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_data()
        self.font_name = pygame.font.match_font(opt.FONT_NAME)
        self.last_mouse_pos = (0,0)
        self.moving_object = None
        self.backup_file = "parking.state"
        self.random_mode = False

        self.original_background = pygame.image.load("img/parking-background-0.jpg")
        self.current_background = pygame.transform.scale(self.original_background, (opt.WIDTH,                                                           opt.HEIGHT))


#
    def _do_help(self):
        print("""
  You can use the followinf keys at any time:

  s: add a sensor
  c: add a car
  l: give some log information (if run with -v option)
  b: save state to file
  r: restore state from file
  p: park one car (choosen at random)
  u: make a car leave (choosen at random)
  x: toggle random parking and leaving of cars
  +/=: double random movement interval
  -/_: halve random movement interval
  h/?: show this help :)
  """)

#
    def start_new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.sensors = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.stairs = pygame.sprite.Group()
        # for _ in range(2):
        #     self._add_sensor()

        # for _ in range(1):
        #     self._add_car()

#
    def _add_sensor(self, pos=None):
        c = len(self.sensors)
        if pos == None:
            pos = (100, c * 50 + 100)
            if pos[1] > opt.HEIGHT - 50:
                error("No room left for sensor")
                return
        zone = c % 3
        s = car_sensor.CarSensor(self, pos, zone)
        debug("Adding sensor n. %d at %s in zone %d", s.oid, pos, zone)

#
    def _add_car(self, pos=None):
        c = len(self.cars)
        if pos == None:
            pos = (opt.WIDTH - 100, c * 50 + 100)
            if pos[1] > opt.HEIGHT - 50:
                error("No room left for car")
                return
        s = car.Car(self, pos)
        debug("Adding car n. %d at %s", s.oid, pos)

#
    def _add_stairs(self, pos=None):
        c = len(self.stairs)
        if pos == None:
            if c == 0:
                pos = (200, 50)
            elif c == 1:
                pos = (200, opt.HEIGHT - 50)
            else:
                error("No room left for car")
                return
        s = stairs.Stairs(self, pos)
        debug("Adding stairs n. %d at %s", s.oid, pos)

#
    def load_data(self):
        pass

#
    def events(self):
        for event in pygame.event.get():

            # QUIT
            if (event.type == pygame.QUIT or
                event.type == pygame.KEYDOWN and
                event.key in [pygame.K_q, pygame.K_ESCAPE]):
                self.running = False
                break
            # RESIZE							########################
            if event.type == pygame.VIDEORESIZE :
                width, height = event.size
                if (width < opt.WIDTH  or
                    height < opt.HEIGHT):
                        width = opt.WIDTH
                        height = opt.HEIGHT
                self.screen = pygame.display.set_mode((width,height),
                pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)

                self.current_background = pygame.transform.scale(self.original_background,                                                                       (width,height))



            #left mouse click on object (start dragging it)?
            if (event.type == pygame.MOUSEBUTTONDOWN):
                self.last_mouse_pos = pygame.mouse.get_pos()
                left, _, _ = pygame.mouse.get_pressed()
                if left:
                    mouse_pos = self.last_mouse_pos = pygame.mouse.get_pos()
                    debug("mouse down at: %s" % str(pygame.mouse.get_pos()))
                    for i, s in enumerate(self.all_sprites):
                        r = s.rect
                        if r.collidepoint(*mouse_pos):
                            debug("Click at %s on %s %d", str(mouse_pos),
                                  s.__class__.__name__, s.oid)
                            self.moving_object = s

            # left mouse released (stop dragging)?
            if (event.type == pygame.MOUSEBUTTONUP):
                self.moving_object = None

            # drag sensor
            if self.moving_object:
                pos = Vector(pygame.mouse.get_pos())
                self.moving_object.pos = pos

            # commands keys --------------------
            if (event.type == pygame.KEYDOWN):

                k,p,s = event.key, pygame, self

                if   k in [p.K_s]: s._add_sensor()
                elif k in [p.K_c]: s._add_car()
                elif k in [p.K_l]: s._do_log()
                elif k in [p.K_b]: s._do_backup()
                elif k in [p.K_r]: s._do_restore()
                elif k in [p.K_p]: s._do_park()
                elif k in [p.K_u]: s._do_unpark()
                elif k in [p.K_x]: s._do_random_park_unpark()
                elif k in [p.K_PLUS, p.K_EQUALS]:
                    s._do_change_random_interval(factor=2)
                elif k in [p.K_MINUS, p.K_UNDERSCORE]:
                    s._do_change_random_interval(factor=.5)
                elif k in [p.K_h, p.K_QUESTION]:
                    s._do_help()
                elif k in [p.K_t]:
                    s._add_stairs()
                else:
                    error("No command bound to '%s' key.", event.unicode)

#
    def _do_change_random_interval(self, factor):
        opt.RANDOM_MOVES_INTERVAL *= factor

#
    def _do_random_park_unpark(self):
        self.last_random_time = time.time()
        self.random_mode = not self.random_mode

    def _do_unpark(self, car=None):
        if car is None:
            ss = [s for s in self.sensors if s.car]
            if not ss:
                if not self.random_mode:
                    error("No parked cars")
                return
            oid = random.choice([s.oid for s in ss])
            sensor = [o for o in ss if o.oid == oid][0]
            car = sensor.car
        ss = [s for s in self.sensors
              if s.car and s.car == car]

        # this should never happen :)
        if not ss:
            if not self.random_mode:
                error("No sensor for car %d", car.oid)
            return

        sensor = ss[0]
        car.unpark_from_sensor(sensor)

#
    def _do_park(self, car=None, sensor=None):

        # check sensor before car ... see below
        if sensor is None:
            ss = [s for s in self.sensors
                  if not (s.car or s.reserved)]
            if not ss:
                if not self.random_mode:
                    error("No free sensors")
                return
            oid = random.choice([s.oid for s in ss])
            sensor = [o for o in ss if o.oid == oid][0]

        if car is None:
            # if there are no sensors, CC will be empty
            # and FF will be equal to self.cars, so you
            # end up with a car to park but no sensors!

            if opt.RANDOM_PARK_TRY_ANY_CAR:
                cc = [o for o in self.cars if o.waiting]
                if not cc:
                    if not self.random_mode:
                        error("No cars to park")
                    return
                car = random.choice(cc)
            else:
                # parked cars
                pp = [s.car for s in self.sensors
                      if s.car]
                # free cars
                ff = [c for c in self.cars
                      if not (c in pp or c.move_target or c.leaving)]
                if not ff:
                    if not self.random_mode:
                        error("No cars to park")
                    return
                oid = min([c.oid for c in ff])
                car = [o for o in ff if o.oid == oid][0]
        car.park_at_sensor(sensor)

#
    def _do_backup(self, file=None):
        if file is None:
            file = self.backup_file
        debug("Saving state to '%s'", file)
        with open(file, "wb") as file:
            pickle.dump((self.sensors, self.cars), file)

    def _do_restore(self, file=None):
        if file is None:
            file = self.backup_file
        debug("Restoring state from '%s'", file)
        try:
            with open(file, "rb") as file:
                ss, cc = pickle.load(file)
        except IOError:
            debug("Failed to open state backup file '%s'", file)
            return
        for o in ss:
            self._add_sensor(o.pos)
        for o in cc:
            self._add_car(o.pos)

#
    def _do_log(self):
        cc = len(self.cars)
        sc = len(self.sensors)
        info("We have %d car%s and %d sensor%s",
             cc, cc > 1 and "s" or "",
             sc, sc > 1 and "s" or "")
        oo = [(s,s.car) for s in self.sensors if s.car]
        if oo:
            for s,c in oo:
                info("Car %d parked at %d", s.car.oid, s.oid)
        else:
            info("No cars parked.")
        out = [s.get_access_log_string()
               for s in sorted(self.sensors)]
        out = "\n".join(out)
        debug("Access log:\n%s", out)

#
    def get_access_data(self):
        return {s.oid: s.access_log
                for s in sorted(self.sensors)}

#
    def draw(self):

        self.screen.blit(self.current_background, [0,0])
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

#
    def run(self):
        while self.running:
            self.clock.tick(opt.FPS)
            self.events()
            self.update()
            self.draw()

#
    def update(self):
        self.all_sprites.update()

        if self.moving_object in self.cars:
            ss = [collide(self.moving_object, self.sensors, False)]
            for s in ss[0]: # WHY is SS a LOL?
                if not s.active:
                    debug("Sensor %s activated by car %d",
                          s.oid, self.moving_object.oid)
                    s.activate(True)

        if self.random_mode:
            if (time.time() - self.last_random_time >
                opt.RANDOM_MOVES_INTERVAL):
                key = random.choice( (pygame.K_p, pygame.K_u) )
                pygame.event.post(pygame.event.Event(
                    pygame.KEYDOWN, key=key))
                self.last_random_time = time.time()

#
    def draw_text(self, text, size, color, pos):
        font = pygame.font.Font(self.font_name, size)
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        rect.midtop = pos
        self.screen.blit(surf, rect)
