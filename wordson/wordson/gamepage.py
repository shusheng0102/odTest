# coding: utf-8
import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.minsix import Str
from wordson.config import Config
from wordson.runline import RunLine
from wordson.topic import Topic
from wordson.processbar import ProcessBar
from wordson.fancycircle import FancyCircle
from wordson.rec import Button
from wordson.sprite import Group
from wordson.sprite import Sprite
from wordson import color, tool, events
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.gamepage')


cfg = Config()


class SaveButton(Button):

    SAVE = 0
    SAVING = 1
    SAVED = 2
    ERROR = 3
    _status = 0
    refresh = False

    def __init__(self, rec):
        self.saveimg = tool.render(cfg.font, cfg.save)
        self.savingimg = tool.render(cfg.font, cfg.saving)
        self.saved = tool.render(cfg.font, cfg.saved)

        self.rect = rec
        super(SaveButton, self).__init__(self.saveimg, rec, events.SAVE, color.indigo)
        self.draw_speed = self.draw_speed * 2
        self.erase_speed = self.erase_speed * 2
        self.update(0)

    def handle(self, event):
        if (event.type == events.SAVE and hasattr(event, 'msg')):
            if event.msg is None:
                self.status = self.SAVED
            else:
                self.raw_image = tool.render(cfg.font, event.msg)
                self.status = self.ERROR
            logger.debug('event %s handled by SaveButton', event)
            return True
        if (event.type == pygame.MOUSEBUTTONUP
                and event.button == 1
                and self.status == self.SAVE):
            self.status = self.SAVING
            evt = events.save()
            logger.debug('send save event %s', evt)
            pygame.event.post(evt)
            return True
        return super(SaveButton, self).handle(event)

    def update(self, time):
        if self.refresh:
            logger.debug('refreshing %s', self.status)
            if self.status != self.ERROR:
                self.raw_image = (self.saveimg, self.savingimg, self.saved)[self.status]
            self.calc_image()
            self.refresh = False
        super(SaveButton, self).update(time)

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        if self._status != value:
            logger.debug('need refresh to %s', value)
            self._status = value
            self.refresh = True

    def clear(self):
        self.status = 0


class Notification(Sprite):

    stay_time = cfg.noti_stay_time

    def __init__(self, width=400):
        super(Notification, self).__init__()
        self.min_width = width

        # comment part
        imgpath = os.path.join(PROJECTDIR, 'img', 'comment.png')
        surf = pygame.image.load(imgpath).convert_alpha()

        imgs = []
        for idx in range(4):
            x = idx * 105
            sub = surf.subsurface((x, 0, 105, 45))
            imgs.append(sub)
        self.imgs = imgs

        # enter key
        enterpath = os.path.join(PROJECTDIR, 'img', 'enter.png')
        self.enter = pygame.transform.scale(pygame.image.load(enterpath).convert_alpha(), (27, 27))

        # the correct anwser is image
        self.correct_is = tool.render(cfg.font, cfg.right_answer, color.red)
        # press enter to continue image
        self.enter_to_continue = tool.render(cfg.font, cfg.enter_to_continue)

        self.image = imgs[0]
        self.rect = pygame.Rect(0, 0, width, 0)

        self.bare = pygame.Surface((0, 0), flags=pygame.SRCALPHA)

        self.hanging_time = 0
        self.correct = ""
        self.level = 0
        self.show = False

        self._update()

    @property
    def blocked(self):
        return self.level == 3

    def update(self, time):
        if self.show and not self.blocked:
            self.hanging_time += time
            if self.hanging_time >= self.stay_time:
                logger.debug('timeout of Notification')
                self.show = False
                self.image = self.bare
        # else:
        #     self.image = self.bare

    def _update(self):
        if self.correct:
            self._update_wrong()
        else:
            self._update_right()

    def _update_wrong(self):
        img = self.imgs[self.level]
        enter = self.enter

        correct_text = self.correct_is    # text image
        this_anwser = tool.render(cfg.font, self.correct)    # text image
        enter_text = self.enter_to_continue    # text image

        imgw, imgh = img.get_rect().size
        correct_text_w, correct_text_h = correct_text.get_rect().size
        this_anwser_w, this_anwser_h = this_anwser.get_rect().size
        enter_text_w, enter_text_h = enter_text.get_rect().size
        enter_icon_w, enter_icon_h = enter.get_rect().size

        width = max(imgw, correct_text_w+this_anwser_w, enter_text_w+enter_icon_w, self.min_width)
        height = imgh + max(correct_text_h, this_anwser_h) + max(enter_text_h, enter_icon_h)

        self.rect.size = width, height

        image = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        image.blit(img, (0, 0))
        logger.debug(image.blit(correct_text, (0, imgh)))
        logger.debug(image.blit(this_anwser, (correct_text_w, imgh)))
        x = width - enter_text_w - enter_icon_w
        y = imgh + correct_text_h
        image.blit(enter_text, (x, y))
        x += enter_text_w
        image.blit(enter, (x, y))

        self.image = image


    def _update_right(self):
        image = self.imgs[self.level]
        rec = image.get_rect()
        self.rect.size = max(self.min_width, self.rect.width), rec.height
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        left = (self.rect.width - rec.width) / 2
        self.image.blit(image, (left, 0))

    def set(self, correct_or_level):
        if isinstance(correct_or_level, Str):
            self.correct = correct_or_level
            self.level = 3
            self._update_wrong()
        else:
            self.correct = ''
            self.level = min(max(correct_or_level, 0), 2)
            self._update_right()

        logger.debug('Notification set to %s, %s', self.correct, self.level)
        self.hanging_time = 0
        self.show = True

    def draw(self, surface):
        if not self.show:
            return
        super(Notification, self).draw(surface)

    def handle(self,event):
        if (self.correct and self.show):
            nomore = False
            if (event.type == pygame.MOUSEBUTTONUP
                    and event.button == 1):
                pos = event.pos

                # enter_text_w, enter_text_h = self.enter_to_continue.get_rect().size
                # enter_icon_w, enter_icon_h = self.enter.get_rect().size
                #
                # width = enter_text_w + enter_icon_w
                # height = max(enter_icon_h, enter_text_h)
                #
                # recttop, rectleft = self.rect.topleft
                # rectw, recth = self.rect.size
                #
                # top = recttop + recth - height
                # left = rectleft + rectw - width
                #
                # rect = pygame.Rect(left, top, width, height)


                if self.rect.collidepoint(pos):
                # if rect.collidepoint(pos):
                    logger.debug('click on Notification')
                    nomore = True

            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                logger.debug('enter on Notification')
                nomore = True

            if nomore:
                self.level = 0    # no block
                self.show = False
                self.hanging_time = 0
                logger.debug('event %s handled by Notification', event)
                evt = events.nexttopic()
                logger.info('post event %s', evt)
                pygame.event.post(evt)
                return True


