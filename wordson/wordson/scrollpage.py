import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson.rec import Button
from wordson.sprite import Sprite
from wordson.sprite import OrderedUpdates
from wordson import color, tool, events
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.scrollpage')


cfg = Config()


# todo: make it easier to use
# todo: remove the hard-code
class ScrollPage(OrderedUpdates):
    left_gap = 100
    top_gap = 70
    title_gap = 50
    screenw, screenh = cfg.screen
    screenx = screenw / 2

    option_width = 150
    option_height = 100
    option_h_gap = 40
    option_v_gap = 30

    speed = cfg.scroll_page_speed

    def __init__(self, title, text, empty, evtid, **evtattrs):
        super(ScrollPage, self).__init__()


        titlefont = cfg.new_font(50)
        image = tool.render(titlefont, title)
        title = Sprite()
        rect = image.get_rect()
        rect.top = self.top_gap
        rect.centerx = self.screenx
        title.image = image
        title.rect = rect

        self.attrs = evtattrs

        self.options = []
        if text:
            thetop = rect.bottom + self.title_gap

            for idx, text in enumerate(text):

                line = idx % 2
                num = idx // 2
                img = tool.render(cfg.font, text)

                left = self.left_gap + num * (self.option_width + self.option_h_gap)
                top = thetop + line * (self.option_height + self.option_v_gap)
                rect = pygame.Rect(left, top, self.option_width, self.option_height)
                btn = Button(img, rect, evtid, index=idx, **self.attrs)
                self.add(btn)
                self.options.append(btn)

        else:
            image = cfg.font.render(empty, True, color.black, None)
            rect = image.get_rect()
            rect.top = title.rect.bottom + self.title_gap
            rect.left = self.left_gap
            empty = Sprite()
            empty.image = image
            empty.rect = rect
            self.add(empty)

        self.add(title)

        if self.need_scroll():
            roll_btn = []
            for each in ('prev.png', 'next.png'):
                img = pygame.image.load(os.path.join(PROJECTDIR, 'img', each)).convert_alpha()

                rect = img.get_rect()
                img = pygame.transform.scale(img, (int(0.5 * rect.width), int(0.5 * rect.height)))
                spr = Sprite()
                spr.image = img
                spr.rect = img.get_rect()

                roll_btn.append(spr)

            self.prev, self.next = roll_btn

            self.prev.rect.left = 250
            self.prev.rect.top = self.screenh - rect.height
            self.next.rect.left = self.screenw - 250 - self.prev.rect.width
            self.next.rect.top = self.prev.rect.top

            self.add(self.prev)
            self.add(self.next)
        else:
            self.prev = None
            self.next = None

        self.mousedown = False
        self.forwarding = False
        self.backwarding = False

    def need_scroll(self):
        if not self.options:
            return False
        last = self.options[-1]
        right = last.rect.right
        if right > (self.screenw - self.left_gap):
            return True
        return False

    def set_warding(self, pos):
        if self.prev is not None:
            if self.prev.rect.collidepoint(pos):
                logger.debug('backwarding')
                self.backwarding = True
                self.forwarding = False
            elif self.next.rect.collidepoint(pos):
                logger.debug('forwarding')
                self.backwarding = False
                self.forwarding = True
            else:
                logger.debug("don't move")
                self.backwarding = self.forwarding = False

    def update(self, time):
        super(ScrollPage, self).update(time)
        offset = time * self.speed

        if not self.options:
            return

        # logger.debug('forward %s, backward %s', self.forwarding, self.backwarding)
        if self.backwarding:
            right = self.options[-1].rect.right
            space = right - (self.screenw - self.left_gap)
            if space <= 0:
                logger.debug('no space for backward')
                return
            move = -max(int(min(offset, space)), 1)

            # logger.debug('try backwarding %s', move)
        elif self.forwarding:
            left = self.options[0].rect.left
            space = self.left_gap - left
            if space <= 0:
                logger.debug('no space for forward')
                return
            move = max(int(min(offset, space)), 1)
            # logger.debug('try forwarding %s', move)
        else:
            return

        # when move is a float, the calc will go wrong
        # it's stupied not using the time to calc the length directly
        # bug it works
        for each in self.options:
            each.rect.left += move

    def handle(self, event):
        if self.prev is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousedown = True
                if event.button == 1:
                    self.set_warding(event.pos)
                    return
                elif event.button == 4:
                    # mouse wheel roll up to down
                    logger.debug('roll down')
                    self.forwarding = True
                    self.backwarding = False
                elif event.button == 5:
                    # mouse wheel roll down to up
                    logger.debug('roll up')
                    self.forwarding = False
                    self.backwarding = True
                # the mouse wheel trigger event together
                # so update immediatly
                # todo: make this better
                self.update(1000 / cfg.tick * 4)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 4, 5):
                    self.mousedown = False
                    self.forwarding = False
                    self.backwarding = False

            elif event.type == pygame.MOUSEMOTION and self.mousedown:
                pos = event.pos
                self.set_warding(pos)
        return super(ScrollPage, self).handle(event)


