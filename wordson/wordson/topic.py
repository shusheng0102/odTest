# coding: utf-8
import os
import sys
import logging
import pygame
import re

from wordson.tracemore import get_exc_plus
from wordson.minsix import Str
from wordson.config import Config
from wordson.circle import Circle
from wordson.inputer import Inputer
from wordson.soundbtn import SoundButtonGroup
from wordson.wrap import Wrapper
from wordson.sprite import Sprite
from wordson.sprite import Group
from wordson import events
from wordson import color


logger = logging.getLogger('wordson.topic')


cfg = Config()


class Text(Sprite):
    '''The topic user need to anwser'''

    LOGGER = logging.getLogger('wordson.topic.Text')

    def __init__(self, width=None, text='', line_interval=0, font=None):
        super(Text, self).__init__()

        self._width = 70 if width is None else width
        self.wrapper = Wrapper(width=self._width)
        self.text = text
        self.line_interval = line_interval

        if font is None:
            self.font = cfg.font
        else:
            self.font = font

        self.image = self.fontsuf()
        self.rect = self.image.get_rect()

    def fontsuf(self, text=None, color=color.black):
        if text is None:
            text = self.text
        textline = self.wrapper.wrap(text).splitlines()
        textsurf = list(map(lambda t: self.font.render(t, True, color, None), textline))

        max_height = 0
        max_width = 0
        for each in textsurf:
            rect = each.get_rect()
            max_height = max(max_height, rect.height)
            max_width = max(max_width, rect.width)

        surf_height = max((max_height+self.line_interval) * len(textsurf) - self.line_interval, 0)
        surf_width = max_width

        surf = pygame.Surface((surf_width, surf_height), flags=pygame.SRCALPHA)
        start = 0
        while textsurf:
            font_suf = textsurf.pop(0)
            surf.blit(font_suf, (0, start))
            start += (max_height + self.line_interval)
        return surf

    # @property
    # def font(self):    # lazy load. Cannot use before init pygame
    #     return cfg.font

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        self._width = value
        self.wrapper = value

    def set(self, text):
        self.text = text
        topleft = self.rect.topleft
        self.image = self.fontsuf()
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

        self.LOGGER.debug('%s at %s', text, self.rect)


class Title(Text):
    def __init__(self, text=''):
        width = cfg.topic_len
        hspace = cfg.topic_hspace
        super(Title, self).__init__(width, text, line_interval=hspace)
        self.rect.x = cfg.topic_x
        self.rect.y = cfg.topic_y
        self.font = cfg.new_font(40)
        self.wrapper.width = 30


class Option(Sprite):

    def __init__(self, text='', value=None):
        self.value = value
        self._rawtext = text
        self.text = Text(cfg.option_len, text)
        super(Option, self).__init__()
        self.circle = Circle()
        self._checked = False
        rectt = self.text.rect
        rectc = self.circle.rect

        # rectc.x = x
        # rectc.y = y
        rectt.left = rectc.right + 3
        rectt.top = rectc.top

        self.rect = pygame.Rect(0, 0, 0, 0)
        self._update()

        self.refresh = False
        self.bind_keys = None

    @property
    def checked(self):
        return self._checked
    @checked.setter
    def checked(self, value):
        self.circle.DRAW = value
        self._checked = value

    @property
    def rawtext(self):
        return self._rawtext
    @rawtext.setter
    def rawtext(self, value):
        self._rawtext = value
        # save old rect position
        oldrect = self.text.rect
        left = oldrect.left
        top = oldrect.top
        # refresh the font image
        self.text = Text(cfg.option_len, value)
        self.text.image = self.text.fontsuf()
        # restore rect position
        rect = self.text.image.get_rect()
        rect.left = left
        rect.top = top
        self.text.rect = rect
        # self.refresh = True
        self._update()

    def handle(self, event):
        if self.text.handle(event):
            logger.debug('%s handled', event)
            return True
        if self.circle.handle(event):
            logger.debug('%s handled by circle', event)
            return True
        if (event.type == pygame.MOUSEMOTION
                and not self.checked):
            pos = event.pos
            collided = self.rect.collidepoint(pos)
            if collided != self.circle.DRAW:
                logger.debug('collided %s, %s', collided, self)
                self.circle.DRAW = collided
        elif event.type == pygame.KEYUP:
            if event.key in self.bind_keys:
                logger.info('key currect %s', event.key)
                self.checked = True
            else:
                self.checked = False

    def collidepoint(self, pos):
        for rect in (self.circle.rect, self.text.rect):
            if rect.collidepoint(pos):
                return True
        return False

    def update(self, time):
        if not self.circle.DONE:
            self.refresh = True    # the circle is drawing. Need calc image
        self.text.update(time)
        self.circle.update(time)

        if self.refresh:
            self._update()

    def _update(self):
        '''join the image together'''
        t = self.text
        c = self.circle
        rt = t.rect
        rc = c.rect

        width = rt.width + rc.width
        height = max(rt.height, rc.height)

        self.rect.size = (width, height)
        img = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        img.blit(c.image, (0, 0))
        img.blit(t.image, (rc.width, 0))
        self.image = img

    def draw(self, surface):
        self.text.draw(surface)
        self.circle.draw(surface)

    def __str__(self):
        result = super(Option, self).__str__()
        return ''.join((result[:-1], 'bind_keys=', pygame.key.name(self.bind_keys), ' value=', str(self.value), '>'))


