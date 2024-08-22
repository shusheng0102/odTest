import os
import sys
import logging
import random
import pygame

logger = logging.getLogger('wordson.block')

from wordson.bashlog import getlogger, DEBUG
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson.sprite import Sprite, OrderedUpdates
from wordson.util import PROJECTDIR

cfg = Config()


class Block(Sprite):
    """Block on the map"""
    PIG = 0
    TRIANGLE = 1
    RECT = 2
    CIRCLE = 3
    TOWER = 4
    SPRING = 5
    THORN = 6

    PAUSE = False

    interval = cfg.block_interval
    _allimgs = []
    def __init__(self, tp=None, x=None):
        super(Block, self).__init__()
        if tp is None:
            tp = random.randint(0, 6)

        if tp == self.PIG:
            self.imgs = self.allimgs[:2]
        elif tp == self.TRIANGLE:
            self.imgs = self.allimgs[2:4]
        elif tp == self.RECT:
            self.imgs = self.allimgs[4:6]
        elif tp == self.CIRCLE:
            self.imgs = self.allimgs[6:8]
        elif tp == self.TOWER:
            self.imgs = [self.allimgs[8]]
        elif tp == self.SPRING:
            self.imgs = [self.allimgs[9]]
        elif tp == self.THORN:
            self.imgs = [self.allimgs[10]]
        else:
            raise ValueError("invaliad type %s", tp)

        self.acted = False    # every block only act with role once

        self.image = self.imgs[0]
        self.rect = self.image.get_rect()
        if x is not None:
            self.rect.x = x
        self.total_time = 0

    def update(self, time):
        if not self.PAUSE:
            self.total_time += time
            newimg = (self.total_time // self.interval) % 2
            if newimg and len(self.imgs)>1:
                self.total_time = 0
                idx = self.imgs.index(self.image)
                length = len(self.imgs)
                thisidx = idx+1
                if thisidx - length >= 0:    # out of range
                    thisidx = 0
                self.image = self.imgs[thisidx]
            return super(Block, self).update(time)

    @property
    def allimgs(self):    # lazy load
        cls = self.__class__
        if not cls._allimgs:
            img = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'block.png')).convert_alpha()
            for x in range(0, 660, 60):
                cls._allimgs.append(img.subsurface((x, 0, 60, 60)))
            logger.debug('init %s, %s', cls.__name__, cls._allimgs)
        return cls._allimgs

    def pause(self):
        self.PAUSE = True

    def unpause(self):
        self.PAUSE = False



# class BlockGroup(pygame.sprite.Group):
class BlockGroup(OrderedUpdates):
    PAUSE = False
    speed = cfg.rollspeed
    prev_speed = speed

    # def __init__(self):
    #     super(BlockGroup, self).__init__()

    def update(self, time):
        if not self.PAUSE:
            for each in self.sprites():
                each.rect.right -= (self.speed * time)    # change x will cause a bug. Why???

                if each.rect.right <= 0:
                    each.kill()
        return super(BlockGroup, self).update(time)

    def pause(self):
        logger.debug('pause')
        return self._pause(True)

    def unpause(self):
        logger.debug('unpause')
        return self._pause(False)

    def _pause(self, value):
        self.PAUSE = value
        if value:
            to = 'pause'
        else:
            to = 'unpause'
        for each in self.sprites():
            getattr(each, to)()

    def stop_roll(self):
        if self.speed != 0:
            self.prev_speed = self.speed
            self.speed = 0

    def resume_roll(self):
        if self.prev_speed != 0:
            self.speed = self.prev_speed


if __name__ == '__main__':
    import time
    getlogger(logger, DEBUG)

    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    group = BlockGroup()
    run = True
    clock = pygame.time.Clock()
    block = Block()
    block.rect.x = 500
    logger.debug(block.rect.x)
    group.add(block)
    thetime = time.time()
    pygame.display.flip()
    while run:
        run += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if time.time() - thetime > 1:
            thetime = time.time()
            block = Block()
            block.rect.x = 500
            group.add(block)
            # group.pause()
        # else:
        #     group.unpause()
        group.update(clock.tick(cfg.tick))
        screen.fill((255, 255, 255))
        group.draw(screen)
        pygame.display.flip()

    pygame.quit()