class BasePage(ScrollPage):
    def __init__(self, title, select, empty, prevpage, **evtattrs):
        super(BasePage, self).__init__(
                title,
                select,
                empty,
                events.SWITCHPAGE,
                **evtattrs)

        img = tool.render(cfg.font, getattr(cfg, 'return'))
        rect = img.get_rect()
        rect.width += 60
        rect.height += 30
        # rect.left = cfg.screen[0] - rect.width - 40
        rect.top = 480

        rtnbtn = Button(img, rect, events.SWITCHPAGE, to=prevpage, by=self.this_page)
        rtnbtn.rect.centerx = cfg.screen[0] / 2
        self.add(rtnbtn)

class LanguagePage(BasePage):
    this_page = cfg.page_lang
    def __init__(self, langs):
        self.elems = list(langs)
        printable_elems = list(self.elems)    # a copy
        if None in printable_elems:    # the unknown
            printable_elems[printable_elems.index(None)] = cfg.unknown_language
        super(LanguagePage, self).__init__(
                cfg.language_title,
                printable_elems,
                cfg.no_language,
                cfg.page_main,
                to=cfg.page_cate,
                by=self.this_page)

    def handle(self, event):
        if super(LanguagePage, self).handle(event):
            return True
        if (event.type == events.SWITCHPAGE
                and event.by == self.this_page
                and event.to == cfg.page_cate
                and hasattr(event, 'index')):
            event.lang = self.elems[event.index]
            del event.index    # remove this attr
            pygame.event.post(event)
            logger.debug('post event %s', event)
            return True


class CategoryPage(BasePage):
    this_page = cfg.page_cate
    def __init__(self, cates):
        self.elems = list(cates)
        printable_elems = list(self.elems)    # a copy
        if None in printable_elems:    # the unknown
            printable_elems[printable_elems.index(None)] = cfg.unknown_language
        super(CategoryPage, self).__init__(
                cfg.category_title,
                printable_elems,
                cfg.no_category,
                cfg.page_lang,
                to=cfg.page_lib,
                by=self.this_page)

    def handle(self, event):
        if super(CategoryPage, self).handle(event):
            return True
        if (event.type == events.SWITCHPAGE
                and event.by == self.this_page
                and event.to == cfg.page_lib
                and not hasattr(event, 'cate')):
            event.cate = self.elems[event.index]
            pygame.event.post(event)
            logger.debug('post event %s', event)
            return True

class LibPage(BasePage):
    this_page = cfg.page_lib
    def __init__(self, libs):
        self.elems = list(libs)
        super(LibPage, self).__init__(
            cfg.lib_title,
            self.elems,
            cfg.no_lib,
            cfg.page_cate,
            to=cfg.page_mode,
            by=self.this_page
        )

    def handle(self, event):
        if super(LibPage, self).handle(event):
            return True
        if (event.type == events.SWITCHPAGE
                and event.by == self.this_page
                and event.to == cfg.page_mode
                and not hasattr(event, 'lib')):
            event.lib = self.elems[event.index]
            pygame.event.post(event)
            logger.debug('post event %s', event)
            return True


if __name__ == '__main__':
    getlogger(logger, logging.INFO)
    getlogger('wordson.rec', logging.DEBUG)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    pygame.display.set_caption(cfg.title)

    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()
    lang = LanguagePage('test0 test1 test2 test3 test4 test5 test6 test7 test8 test9'.split())
    # lang = CategoryPage('test0 test1 test2 test3 test4 test5 test6 test7 test8 test9'.split())
    # lang = LanguagePage([])

    while run:
        for event in pygame.event.get():
            if lang.handle(event):
                continue
            if event.type == pygame.QUIT:
                run = False

        inter = clock.tick(cfg.tick)
        lang.update(inter)
        screen.fill(color.white)
        lang.draw(screen)
        pygame.display.flip()

    pygame.quit()