class Topic(Group):

    SELECT = True
    auto_1st_char = True

    CONFIG = Config()
    LOGGER = logging.getLogger('wordson.topic.Topic')

    def __init__(self, auto_1st_char=True, top=100):
        super(Topic, self).__init__()
        self.auto_1st_char = auto_1st_char
        t = Title()
        t.rect.top = top
        self.title = t
        self.options = []
        for value, keys in enumerate((
                    (pygame.K_a, pygame.K_1),
                    (pygame.K_b, pygame.K_2),
                    (pygame.K_c, pygame.K_3),
                    (pygame.K_d, pygame.K_4),
                )):
            opt = Option(value=value)
            opt.bind_keys = keys
            self.options.append(opt)
        self.inputer = Inputer()
        self.add(self.title)
        self.sound_title = Text(font=self.CONFIG.new_font(path=self.CONFIG.soundmark_font))
        self.add(self.sound_title)
        self.sound_btn_group = None
        self.refresh_sprites()

        self.answer_value = None

    @property
    def bottom(self):
        if self.SELECT:
            return self.options[-1].rect.bottom
        return self.inputer.rect.bottom

    def handle(self, event):
        result = False
        # select
        if self.SELECT:
            answer_value = None
            if (event.type == pygame.MOUSEBUTTONUP
                    and event.button == 1):

                for each in self.options:
                    if each.rect.collidepoint(event.pos):
                        logger.info('anwser=%s', each.value)
                        each.checked = True
                        answer_value = each.value
                    else:
                        each.checked = False

            elif event.type == pygame.KEYUP:
                key = event.key
                for each in self.options:
                    if key in each.bind_keys:
                        each.checked = True
                        answer_value = key.value
                        break

            if answer_value is not None:
                pygame.event.post(events.answer(answer_value))
                result = True
        # input
        elif (not self.SELECT
                and event.type == pygame.KEYUP
                and event.key == pygame.K_RETURN):
            result = self.inputer.value().strip()
            if result:
                logger.info('anwser=%s', result)
                pygame.event.post(events.answer(result))
            else:
                logger.debug('empty anwser')
            return True

        if self.sound_btn_group is not None:
            self.sound_btn_group.handle(event)

        if not result:
            return super(Topic, self).handle(event)
        return result

    def set(self, title, options=None, placeholder=None, sound=None):
        self.answer_value = None
        if placeholder is not None:
            self.inputer.placeholder = placeholder
        #     self.inputer.placeholder = u''
        # else:

        select = (options is not None)
        if select != self.SELECT:
            logger.debug('set to select: %s', select)
            self.SELECT = select
            self.refresh_sprites()

        self.title.set(title)
        if select:
            for text, opt, s in zip(options, self.options, ('A. ', 'B. ', 'C. ', 'D.')):
                if self.auto_1st_char:
                    text = s + text
                opt.rawtext = text
                opt.checked = False

        self.sound_title.set('')
        if self.sound_btn_group is not None:
            self.sound_btn_group.stop()
            self.sound_btn_group.kill()
            self.remove(self.sound_btn_group)
            self.sound_btn_group = None

        if sound:
            mode = sound['mode']
            if mode == 'mixed':
                title = ' '.join('[{}]'.format(each) for each in sound['value']['soundmarks'])
                self.sound_title.set(title)
                sound_info = [{'text': '', 'sound_path': each} for each in sound['value']['soundpaths']]
            else:
                sound_info = [{'text': each['soundmark'], 'sound_path': each['soundpath']} for each in sound['value']]

            self.LOGGER.debug('set sound %s', sound_info)
            self.sound_btn_group = SoundButtonGroup(sound_info)
            self.add(self.sound_btn_group)
            self.sound_btn_group.play()

        self.inputer.clear()

        self.rearange()

    def refresh_sprites(self):
        logger.debug('refresh sprites: select=%s', self.SELECT)
        if self.SELECT:
            kill = [self.inputer]
            add = self.options
        else:
            kill = self.options
            add = [self.inputer]

        for each in kill:
            each.kill()

        for each in add:
            self.add(each)

    def rearange(self):
        '''adjust the rect of each sprite'''
        gap = 20

        # title
        rectt = self.title.rect
        top = rectt.bottom + gap
        left = rectt.left
        centerx = rectt.centerx

        # sound title
        if self.sound_title.text:
            self.sound_title.rect.top = top
            self.sound_title.rect.left = 50
            top = self.sound_title.rect.bottom + gap

        if self.sound_btn_group is not None:
            x = 50
            y = top
            screen_width, _ = self.CONFIG.screen
            max_width = screen_width - left - 20
            self.sound_btn_group.rearange((x, y), max_width)

            top = self.sound_btn_group.get_bottom() + gap

        recti = self.inputer.rect
        recti.top = top

        for each in self.options:
            recto = each.rect
            recto.left = left
            recto.top = top
            top += recto.height

    def update(self, interval):
        self.title.update(interval)
        self.inputer.update(interval)
        if self.sound_title.text:
            self.sound_title.update(interval)
        if self.sound_btn_group is not None:
            self.sound_btn_group.update(interval)
        for each in self.options:
            each.update(interval)


