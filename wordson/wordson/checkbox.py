import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson.sprite import Sprite
from wordson import color, tool
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.checkbox')


cfg = Config()


class CheckBox(Sprite):
    interval = cfg.chkbox_interval
    boxes = []
    def __init__(self):
        super(CheckBox, self).__init__()

        if not self.boxes:    # lazy load images into class(not instance)

            cls = self.__class__

            surf = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'chkbox.png')).convert_alpha()

            boxes = []
            for idx in range(13):
                subsurf = pygame.transform.scale(surf.subsurface((idx * 80, 0, 80, 80)), (50, 50))
                boxes.append(subsurf)

            cls.boxes = boxes

        self.time = 0
        self.idx = 0

        self.image = self.boxes[0]
        self.rect = self.image.get_rect()
        self.checked = False

    def update(self, time):
        maxidx = len(self.boxes)-1
        if ((self.checked and self.idx == maxidx)
                or (not self.checked and self.idx == 0)):
            return True

        self.time += time
        step = self.time // self.interval
        if step < 1:    # not hit the interval, wait for next update
            return False

        self.time = 0

        if not self.checked:    # erasing
            self.idx = max(self.idx - step, 0)
            self.image = self.boxes[self.idx]
            return self.idx == 0

        # drawing
        idx = min(self.idx+step, maxidx)    # should not get out of range

        self.idx = idx
        self.image = self.boxes[idx]
        return (idx == maxidx)

    def handle(self, event):
        if (event.type == pygame.MOUSEBUTTONUP
                and event.button == 1):
            pos = event.pos
            if self.rect.collidepoint(pos):
                self.checked = not self.checked

class LabelCheckBox(Sprite):
    def __init__(self, label, help=None, x=0, y=0):

        super(LabelCheckBox, self).__init__()

        self.chkbox = CheckBox()
        self.label = tool.render(cfg.font, label)
        if help:
            self.help = tool.render(cfg.new_font(10), help)
        else:
            self.help = None
        self.rect = pygame.Rect(x, y, 0, 0)
        self.update_img()

        self.first_0 = False
        # this is: when checkbox count to 0, it return True
        # but LabelCheckBox need one update after that


    def update(self, time):
        if not self.chkbox.update(time):
            self.first_0 = True
            self.update_img()
            return False
        elif (not self.chkbox.checked
                and self.chkbox.idx == 0
                and self.first_0):
            self.update_img()
            self.first_0 = False
            return True
        return True


    def update_img(self):
        chkimg = self.chkbox.image
        chkrct = self.chkbox.rect

        labelimg = self.label
        labelw, labelh = labelimg.get_rect().size
        helpw, helph = self.help.get_rect().size if self.help else (0, 0)

        selfrct = self.rect

        width = chkrct.width + max(labelw, helpw)
        height = max(chkrct.height, labelh + helph)

        centerx = max(chkrct.height, labelh) / 2
        chktop = centerx - chkrct.height / 2
        labeltop = centerx - labelh / 2

        surf = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        surf.blit(chkimg, (0, chktop))
        surf.blit(labelimg, (chkrct.width, labeltop))
        if self.help:
            surf.blit(self.help, (chkrct.width, labelh))

        selfrct.size = width, height
        self.image = surf

    def handle(self, event):
        if (event.type == pygame.MOUSEBUTTONUP
                and event.button == 1):
            pos = event.pos
            if self.rect.collidepoint(pos):
                self.chkbox.checked = not self.chkbox.checked

    @property
    def checked(self):
        return self.chkbox.checked
    @checked.setter
    def checked(self, value):
        self.chkbox.checked = value


if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    pygame.display.set_caption(cfg.title)

    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()
    # chkbox = CheckBox()
    chkbox = LabelCheckBox('title', 'helpmsg')

    while run:
        for event in pygame.event.get():
            if chkbox.handle(event):
                continue
            if event.type == pygame.QUIT:
                run = False

        inter = clock.tick(cfg.tick)
        chkbox.update(inter)
        screen.fill(color.white)
        chkbox.draw(screen)
        pygame.display.flip()

    pygame.quit()
