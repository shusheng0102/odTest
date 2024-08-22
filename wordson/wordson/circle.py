# coding: utf-8
import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson import events
from wordson import color
from wordson.sprite import Sprite
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.circle')


cfg = Config()

class Circle(Sprite):
    interval = cfg.circle_interval
    _sufs = []
    DRAW = False
    PAUSE = False
    DONE = True

    def __init__(self):
        '''Circle() -> circle instance'''
        super(Circle, self).__init__()

        self.image = self.imgs[0]
        self.rect = self.image.get_rect()
        self.idx = 0
        self.time = 0
        self.step = 0


    @property
    def imgs(self):    # lazy load
        cls = self.__class__
        if not cls._sufs:
            img = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'circle.png'))
            for idx in range(1, 22):#, 2):
                subsuf = img.subsurface((idx*67, 0, 67, 67))
                w, h = subsuf.get_size()
                w = int(w * cfg.circle_resize)
                h = int(h * cfg.circle_resize)
                subsuf = pygame.transform.scale(subsuf, (w, h))
                cls._sufs.append(subsuf)
            empty = pygame.Surface((w, h), flags=pygame.SRCALPHA)
            cls._sufs.insert(0, empty)
        return cls._sufs

    def update(self, time):
        step = self.time // self.interval
        imgs = self.imgs
        length = len(imgs)
        if step == self.step != 0:    # same interval
            self.time += time
            return not (0 < self.idx < length-1)
        self.step = step
        a_loop = False
        if self.DRAW and self.idx < length-1:
            self.idx += 1
        elif not self.DRAW and self.idx > 0:
            self.idx -= 1
        else:
            self.time = 0
            a_loop = True
        # if not a_loop:
        #     logger.debug('idx %s', self.idx)
        self.image = imgs[self.idx]
        self.time += time
        self.DONE = a_loop
        return a_loop


if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)

    pygame.init()
    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()
    circle = Circle()
    count = 0

    while run:
        for event in pygame.event.get():
            circle.handle(event)
            if event.type == pygame.QUIT:
                run = False

        inter = clock.tick(cfg.tick)
        result = circle.update(inter)
        if result:
            circle.DRAW = not circle.DRAW
        screen.fill(color.white)
        circle.draw(screen)
        pygame.display.flip()
        count += 1
    pygame.quit()
