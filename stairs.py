# -*- coding:utf-8 -*-

#
import pygame
import settings as opt

import logging
info = logging.info
debug = logging.debug
error = logging.error
warning = logging.warning
collide = pygame.sprite.spritecollide

from vec import Vec2d as Vector

class Stairs(pygame.sprite.Sprite):
    oid = 0
    def __init__(self, world, pos):
        self._layer = opt.STAIRS_LAYER
        self.groups = world.all_sprites, world.stairs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.oid = Stairs.oid
        Stairs.oid += 1
        self.world = world
        self.image = pygame.Surface((100, 30))
        self.image.fill(opt.GRAY)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.pos = Vector(pos)

    def update(self):
        self.rect.center = self.pos
