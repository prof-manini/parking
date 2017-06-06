# -*- coding:utf-8 -*-
#
import pygame
import settings as opt


import log_file
to_file = log_file.to_file

import logging
info = logging.info
debug = logging.debug
error = logging.error
warning = logging.warning
collide = pygame.sprite.spritecollide

from vec import Vec2d as Vector

class CarSensor(pygame.sprite.Sprite):
    oid = 0
    def __init__(self, world, pos, zone=0):
        self._layer = opt.CAR_SENSOR_LAYER
        self.groups = world.all_sprites, world.sensors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.oid = CarSensor.oid
        CarSensor.oid += 1
        self.world = world
        self.zone = zone
        self.image = pygame.Surface((30, 30))
        self.color = [opt.LIGHT_GREEN, opt.GREEN, opt.DARK_GREEN][zone]
        print(self.color)
        self.image.fill(self.color)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.pos = Vector(pos)
        self._active = False
        self.car = None
        self.reserved = False
        self.access_log = dict()

#
    @property
    def active(self):
        return self._active

#
    def __cmp__(self, other):
        return cmp(self.oid, other.oid)

#
    def store_car_access(self, car, entering, when=None):
        if when is None:
            when = opt.now()
        if car.oid not in self.access_log:
            debug("Car %s is a new entry in sensor %d",
                  car.oid, self.oid)
            self.access_log[car.oid] = list()
        car_data = self.access_log[car.oid]
        if entering:
            car_data.append( [when] )
        else:
            car_data[-1].append(when)
        self.access_log[car.oid] = car_data[:]

#
    def get_access_log_string(self):
        log = self.access_log
        if not log:
            return ""
        out = ["sensor: %d as %d log entries" % (self.oid, len(log))]
        for car, data in sorted(log.items()):
            out.append("  car: %d" % car)
            for p in data:
                # p is usually a pair of "instants" (in, out) recorded
                # as seconds, but if a car is still parked, the "out"
                # instant is missing and p contains just the "in"
                # info.
                try:
                    i,o = p
                    i = opt.format_sec(sec=i)
                    o = opt.format_sec(sec=o)
                except ValueError:
                    i = p[0]
                    i = opt.format_sec(i)
                    o = "NOT YET..."
                out.append("    %s -> %s" % (i,o))
        out = "\n".join(out)
        return "\n" + out

#
    def update(self):
        self.rect.center = self.pos
        cc = collide(self, self.world.cars, False)
        if self.active:
            if not cc:
                self.activate(False)
                self.store_car_access(self.car, entering=False)
                debug("Car %d left sensor %d at %s",
                      self.car.oid, self.oid, opt.str_now())
                to_file("%d %d %d %s"
                        % (self.car.oid, self.oid, 0, opt.str_now()))
                self.car = None
        else:
            if cc:
                for c in cc:
                    self.activate(True)
                    self.car = c
                    self.reserved = False
                    self.store_car_access(self.car, entering=True)
                    debug("Car %d arrived at sensor %d at %s",
                           c.oid, self.oid, opt.str_now())
                    to_file("%d %d %d %s"
                          % (self.car.oid, self.oid, 1, opt.str_now()))
        if self.reserved:
            self.image.fill(opt.GRAY)
        f = pygame.font.SysFont("Arial", 25)
        t = f.render(str(self.oid), 0, opt.WHITE)
        pygame.Surface.blit(self.image, t, (10,0))

#
    def activate(self, value):
        self._active = value
        self.image.fill(self.active and opt.RED or self.color)

    def __getstate__(self):
        return {"pos": self.pos,
                "zone": self.zone}

    def __setstate__(self, state):
        self.pos = state["pos"]
        self.zone = state["zone"]
