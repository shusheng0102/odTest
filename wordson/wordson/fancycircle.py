import os
import sys
import logging
import pygame


from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson.sprite import Sprite
from wordson import color
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.fancycircle')


cfg = Config()

class FancyCircle(Sprite):
    imgs = []
    interval = 40
    def __init__(self):
        if not self.imgs:
            self.load_imgs()

        self.image = self.imgs[0]
        self.rect = self.image.get_rect()

        self.time = 0
        self.idx = 0
        self.DRAW = False

    @classmethod
    def load_imgs(cls):
        file = os.path.join(PROJECTDIR, 'img', 'fancy_circle.png')
        surf = pygame.image.load(file).convert_alpha()
        for idx in range(13):
            cls.imgs.append(surf.subsurface(idx * 50, 0, 50, 50))

    def update(self, time):
        imgs_num = len(self.imgs)
        if self.DRAW and self.idx == imgs_num - 1:
            return True    # finished draw
        elif not self.DRAW and self.idx == 0:
            return True    # finished erase

        self.time += time
        step = self.time // self.interval

        if step < 1:
            return False    # wait for the next interval

        self.time = 0

        if self.DRAW:
            self.idx = min(self.idx + step, imgs_num-1)
            a_loop = (self.idx == imgs_num - 1)
        else:
            self.idx = max(self.idx - step, 0)
            a_loop = (self.idx == 0)

        # logger.debug('draw: %s, idx: %s', self.DRAW, self.idx)

        self.image = self.imgs[self.idx]
        return a_loop





if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)
    getlogger('wordson.topic', logging.DEBUG)
    getlogger('wordson.inputer', logging.DEBUG)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    pygame.display.set_caption(cfg.title)

    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()

    fcircle = FancyCircle()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        inter = clock.tick(cfg.tick)
        if fcircle.update(inter):
            # pass
            fcircle.DRAW = not fcircle.DRAW

        screen.fill(color.white)
        fcircle.draw(screen)
        pygame.display.flip()

    pygame.quit()
