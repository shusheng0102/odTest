# coding: utf-8
import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson import events
from wordson.color import black
from wordson.color import grey
from wordson.color import white
from wordson.sprite import Sprite
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.inputer')


cfg = Config()


class Inputer(Sprite):
    printable = (
        pygame.K_0,
        pygame.K_1,
        pygame.K_2,
        pygame.K_3,
        pygame.K_4,
        pygame.K_5,
        pygame.K_6,
        pygame.K_7,
        pygame.K_8,
        pygame.K_9,
        pygame.K_AMPERSAND,
        pygame.K_ASTERISK,
        pygame.K_AT,
        pygame.K_BACKQUOTE,
        pygame.K_BACKSLASH,
        pygame.K_BACKSPACE,
        pygame.K_BREAK,
        pygame.K_CARET,
        pygame.K_COLON,
        pygame.K_COMMA,
        pygame.K_DOLLAR,
        pygame.K_EQUALS,
        pygame.K_EURO,
        pygame.K_LEFTBRACKET,
        pygame.K_MINUS,
        pygame.K_PLUS,
        pygame.K_POWER,
        pygame.K_PERIOD,   # <,
        pygame.K_QUESTION,
        pygame.K_QUOTE,
        pygame.K_QUOTEDBL,
        pygame.K_RIGHTBRACKET,
        pygame.K_RIGHTPAREN,
        pygame.K_SLASH,
        pygame.K_SPACE,
        pygame.K_SEMICOLON,    # ;
        pygame.K_UNDERSCORE,
        pygame.K_UNKNOWN,
        pygame.K_a,
        pygame.K_b,
        pygame.K_c,
        pygame.K_d,
        pygame.K_e,
        pygame.K_f,
        pygame.K_g,
        pygame.K_h,
        pygame.K_i,
        pygame.K_j,
        pygame.K_k,
        pygame.K_l,
        pygame.K_m,
        pygame.K_n,
        pygame.K_o,
        pygame.K_p,
        pygame.K_q,
        pygame.K_r,
        pygame.K_s,
        pygame.K_t,
        pygame.K_u,
        pygame.K_v,
        pygame.K_w,
        pygame.K_x,
        pygame.K_y,
        pygame.K_z,
    )
    def __init__(self, centerx=300, y=0):
        self.placeholder = cfg.placeholder
        logger.debug('inputer placeholder=%r', self.placeholder)
        self.words = []
        self.words_changed = True

        linepath = os.path.join(PROJECTDIR, 'img', 'line.png')
        self.line = pygame.image.load(linepath).convert_alpha()

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.centerx = centerx

        self.update(0)

        super(Inputer, self).__init__()

    def fontsurf(self, text=None, color=None):
        if text is None:
            if self.words:
                text = ''.join(self.words)
                if color is None:
                    color = black
            else:
                text = self.placeholder
                logger.debug('use placeholder %r', text)
                if color is None:
                    color = grey

        logger.debug('text=%r', text)
        textsurf = cfg.font.render(text, True, color, None)
        return textsurf

    def update(self, time):
        if self.words_changed:
            self.words_changed = False
            logger.debug('words changed')
            fontsurf = self.fontsurf()
            centerx = self.rect.centerx
            y = self.rect.y

            imgw, imgh = fontsurf.get_rect().size
            linew, lineh = self.line.get_rect().size

            height = imgh + lineh
            width = max(imgw, linew)
            self.rect.size = width, height
            self.rect.centerx = centerx
            self.rect.y = y

            image = pygame.Surface((width, height), flags=pygame.SRCALPHA)
            image.blit(fontsurf, ((width-imgw)//2, 0))
            image.blit(self.line, ((width-linew)//2, height-lineh))
            self.image = image

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key >= 0x100 and event.key <= 0x109):    # Num Keyboard
                event.key - 0xD0

            if event.key == pygame.K_BACKSPACE:
                if self.words:
                    poped = self.words.pop()
                    logger.debug('pop %s', poped)
                    self.words_changed = True

            elif (event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL)):
                logger.debug('function key has been pressed. skip %s', event)
                return False

            elif event.key in self.printable:

                result = event.unicode
                self.words.append(result)
                self.words_changed = True
                logger.debug('new val %s. Key %s', result, event.key)
                return False

        # elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
        #     self.deleting = False
        #     self.deleting_time = 0

    def clear(self):
        self.words[:] = ()
        self.words_changed = True

    def value(self):
        return ''.join(self.words)


if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)

    pygame.init()
    screen = pygame.display.set_mode(cfg.screen)
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)

    run = True
    clock = pygame.time.Clock()
    count = 0

    inputer = Inputer()

    while run:
        for event in pygame.event.get():
            inputer.handle(event)
            if event.type == pygame.QUIT:
                run = False

        inter = clock.tick(cfg.tick)
        inputer.update(inter)
        screen.fill(white)
        inputer.draw(screen)
        pygame.display.flip()
        count += 1
    pygame.quit()