if __name__ == '__main__':

    from wordson.bashlog import getlogger
    from wordson.util import PROJECTDIR

    getlogger(None, logging.DEBUG)

    pygame.init()
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
    screen = pygame.display.set_mode(cfg.screen)


    run = True
    clock = pygame.time.Clock()
    # title = Title("""I'm using python with pygame and trying to get the width of text. The pygame documentation says to use pygame.font.Font.size(). 但我有点不明白应该使用哪个函数。我一直收到`TypeError: descriptor 'size' requires a 'pygame.font.Font' object but received a 'str'`的错误。""")
    # title.set("Test")
    # title.image = title.fontsuf()
    # opt = Option(0, 0, 'Test')
    # cir = opt.circle
    topic = Topic()
    # topic.set(u"Test title", None, u'some placeholder')
    # topic.set(u"Test title", None, None)
    topic.set(u"I'm using python with pygame a。",
              (u"重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启重启;"
              u"关机关机关机关机关机关机关机关机关机关机关机;还原;换用Ubuntu系统啊Ubuntu啊这年头谁还用Windows写代码啊").split(';'),
              'holder',
              sound={
                "mode": "one2one",
                "value": [
                  {
                    "soundmark": "ˌeɪviˈeɪʃən $",
                    "soundpath": os.path.join(PROJECTDIR, 'words', "test1.wav"),
                  },
                  {
                    "soundmark": "ˌæ-ɪviˈeɪʃən $",
                    "soundpath": os.path.join(PROJECTDIR, 'words', "test2.wav"),
                  }
                ]
              }
              # sound={
              #   "mode": "mixed",
              #   "value": {
              #     "soundmarks": ["ˌeɪviˈeɪʃən $", "ˌeɪ-", "ˌæ-"],
              #     "soundpaths": [os.path.join(PROJECTDIR, 'words', "test1.wav"), os.path.join(PROJECTDIR, 'words', "test2.wav")],
              #   }
              # }
              )
                # "...",
                # False)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # opt.handle(event)
            topic.handle(event)

        inter = clock.tick(cfg.tick)
        # opt.update(inter)
        topic.update(inter)
        screen.fill(color.white)
        # title.draw(screen)
        # opt.draw(screen)
        topic.draw(screen)
        # topic.title.draw(screen)
        pygame.display.flip()

    pygame.quit()
