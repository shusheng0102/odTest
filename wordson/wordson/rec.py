import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson import color
from wordson.sprite import Sprite


logger = logging.getLogger('wordson.rec')


cfg = Config()


class Rec(Sprite):
    width = cfg.rec_width
    draw_speed = cfg.rec_draw_speed
    erase_speed = cfg.rec_erase_speed
    interval = cfg.rec_interval
    color = color.black
    DRAW = False
    REFRESH = False

    def __init__(self, image, rect, bgcolor=None):

        super(Rec, self).__init__()
        self.bg = bgcolor

        self.draw_length = 0
        self.erase_length = 0
        self.raw_image = image.copy()
        # self.image = self.calc_image()
        self.rect = rect
        self.image = self.calc_image(image)
        self.counttime = 0

    def update(self, time):
        self.counttime += time
        if not self.counttime // self.interval:
            return False
        self.counttime = 0
        if self.REFRESH:
            self.draw_length += (self.interval * self.draw_speed)    # need not pause. erase is faster than draw
            if not self.DRAW:
                self.erase_length += (self.interval * self.erase_speed)    # pause erase if it's drawing

            width, height = self.rect.size
            all_length = (width + height) * 2

            self.draw_length = min(self.draw_length, all_length)
            self.erase_length = min(self.erase_length, all_length)

            drawl = self.draw_length  # % all_length
            erasel = self.erase_length  # % all_length

            if drawl == erasel == all_length and not self.DRAW:    # erase finished
                # logger.debug('erase finished')
                self.image = self.calc_image(self.raw_image)
                self.draw_length = 0
                self.erase_length = 0    # don't go too big
                self.REFRESH = False
                return True

            # rect = self.raw_image.get_rect()
            # img = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
            img = self.calc_image(self.raw_image)
            # the black line
            lineimg = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
            for rect in self.get_rects(drawl):
                surf = pygame.Surface(rect.size)
                surf.fill(self.color)
                # img.blit(surf, rect.topleft)
                lineimg.blit(surf, rect.topleft)
            # the mask
            for rect in self.get_rects(erasel):
                surf = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
                # img.blit(surf, rect.topleft, None, pygame.BLEND_RGBA_MULT)
                lineimg.blit(surf, rect.topleft, None, pygame.BLEND_RGBA_MULT)
            # draw the real line to image

            # self.image = self.raw_image.copy()
            img.blit(lineimg, (0, 0))
            self.image = img
            # self.image.blit(img, (0, 0))

    def set_image(self, img):
        self.raw_image = img.copy()
        self.image = self.calc_image(img)

    def calc_image(self, img):
        result_img = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        if self.bg:
            result_img.fill(self.bg)
        # imgw, imgh = self.raw_image.get_rect().size
        imgw, imgh = img.get_rect().size

        realw, realh = self.rect.size
        x = (realw - imgw) // 2
        h = (realh - imgh) // 2
        # img.blit(self.raw_image, (x, h))
        result_img.blit(img, (x, h))
        return result_img

    def get_rects(self, length):
        result = []
        width, height = self.rect.size
        line = self.width
        lmt = 0
        if length > lmt:    # 0
            r = pygame.Rect(0, 0, line, min(length, height))
            result.append(r)
            lmt += height
        if length > lmt:    # height
            r = pygame.Rect(0, height-line, min(width, length-lmt), line)
            result.append(r)
            lmt += width
        if length > lmt:    # height + width
            minlen = min(lmt+height, length)
            y = lmt + height - minlen
            reallen = height - y
            r = pygame.Rect(width-line, y, line, reallen)
            result.append(r)
            lmt += height
        if length > lmt:    # height + width + height
            minlen = min(lmt+width, length)
            reallen = minlen - lmt
            x = width - reallen
            r = pygame.Rect(x, 0, reallen, line)
            result.append(r)

        return result

    def handle(self, event):
        if (event.type == pygame.MOUSEMOTION
                # or it's the mouse wheel which may cause the ui change(though mouse is not changing)
                or (event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN)
                    and event.button in (4, 5, 6))
            ):
            collided = self.rect.collidepoint(event.pos)
            if self.DRAW != collided:
                # logger.debug('change to %s'%('draw' if collided else 'erase'))
                self.DRAW = collided
                self.REFRESH = True
                if collided:    # to draw
                    self.draw_length = 0
                    self.erase_length = 0

    def set_to_draw(self):
        if not self.DRAW:
            self.DRAW = True
            self.REFRESH = True

    def set_to_undraw(self):
        if self.DRAW:
            self.DRAW = False
            self.REFRESH = True

class Button(Rec):

    def __init__(self, img, rect, evtid, bg=color.grey, **attrs):
        super(Button, self).__init__(img, rect, bg)

        self.evtid = evtid
        self.evtattrs = attrs

        # logger.debug('event id=%s, event attrs=%s', evtid, attrs)

    def handle(self, event):
        super_result = super(Button, self).handle(event)
        if (event.type == pygame.MOUSEBUTTONUP
                and self.evtid is not None
                and event.button == 1
                and self.rect.collidepoint(event.pos)):
            evt = pygame.event.Event(self.evtid, **self.evtattrs)
            logger.debug('send event %s', evt)
            pygame.event.post(evt)
            return True
        return super_result

if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)

    class Test(Button):
        def __init__(self):
            self.image = pygame.Surface((50, 50))
            self.image.fill(color.grey)
            self.rect = self.image.get_rect()
            self.rect.topleft = 20, 20
            super(Test, self).__init__(self.image, self.rect, 25)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()
    rec = Test()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            rec.handle(event)

        inter = clock.tick(cfg.tick)
        rec.update(inter)
        screen.fill(color.white)
        rec.draw(screen)
        pygame.display.flip()

    pygame.quit()
