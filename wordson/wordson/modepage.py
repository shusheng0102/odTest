import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.minsix import callable
from wordson.config import Config
from wordson.rec import Button
from wordson.checkbox import LabelCheckBox
from wordson.circle import Circle
from wordson.sprite import Sprite
from wordson.sprite import Group
from wordson import tool
from wordson import events
from wordson import color


logger = logging.getLogger('wordson.modepage')


cfg = Config()

# todo: don't copy myself


class ModePage(Group):

    this_page = cfg.page_mode
    screenx = cfg.screen[0] / 2

    left_gap = 150
    top_gap = 70

    btn_gap = 100

    option_title_gap = 50
    option_line_gap = 10
    option_group_gap = 40

    mid_left_gap = 40
    mid_top_gap = 50
    mid_line_gap = 10

    radio_top_gap = 20
    radio_line_gap = 10


    def __init__(self):
        super(ModePage, self).__init__()

        # title
        titlefont = cfg.new_font(50)
        image = tool.render(titlefont, cfg.mode_title)
        title = Sprite()
        rect = image.get_rect()
        rect.top = self.top_gap
        rect.centerx = self.screenx
        title.image = image
        title.rect = rect
        self.add(title)

        # return button
        img = tool.render(cfg.font, getattr(cfg, 'return'))
        rect = img.get_rect()
        rect.width += 60
        rect.height += 30
        rect.top = 480

        rtnbtn = Button(img, rect, events.SWITCHPAGE, to=cfg.page_cate, by=self.this_page)
        rtnbtn.rect.centerx = cfg.screen[0] / 2 + self.btn_gap

        self.add(rtnbtn)

        # start button
        img = tool.render(cfg.font, cfg.start)
        rect = img.get_rect()
        rect.width += 60
        rect.height += 30
        rect.top = 480

        startbtn = Button(img, rect, events.SWITCHPAGE, bg=color.indigo, to=cfg.page_game, by=self.this_page)
        startbtn.rect.centerx = cfg.screen[0] / 2 - self.btn_gap

        self.add(startbtn)

        self.startbtn = startbtn

        # how to show the topic
        x = self.left_gap
        y = title.rect.bottom + self.option_title_gap
        opts = []
        for text in (cfg.mode_option_select_by_meaning,
                     cfg.mode_option_write_by_meaning,
                     cfg.mode_option_select_by_word,
                     cfg.mode_play_sound,
                    ):
            box = LabelCheckBox(text, x=x, y=y)
            y += (box.rect.height + self.option_line_gap)
            opts.append(box)
            self.add(box)
        self.choose_meaning, self.write_word, self.choose_word, self.play_sound = opts
        self.write_word.checked = True
        self.play_sound.checked = True

        # how to hit the word
        x = self.mid_left_gap + self.screenx
        y = title.rect.bottom + self.mid_top_gap
        opts = []
        for text in (cfg.mode_show_type,
                     cfg.mode_show_first_char,
                     cfg.mode_shuffle,
                     ):
            box = LabelCheckBox(text, x=x, y=y)
            y += (box.rect.height + self.mid_line_gap)
            opts.append(box)
            self.add(box)
        self.show_type, self.show_1st_char, self.shuffle = opts
        self.show_type.checked = True
        self.shuffle.checked = True

        # how to repeat the topic
        x = self.mid_left_gap + self.screenx + 10
        y = opts[-1].rect.bottom + self.radio_top_gap
        opts = []
        for text, help in ((cfg.mode_repeat_word, cfg.mode_repeat_word_help),
                           (cfg.mode_once_word, cfg.mode_once_word_help)):
            radio = LabelRadio(text, help, x, y)
            y += (radio.rect.height + self.radio_line_gap)
            opts.append(radio)
            self.add(radio)

        self.repeat_word, self.once_word = opts
        self.repeat_word.checked = True

    def update(self, time):
        self.repeat_word.checked, self.once_word.checked = not self.once_word.checked, not self.repeat_word.checked
        if any(x.checked for x in (self.choose_meaning, self.write_word, self.choose_word)):
            self.add(self.startbtn)
        else:
            self.startbtn.kill()
        return super(ModePage, self).update(time)

    def handle(self, event):
        super(ModePage, self).handle(event)
        if event.type == pygame.MOUSEBUTTONUP:
            repeat, once = self.repeat_word, self.once_word
            if repeat.rect.collidepoint(event.pos):
                repeat.checked = True
                once.checked = False
                return True
            elif once.rect.collidepoint(event.pos):
                repeat.checked = False
                once.checked = True
                return True
        # to=cfg.page_game, by=self.this_page
        elif (event.type == events.SWITCHPAGE
                and event.to == cfg.page_game
                and event.by == self.this_page
                and not hasattr(event, 'repeat')):
                result = {
                    'choose_meaning': self.choose_meaning.checked,
                    'choose_word': self.choose_word.checked,
                    'write_word': self.write_word.checked,
                    'show_type': self.show_type.checked,
                    'show_1st_char': self.show_1st_char.checked,
                    'play_sound': self.play_sound.checked,
                    'shuffle': self.shuffle.checked,
                    'repeat': self.repeat_word.checked
                }
                event.dict.update(result)
                logger.debug('post event %s', event)
                pygame.event.post(event)
                return True


class LabelRadio(Sprite):

    line_gap = 5

    def __init__(self, label, help, x, y):
        super(LabelRadio, self).__init__()
        self.label = tool.render(cfg.font, label)
        self.help = tool.render(cfg.new_font(15), help)
        self.circle = Circle()
        self._checked = False
        self.rect = pygame.Rect(x, y, 0, 0)
        self._update()

    def update(self, time):
        if self.circle.update(time):
            return True
        self._update()

    def _update(self):
        circleimg = self.circle.image
        circlew, circleh = self.circle.rect.size

        labelimg = self.label
        labelw, labelh = labelimg.get_rect().size

        helpimg = self.help
        helpw, helph = helpimg.get_rect().size

        _height = max(circleh, labelh)
        circletop = (_height - circleh) / 2
        labeltop = (_height - labelh) / 2

        width = circlew + max(labelw, helpw)
        height = max(circleh, labelh + helph) + self.line_gap

        surf = pygame.Surface((width, height), flags=pygame.SRCALPHA)

        surf.blit(circleimg, (0, circletop))
        surf.blit(labelimg, (circlew, labeltop))
        surf.blit(helpimg, (circlew, labelh+self.line_gap))

        self.rect.size = width, height
        self.image = surf


    # def handle(self, event):
    #     if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
    #         self.checked = True
    #         return True
    #
    @property
    def checked(self):
        return self._checked
    @checked.setter
    def checked(self, value):
        self.circle.DRAW = value
        self._checked = value


if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    pygame.display.set_caption(cfg.title)

    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()
    page = ModePage()
    # btn = Button("test")

    while run:
        for event in pygame.event.get():
            if page.handle(event):
                continue
            if event.type == pygame.QUIT:
                run = False

        inter = clock.tick(cfg.tick)
        page.update(inter)
        screen.fill(color.white)
        page.draw(screen)
        pygame.display.flip()

    pygame.quit()