class PauseButton(Group):

    def __init__(self, x=600, y=50):
        super(PauseButton, self).__init__()
        self.circle = FancyCircle()
        crect = self.circle.rect
        crect.topleft = x, y
        # crect.y = y

        self.pb = ProcessBar()
        prect = self.pb.rect
        prect.centery = y + crect.height / 2
        prect.x = x + crect.width - 10

        self.timer = tool.Timer()
        self.timer.start()
        trect = pygame.Rect(0, 0, 0, 0)
        trect.centery = prect.centery - 12
        trect.x = prect.x + 20
        self.time_rect = trect

        self.pauseimg = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'pause.png')).convert_alpha()
        self.playimg = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'play.png')).convert_alpha()

        brect = self.pauseimg.get_rect()
        brect.center = crect.center
        self.btn_rect = brect

        self.playing = True
        self.btn = self.pauseimg

    def set_process(self, process):
        return self.pb.set(process)

    def clear(self):
        self.timer.start()    # restart
        self.set_process(0)

    def update(self, time):
        if self.playing:
            self.btn = self.pauseimg
        else:
            self.btn = self.playimg
        self.timer.update(time)
        self.circle.update(time)
        self.pb.update(time)

    def draw(self, surface):
        self.pb.draw(surface)
        self.circle.draw(surface)

        text = self.timer.formatted
        img = tool.render(cfg.font, text)
        surface.blit(img, (self.time_rect.x, self.time_rect.y))

        surface.blit(self.btn, (self.btn_rect.x, self.btn_rect.y))

    def handle(self, event):
        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            pos = event.pos
            if self.collidepoint(pos):
                self.circle.DRAW = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.playing = not self.playing
                    if self.playing:
                        self.timer.unpause()
                    else:
                        self.timer.pause()
            else:
                self.circle.DRAW = False

    def collidepoint(self, pos):
        return self.circle.rect.collidepoint(pos) or self.pb.rect.collidepoint(pos)

    def get_time(self):
        return self.timer.time

    def get_formatted_time(self):
        return self.timer.formatted

    def set_time(self, time):
        self.timer.time = time
        return time


