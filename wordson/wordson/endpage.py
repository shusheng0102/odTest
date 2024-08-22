import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.wrap import Wrapper
from wordson.config import Config
from wordson.rec import Button
from wordson.role import Role
from wordson.sprite import Sprite
from wordson.sprite import Group
from wordson import color
from wordson import tool
from wordson import events
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.endpage')


cfg = Config()

class EndPage(Group):
    this_page = cfg.page_end
    screenw = cfg.screen[0]
    left = 50
    top = 50
    linegap = 10
    wrapper = Wrapper(None, 75)
    def __init__(self, time, rate, word_and_time, chart=True):
        super(EndPage, self).__init__()

        self.chart = chart
        self.right_num, self.total_num = rate

        # role
        self.role = Role()
        self.role.rect.left = -self.role.rect.width
        self.role.forward_speed = 0.4

        # ground
        line = Sprite()
        lineimg = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'ground.png')).convert_alpha()
        linerect = lineimg.get_rect()
        linerect.y = cfg.ground - 5
        line.image = lineimg
        line.rect = linerect

        # back button
        gap = 50
        btrec = pygame.Rect(0, line.rect.bottom+20, 150, 50)
        bkimg = tool.render(cfg.font, getattr(cfg, 'return'))
        bkrec = pygame.Rect(btrec)
        bkrec.right = self.screenw / 2 - gap
        bkbtn = Button(bkimg, bkrec, events.SWITCHPAGE, bg=color.indigo, to=cfg.page_main, by=self.this_page)

        # exit button
        exitimg = tool.render(cfg.font, cfg.exit)
        exitrec = pygame.Rect(btrec)
        exitrec.left = self.screenw / 2 + gap
        exitbtn = Button(exitimg, exitrec, pygame.QUIT, bg=color.red)

        # used time
        used_time = Sprite()
        img = tool.render(cfg.font, cfg.used_time%time)
        rec = img.get_rect()
        rec.left = self.left
        rec.top = self.top
        used_time.image = img
        used_time.rect = rec

        # rate
        top = rec.bottom + 5
        rate = Sprite()
        ratenum = self.right_num * 100/self.total_num if self.total_num != 0 else 100
        img = tool.render(cfg.font, cfg.word_rate % (ratenum, self.right_num, self.total_num))
        rec = img.get_rect()
        rec.left = self.left
        rec.top = top
        rate.image = img
        rate.rect = rec
        # char title
        top = rec.bottom + 5
        chartitle = Sprite()
        img = tool.render(cfg.font, cfg.word_wrong)
        rec = img.get_rect()
        rec.top = top
        rec.left = self.left
        chartitle.image = img
        chartitle.rect = rec

        top = rec.bottom + 10
        bottom = line.rect.top - 10
        height = bottom - top
        width = self.screenw - self.left * 2

        self.midrect = pygame.Rect(self.left, top, width, height)
        if word_and_time:
            if chart:
                self.lines = self.mkline(word_and_time, self.midrect)
            else:
                self.lines = self.mkwords(word_and_time)
        else:
            self.lines = tool.render(cfg.font, cfg.no_wrong)
        self.start_at = 0

        self.extend(self.role, line, bkbtn, exitbtn, used_time, rate, chartitle)

    def mkwords(self, word_and_time):
        all_words = '; '.join(x[0] for x in word_and_time)
        one_str = self.wrapper.wrap(all_words)
        return tool.render(cfg.font, one_str)


    def mkline(self, word_and_time, rec):
        left = rec.x
        top = rec.y
        width = rec.width
        gap = self.linegap

        words = []
        maxnum = 0
        maxwordlen = 0
        maxwordheight = 0
        nums = []
        for word, times in word_and_time:
            wordimg = tool.render(cfg.font, cfg.word_and_time%(word, times))
            words.append(wordimg)
            nums.append(times)
            maxnum = max(maxnum, times)
            rec = wordimg.get_rect()
            maxwordlen = max(rec.width, maxwordlen)
            maxwordheight = max(rec.height, maxwordheight)

        fackheight = (maxwordheight + gap) * len(word_and_time)
        needsurf = pygame.Surface((width, fackheight), pygame.SRCALPHA)

        y = 0
        for wordimg, num in zip(words, nums):
            imgr = wordimg.get_rect()
            imgw = imgr.width
            x = maxwordlen - imgw
            needsurf.blit(wordimg, (x, y))

            subwidth = num * (width-maxwordlen-5) / maxnum
            subheight = 20
            subx = maxwordlen + 5
            suby = y + (maxwordheight - subheight) / 2
            sub = needsurf.subsurface((subx, suby, subwidth, subheight))
            sub.fill(color.green)

            y += imgr.height + gap

        return needsurf

    def draw(self, surface):
        # surface.blit(self.lines, (0, 0))

        sub = surface.subsurface(self.midrect)
        # surfh = self.midrect.height
        # realh = self.lines.get_rect().height
        start_at = self.start_at
        # y =
        sub.blit(self.lines, (0, start_at))
        super(EndPage, self).draw(surface)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4: # roll up
                self.start_at += 25
            elif event.button == 5:    # roll down
                self.start_at -= 25
            else:
                return super(EndPage, self).handle(event)
            max_at = self.midrect.height - self.lines.get_rect().height
            start_at = max(self.start_at, max_at)
            self.start_at = min(0, start_at)
        super(EndPage, self).handle(event)




    def update(self, time):
        if self.role.rect.x > self.screenw:
            self.role.kill()

        super(EndPage, self).update(time)



if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    pygame.display.set_caption(cfg.title)

    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()
    page = EndPage('00:42:20', (2, 9), (('1words', 7),
                                        ('2words', 2),
                                        ('3words', 3),
                                        ('4words', 12),
                                        ('5words', 5),
                                        ('6words', 8),
                                        ('7words', 2),
                                        ('8words', 5),
                                        ('9words', 1),
                                        ('10words', 1),
                                        ('11words', 1),
                                        ('12words', 1),
                                        ('13words', 1),
                                        ),
                    True)

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
