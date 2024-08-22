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


logger = logging.getLogger('wordson.processbar')


cfg = Config()


# todo: animation
class ProcessBar(Sprite):
    start_at = 10

    def __new__(cls):
        if not hasattr(cls, 'emptyimg'):
            file = os.path.join(PROJECTDIR, 'img', 'empty_bar.png')
            cls.emptyimg = pygame.image.load(file).convert_alpha()
            file = os.path.join(PROJECTDIR, 'img', 'full_bar.png')
            cls.fullimg = pygame.image.load(file).convert_alpha()
            cls.mask = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'mask_bar.png')).convert_alpha()

        return super(ProcessBar, cls).__new__(cls)

    def __init__(self):
        self.image = self.emptyimg
        self.rect = self.image.get_rect()
        self.process = 0
        self.now = -1
        self.update(0)


    def update(self, time):
        if self.process != self.now:
            img = self.emptyimg.copy()
            # img = self.fullimg.copy()

            width = self.rect.width
            avaliable_width =  width - self.start_at
            start_at = -avaliable_width
            need_width = self.process * avaliable_width / 100
            start_at += need_width

            img.blit(self.fullimg, (start_at, 0))
            img.blit(self.mask, (0, 0), None, pygame.BLEND_RGBA_MULT)

            self.image = img

    def set(self, process):
        self.now = self.process
        self.process = process


if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    pygame.display.set_caption(cfg.title)

    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()

    pb = ProcessBar()
    pb.rect.x = 50
    pb.rect.y = 50
    pb_value = 0
    add_every = 1

    while run:

        pb.set(pb_value)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        inter = clock.tick(cfg.tick)

        pb.update(inter)

        screen.fill(color.grey)
        pb.draw(screen)
        pygame.display.flip()

        if pb_value > 100:
            pb_value = 101
            add_every = -1
        if pb_value < 0:
            pb_value = -1
            add_every = 1

        pb_value += add_every

    pygame.quit()