class GamePage(Group):

    screenx = int(cfg.screen[0] / 2)
    award_time_interval = cfg.award_time_interval

    def __init__(self):
        super(GamePage, self).__init__()

        self.runline = RunLine()
        self.topic = Topic()

        self.noti = Notification()
        self.pause_btn = PauseButton()

        self.noti.centerx = self.screenx

        self.white = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'white.png')).convert_alpha()

        rec = pygame.Rect(0, 0, 250, 90)
        rec.centerx = self.screenx
        rec.y = 150

        resume = tool.render(cfg.font, cfg.resume)
        self.resume_btn = Button(resume, pygame.Rect(rec), None, color.indigo)
        self.resume_btn.draw_speed = self.resume_btn.draw_speed * 2    # rebound. dont use *=
        self.resume_btn.erase_speed = self.resume_btn.erase_speed * 2

        rec.y += rec.height + 20
        self.save_btn = SaveButton(pygame.Rect(rec))

        exit = tool.render(cfg.font, cfg.exit)
        rec.y += rec.height + 20
        self.exit_btn = Button(exit, pygame.Rect(rec), pygame.QUIT, color.red)
        self.exit_btn.draw_speed = self.exit_btn.draw_speed * 2
        self.exit_btn.erase_speed = self.exit_btn.erase_speed * 2

        self.timer = tool.Timer()

        # self.extend(self.runline, self.topic, self.noti)
    def get_time(self):
        return self.pause_btn.get_time()

    def get_formatted_time(self):
        return self.pause_btn.get_formatted_time()

    def set_time(self, time):
        return self.pause_btn.set_time(time)

    def update(self, time):
        if self.pause_btn.playing:
            self.noti.update(time)
            self.runline.update(time)
            self.topic.update(time)

            self.noti.rect.top = self.topic.bottom
            self.noti.rect.centerx = self.screenx
        else:
            self.save_btn.update(time)
            self.exit_btn.update(time)
            self.resume_btn.update(time)

        self.pause_btn.update(time)

    def draw(self, surface):
        self.noti.draw(surface)
        self.runline.draw(surface)
        self.topic.draw(surface)

        if not self.pause_btn.playing:
            white = pygame.transform.scale(self.white, surface.get_size())
            surface.blit(white, (0, 0))

            self.resume_btn.draw(surface)
            self.save_btn.draw(surface)
            self.exit_btn.draw(surface)

        self.pause_btn.draw(surface)

    def handle(self, event):
        if not self.pause_btn.playing:
            self.exit_btn.handle(event)
            self.save_btn.handle(event)
            self.resume_btn.handle(event)

        if event.type == events.RESULT:
            self.is_correct(event.currect, event.answer)
            logger.debug('event %s handled by gamepage', event)
            return True

        # click resume button
        if (not self.pause_btn.playing    # pausing
                and event.type == pygame.MOUSEBUTTONUP
                and event.button == 1    # left button
                and self.resume_btn.rect.collidepoint(event.pos)):    # in resume button

            self.pause_btn.playing = True
            self.save_btn.status = self.save_btn.SAVE
            logger.debug('event %s handled by resume', event)
            return True

        # click on the pause button, fresh the save button
        if (event.type == pygame.MOUSEBUTTONUP
                and event.button == 1
                and self.pause_btn.playing
                and self.pause_btn.collidepoint(event.pos)):
            self.save_btn.clear()


        if not self.noti.blocked:
            children = (self.noti, self.runline, self.pause_btn, self.topic)
        else:
            children = (self.noti, self.runline, self.pause_btn)
        if any(map(lambda x: x.handle(event), children)):
            return True

    def is_correct(self, result, anwser=None):
        logger.debug('correct: %r', result)
        inter_time = self.timer.stop()
        logger.info("use time %s", inter_time)
        self.timer.start()
        if result:    # correct
            self.noti.set(inter_time // self.award_time_interval)
            evt = events.nexttopic()
            logger.info('post event %s', evt)
            pygame.event.post(evt)
            self.runline.jump_next()
            return

        self.noti.set(anwser)
        self.runline.roll_next()

    def set(self, title, options=None, placeholder=None, sound=None):
        self.timer.start()    # refresh timer
        self.topic.set(title, options, placeholder, sound)
        if not options:    # input
            for each in (self.topic.title.rect, self.topic.inputer.rect):
                each.centerx = self.screenx
                logger.debug(each)

    def set_process(self, process):
        return self.pause_btn.set_process(process)

    def clear(self):
        self.runline.clear()
        self.pause_btn.clear()


if __name__ == '__main__':
    getlogger(logging.getLogger(), logging.DEBUG)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    pygame.display.set_caption(cfg.title)

    screen = pygame.display.set_mode(cfg.screen)

    run = True
    clock = pygame.time.Clock()
    page = GamePage()
#     page.topic.set('Select your favorite Zen of Python:')
    page.set('X:')
#     page.set('Select your favorite Zen of Python:', '''以动手实践为荣 , 以只看不练为耻;
# 以打印日志为荣 , 以单步跟踪为耻;
# 以空格缩进为荣 , 以制表缩进为耻;
# 以单元测试为荣 , 以人工测试为耻;'''.splitlines())

    # page.is_correct(True)
    # page.is_correct(False)
    # page.is_correct(True)
    # page.is_correct(False)

    # noti = Notification()
    # noti.rect.x = 50
    # noti.rect.x = 300
    # noti.set("ERROR")

    # pbt = PauseButton()

    while run:
        for event in pygame.event.get():
            if page.handle(event):
                continue
            # if noti.handle(event):
            #     continue
            # pbt.handle(event)
            if event.type == pygame.QUIT:
                run = False

        inter = clock.tick(cfg.tick)
        # noti.update(inter)
        page.update(inter)
        # pbt.update(inter)
        screen.fill(color.white)
        # screen.set_colorkey(color.white)
        # noti.draw(screen)
        page.draw(screen)
        # pbt.draw(screen)
        pygame.display.flip()

    pygame.quit()
