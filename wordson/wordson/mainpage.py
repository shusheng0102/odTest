import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.minsix import callable
from wordson.config import Config
from wordson.rec import Button
from wordson.sprite import Sprite
from wordson.sprite import Group
from wordson import color
from wordson import tool
from wordson import events


logger = logging.getLogger('wordson.mainpage')


cfg = Config()


class LoadButton(Button):
    refresh = False
    def __init__(self, rec):
        self.noload = tool.render(cfg.new_font(cfg.btn_fontsize), cfg.no_save)
        self.load = tool.render(cfg.new_font(cfg.btn_fontsize), cfg.load)
        self.rect = rec
        self._date = None

        super(LoadButton, self).__init__(self.noload, rec, events.LOAD, color.grey)
        self.image = self.set_image()

    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, value):
        if self._date != value:
            logger.debug('refresh to %s', value)
            self._date = value
            self.image = self.set_image()

    def set_image(self):
        if not self.date:
            logger.debug('no date')
            self.raw_image = self.noload
        else:
            logger.debug('date %s', self._date)
            loadimg = self.load
            dateimg = tool.render(cfg.font, self.date)
            imgrect = loadimg.get_rect()
            daterect = dateimg.get_rect()

            width = max(imgrect.width, daterect.width)
            height = imgrect.height + imgrect.height

            surf = pygame.Surface((width, height), pygame.SRCALPHA)

            startimg = (width - imgrect.width) / 2
            startdate = (width - daterect.width) / 2

            surf.blit(loadimg, (startimg, 0))
            surf.blit(dateimg, (startdate, imgrect.height))
            self.raw_image = surf

        return self.calc_image(self.raw_image)


class MainPage(Group):
    _title_font = None
    this_page = cfg.page_main

    def __init__(self):
        super(MainPage, self).__init__()

        screenx = cfg.screen[0] // 2

        # title
        big_font = cfg.new_font(cfg.titlesize)
        title = Sprite()
        title.image = tool.render(big_font, cfg.title)
        title.rect = title.image.get_rect()
        title.rect.top = cfg.title_offset
        title.rect.centerx = screenx
        self.add(title)

        # button
        btnrect = pygame.Rect(0, 0, 120, 80)
        # start btn
        btn_font = cfg.new_font(cfg.btn_fontsize)
        img = tool.render(btn_font, cfg.start)
        # rect = img.get_rect()
        rect = pygame.Rect(btnrect)
        rect.width += cfg.btn_h_offset * 2
        rect.height += cfg.btn_v_offset * 2
        rect.centerx = screenx
        rect.top = title.rect.bottom + cfg.start_btn_gap
        startbtn = Button(img, rect, events.SWITCHPAGE, to=cfg.page_lang, by=self.this_page)
        self.add(startbtn)

        # load save botton
        # img = tool.render(btn_font, cfg.load)
        # # rect = img.get_rect()
        # rect = pygame.Rect(btnrect)
        # rect.width += cfg.btn_h_offset * 2
        # rect.height += cfg.btn_v_offset * 2
        # rect.centerx = screenx
        # rect.top = startbtn.rect.bottom + cfg.btn_gap
        # loadbtn = Button(img, rect, events.SWITCHPAGE, to=cfg.page_load, by=self.this_page)
        # self.add(loadbtn)

        rect = pygame.Rect(btnrect)
        rect.width += cfg.btn_h_offset * 2
        rect.height += cfg.btn_v_offset * 2
        rect.centerx = screenx
        rect.top = startbtn.rect.bottom + cfg.btn_gap
        self.loadbtn = LoadButton(rect)
        self.add(self.loadbtn)

        # exit button
        img = btn_font.render(cfg.exit, True, color.black, None)
        # rect = img.get_rect()
        rect = pygame.Rect(btnrect)
        rect.height += cfg.btn_v_offset * 2
        rect.width += cfg.btn_h_offset * 2
        rect.centerx = screenx
        rect.top = self.loadbtn.rect.bottom + cfg.btn_gap
        exitbtn = Button(img, rect, evtid=pygame.QUIT)
        self.add(exitbtn)

    def set_load_date(self, date=None):
        self.loadbtn.date = date




if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    pygame.display.set_caption(cfg.title)

    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()
    page = MainPage()
    # btn = Button("test")
    page.set_load_date('2015-03-22 21:49:05')

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
