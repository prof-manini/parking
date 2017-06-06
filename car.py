# -*- coding:utf-8 -*-

import pygame
import settings as opt

import logging
info = logging.info
debug = logging.debug
error = logging.error
warning = logging.warning

from vec import Vec2d as Vector

collide = pygame.sprite.spritecollide

class Car(pygame.sprite.Sprite):
    oid = 0
    def __init__(self, world, pos):
        self._layer = opt.CAR_LAYER
        self.groups = world.all_sprites, world.cars
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.oid = Car.oid
        Car.oid += 1
        self.world = world
        self.image = pygame.Surface((30, 30))
        self.image.fill(opt.YELLOW)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.pos = Vector(pos)
        self.move_target = None
        self._state = opt.WAITING
        self.sensor = None

    @property
    def waiting(self):
        return self._state == opt.WAITING

    @property
    def parking(self):
        return self._state == opt.PARKING

    @property
    def parked(self):
        return self._state == opt.PARKED

    @property
    def leaving(self):
        return self._state == opt.LEAVING

    def __cmp__(self, other):
        return cmp(self.oid, other.oid)

#
    def update(self):

        if self.parking: # and self.move_target:
            self.pos += self.move_step

        self.rect.center = self.pos

        ss = collide(self, self.world.sensors, False)
        if self.parking and self.move_target and self.move_target in ss:
            self.pos.x = self.move_target.pos.x + 15
            self.pos.y = self.move_target.pos.y
            self.move_target = None
            self.sensor = self.move_target
            self._state = opt.PARKED
            self.move_step = 0

        # parking
        if False and self.parking: # and self.move_target:
            self.pos += self.move_step
            if self.pos.get_distance(self.move_target.pos) < self.move_len:
                if ((self.move_target is not self.sensor) and
                    self.move_target.active):
                    warning("Car %d cannot park at %d (already taken).",
                            self.oid, self.move_target.oid)
                    self.unpark_from_sensor(self.move_target)
                else:
                    self.pos.x = self.move_target.pos.x + 15
                    self.pos.y = self.move_target.pos.y
                    self.move_target = None
                    self.sensor = self.move_target

        # leaving
        if self.leaving:
            self.pos += self.move_step
            if self.pos[0] > opt.WIDTH - 30:
                self._state = opt.WAITING
                self.move_step = 0

        # update
        self.rect.center = self.pos
        f = pygame.font.SysFont("Arial", 25)
        t = f.render(str(self.oid), 0, opt.BLACK)
        pygame.Surface.blit(self.image, t, (10,0))

#
    def park_at_sensor(self, sensor):
        self._state = opt.PARKING
        self.move_target = sensor
        sensor.reserved = True
        self.move_step = (sensor.pos - self.pos)/50.
        self.move_len = self.move_step.get_length()

#
    def unpark_from_sensor(self, sensor):
        self._state = opt.LEAVING
        self.move_target = None
        self.move_step = Vector(opt.WIDTH - self.pos[0], 0)/50.

#
    def __getstate__(self):
        return {"pos": self.pos}

    def __setstate__(self, state):
        self.pos = state["pos"]
