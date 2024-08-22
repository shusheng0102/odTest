import logging
import os

import pygame

from wordson import import_init as _
from wordson.rec import Button
from wordson.config import Config
from wordson.sprite import Group
from wordson import events, tool
from wordson.util import PROJECTDIR


class SoundButton(Button):

    LOGGER = logging.getLogger('wordson.soundbutton')

    SPEAKER_IMG = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'speaker-icon.png')).convert_alpha()
    PLAY_IMG = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'play-icon.png')).convert_alpha()

    GAP_ICON = 5
    GAP_H = 10
    GAP_V = 10

    def __init__(self, label_img, sound_path, channel_id, x_y, **event_attrs):
        # text_img = tool.render(self.CONFIG.font, text)
        self.channel_id = channel_id
        self.channel = pygame.mixer.Channel(channel_id)
        self.sound = pygame.mixer.Sound(sound_path)

        _, _, label_w, label_h = label_img.get_rect()
        pref_w = pref_h = label_h

        speaker_img = pygame.transform.scale(self.SPEAKER_IMG, (pref_w, pref_h))
        play_img = pygame.transform.scale(self.PLAY_IMG, (pref_w, pref_h))

        merged_imgs = []
        merged_w = pref_w + self.GAP_ICON + label_w
        merged_h = label_h
        for pref_img in (play_img, speaker_img):
            merged_serf = pygame.Surface((merged_w, merged_h), flags=pygame.SRCALPHA)
            # merged_serf.blits(
            #     (pref_img, (0, 0)),
            #     (label_img, (pref_w + self.GAP_ICON, 0)),
            # )
            merged_serf.blit(pref_img, (0, 0))
            merged_serf.blit(label_img, (pref_w + self.GAP_ICON, 0))
            merged_imgs.append(merged_serf)

        self.default_img, self.playing_img = merged_imgs

        self.playing = False

        x, y = x_y

        rect = pygame.Rect(x, y, merged_w + self.GAP_H * 2, merged_h + self.GAP_V * 2)

        new_event_attrs = {
            'sub_type': events.TYPESOUNDBUTTONCLICK,
            'channel_id': channel_id,
        }
        new_event_attrs.update(event_attrs)

        super(SoundButton, self).__init__(self.default_img, rect, events.WORDSOUND, **new_event_attrs)

    def play(self):
        self.set_to_draw()
        self.set_image(self.playing_img)
        self.playing = True
        self.channel.play(self.sound)

    def stop(self, send_event=False):
        self.channel.fadeout(1000)
        # self.channel.stop()
        self.set_image(self.default_img)
        self.playing = False
        self.set_to_undraw()
        if send_event:
            evt = pygame.event.Event(events.WORDSOUND, sub_type=events.TYPESOUNDEND, channel_id=self.channel_id)
            self.LOGGER.debug('send event %s', evt)
            pygame.event.post(evt)

    def handle(self, event):
        # result = super(SoundButton, self).handle(event)
        result = False
        if event.type == events.WORDSOUND and event.sub_type == events.TYPESOUNDBUTTONCLICK and event.channel_id == self.channel_id:
            self.LOGGER.debug('start playing sound for channel %s', self.channel_id)
            self.stop()
            self.set_image(self.playing_img)
            self.channel.play(self.sound)
            self.playing = True
            # self.image =
            self.set_to_draw()
            return True

        if not self.playing:
            self.set_to_undraw()
            result = super(SoundButton, self).handle(event)
        return result

    def update(self, inteval):

        super_result = False

        if self.playing and not self.channel.get_busy():
            # assert False
            self.playing = False
            self.set_image(self.default_img)
            evt = pygame.event.Event(events.WORDSOUND, sub_type=events.TYPESOUNDEND)
            self.LOGGER.debug('send event %s', evt)
            pygame.event.post(evt)
            return True

        # if self.playing:
        #     self.set_to_draw()
        # else:
        #     super_result = super(SoundButton, self).update(inteval)
        super_result = super(SoundButton, self).update(inteval)

        return super_result

    def __del__(self):
        try:
            self.channel.stop()
        except pygame.error:
            pass


class SoundButtonGroup(Group):

    LOGGER = logging.getLogger('wordson.soundbuttongrup')
    CONFIG = Config()

    GAP = 10
    PLAY_INTERVAL = 1000 # 1 sec

    def __init__(self, text_sound_path):
        super(SoundButtonGroup, self).__init__()

        pygame.mixer.set_num_channels(len(text_sound_path) + 10)

        max_text_width = max_text_height = 0

        font = self.CONFIG.new_font(path=self.CONFIG.soundmark_font)

        for each in text_sound_path:
            max_text_img = tool.render(font, each['text'])
            # _, _, text_img_width, text_img_height = max_text_img.get_rect()
            # max_text_width = max(max_text_width, text_img_width)
            # max_text_height = max(max_text_height, text_img_height)
            #
            # each['text_width'] = text_img_width
            # each['text_height'] = text_img_height
            each['text_img'] = max_text_img

        # x, y = x_y
        # acc_x, acc_y = x_y
        # max_x = x + max_width

        self.id_to_info = id_to_info = {}

        for index, each in enumerate(text_sound_path):
            channel_id = index + 10
            text = each['text']
            sound_path = each['sound_path']
            # text_img = tool.render(self.CONFIG.font, text)
            #
            # btn_x = acc_x
            #
            # if btn_x > max_x:
            #     btn_x = x
            #     btn_y = acc_y + max_text_height + self.GAP + SoundButton.GAP_V * 2
            # else:
            #     btn_y = acc_y

            sound_button = SoundButton(
                each['text_img'],
                sound_path,
                channel_id,
                # (btn_x, btn_y),
                (0, 0),
            )

            # _, _, sound_button_width, _ = sound_button.rect
            #
            # acc_x = btn_x + sound_button_width + self.GAP
            # acc_y = btn_y

            id_to_info[channel_id] = {
                'text': text,
                'sound_path': sound_path,
                'sound_btn': sound_button,
            }

            # if index > 0:  # not first one
            #     last_btn = id_to_info[channel_id - 1]['sound_btn']
            #     last_rect = last_btn.rect

            self.add(sound_button)

        # if auto_play:
        #     min_key = min(self.id_to_info.keys())
        #     self.playing_btn = btn = self.id_to_info[min_key]['sound_btn']
        #     self.next_btn = self.id_to_info.get(min_key + 1, {'sound_btn': None})['sound_btn']
        #     self.next_countdown = self.PLAY_INTERVAL
        #     btn.play()
        # else:
        #     self.playing_btn = None
        #     self.next_btn = None
        #     self.next_countdown = -1
        self.auto_play = False
        self.playing_btn = None
        self.next_btn = None
        self.next_countdown = -1

    def rearange(self, x_y, max_width):
        acc_x, acc_y = x, y = x_y
        max_x = x + max_width

        for id, each in sorted(self.id_to_info.items(), key=lambda k_v: k_v[0]):
            sound_button = each['sound_btn']

            btn_x = acc_x

            if btn_x > max_x:
                btn_x = x
                btn_y = acc_y + sound_button.rect.height + self.GAP
            else:
                btn_y = acc_y

            sound_button.rect.x = btn_x
            sound_button.rect.y = btn_y

            sound_button_width = sound_button.rect.width

            acc_x = btn_x + sound_button_width + self.GAP
            acc_y = btn_y

    def play(self):
        self.auto_play = True
        self.next_countdown = 0
        info_sorted = sorted(self.id_to_info.items(), key=lambda k_v: k_v[0])
        self.LOGGER.debug('play all %s', info_sorted)
        first_btn_info = info_sorted[0]
        self.playing_btn = None
        self.next_btn = first_btn_info[1]['sound_btn']
        # self.update(0)

    def stop(self):
        self.auto_play = False
        self.playing_btn = None
        for info in self.id_to_info.values():
            sound_btn = info['sound_btn']
            sound_btn.stop()

    def get_bottom(self):
        return sorted(self.id_to_info.items(), key=lambda k_v: k_v[0])[-1][-1]['sound_btn'].rect.bottom

    def update(self, interval):
        for btn in self.sprites():
            btn.update(interval)

        if self.auto_play and self.playing_btn is None:
            if self.next_countdown > 0:  # still need to countdown
                self.next_countdown -= interval
                # self.LOGGER.debug('counting down %s', self.next_countdown)
            else:  # try playing next
                if self.next_btn is None:  # no next
                    self.LOGGER.debug('no next')
                    self.auto_play = False
                else:  # play next
                    self.LOGGER.debug('play next')
                    self.playing_btn = self.next_btn
                    self.playing_btn.play()
                    self.next_countdown = self.PLAY_INTERVAL
                    self.next_btn = None

    def handle(self, event):
        handle_btn = None

        for btn in self.sprites():
            handle_result = btn.handle(event)
            if handle_result:
                handle_btn = btn

        if event.type == events.WORDSOUND and event.sub_type == events.TYPESOUNDEND and self.auto_play and self.playing_btn is not None:
            current_channel_id = self.playing_btn.channel_id
            self.LOGGER.debug('sound end for %s', current_channel_id)
            next_channel_id = current_channel_id + 1
            self.next_btn = self.id_to_info.get(next_channel_id, {'sound_btn': None})['sound_btn']
            self.LOGGER.debug('set playing btn to None, %s', current_channel_id)
            self.playing_btn = None

        if (handle_btn is not None and
                        event.type == events.WORDSOUND and
                        event.sub_type == events.TYPESOUNDBUTTONCLICK and
                        self.auto_play
                    ):
                    self.LOGGER.debug('btn clicked, stop current')
                    if self.playing_btn is not None:
                        self.playing_btn.stop()
                    self.playing_btn = btn
                    self.next_btn = None
                    self.next_countdown = -1
                    self.auto_play = False


if __name__ == '__main__':
    import os
    from wordson.bashlog import getlogger
    from wordson.util import PROJECTDIR
    from wordson.color import white
    getlogger(logging.getLogger(), logging.DEBUG)
    cfg = Config()

    pygame.init()
    screen = pygame.display.set_mode(cfg.screen)
    pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)

    run = True
    clock = pygame.time.Clock()
    count = 0

    pygame.mixer.init()
    pygame.mixer.set_num_channels(11)

    # sound_btn = SoundButton(tool.render(cfg.font, 'Play >>'), os.path.join(PROJECTDIR, 'words', 'test1.wav'), 10)
    sound_btns = SoundButtonGroup(
    # (20, 50),
    # 500,
    [
        {
            'text': 'test1',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test1.wav'),
        },
        {
            'text': 'long long long long test2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        },
        {
            'text': 'fake',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test1.wav'),
        },
        {
            'text': 'fake2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        },
        {
            'text': 'fake2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        },
        {
            'text': 'fake2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        },
        {
            'text': 'fake2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        },
        {
            'text': 'fake2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        },
        {
            'text': 'fake2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        },
        {
            'text': 'fake2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        },
        {
            'text': 'fake2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        },
        {
            'text': 'fake2',
            'sound_path': os.path.join(PROJECTDIR, 'words', 'test2.wav'),
        }
    ])

    sound_btns.rearange((50, 70), 300)
    sound_btns.play()

    while run:
        for event in pygame.event.get():
            sound_btns.handle(event)
            if event.type == pygame.QUIT:
                run = False

        inter = clock.tick(cfg.tick)
        sound_btns.update(inter)
        screen.fill(white)
        sound_btns.draw(screen)
        pygame.display.flip()
        count += 1
        # cond = (count - (count // 200) * 200)
        # if cond < 100:
        #     sound_btn.set_image(tool.render(cfg.font, 'Play ..'))
        # else:
        #     sound_btn.set_image(tool.render(cfg.font, 'Play >>'))

    pygame.quit()
