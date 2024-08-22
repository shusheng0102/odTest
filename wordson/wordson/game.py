# coding: utf-8
import os
import sys
import logging
import random
import time

import pygame

from wordson.import_init import screen
from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson.data import Data
from wordson.minsix import Str
from wordson import color, events
from wordson.mainpage import MainPage
from wordson.scrollpage import LanguagePage, CategoryPage, LibPage
from wordson.gamepage import GamePage
from wordson.modepage import ModePage
from wordson.endpage import EndPage
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.game')

cfg = Config()
data = Data()


try:
    any
except NameError:

    def any(iterable):
        for each in iterable:
            if each:
                return True
        return False


class Game(object):
    """The Controller of the game"""

    LOGGER = logging.getLogger('wordson.game')

    def __init__(self):
        # pygame.init()
        # self.screen = pygame.display.set_mode(cfg.screen)
        self.screen = screen

        self._main_page = MainPage()
        self.lang_page = LanguagePage(data.get_langs())
        self.mode_page = ModePage()
        self.load_page = None
        self.game_page = GamePage()

        self.current_page = self.main_page

        self.running = True

        # self.all_source = {}    # store the all data.
        # self.rest_source = {}    # store the untested data.
        # self.wrong = {}    # store all wrong answer. format: {'word': int}
        # self.current_word = None    # current word for the topic
        # self.current_answer = None

        self.source_file = None

        self.raw_source = []
        self.all_source = []
        # self.rest_source = []
        self.current_index = -1
        self.current_answer = 0
        self.current_answer_type = None
        self.current_answer_display = None

        self.wrong_indexes = []
        self.unpassed_indexes = []

    @property
    def main_page(self):
        page = self._main_page
        saved_data = data.save_data
        if saved_data is not None:
            saved_time = self.format_time(saved_data['time'])
            page.set_load_date(saved_time)
        return page

    @property
    def end_page(self):
        total = len(self.all_source)
        right = total - len(self.wrong_indexes)
        wrong_and_num = []
        for wrong_index in set(self.wrong_indexes):
            wrong_word = self.all_source[wrong_index]
            write_as = ', '.join(wrong_word['word'])
            wrong_count = self.wrong_indexes.count(wrong_index)
            wrong_and_num.append((write_as, wrong_count))

        used_time = self.game_page.get_formatted_time()
        return EndPage(used_time, (right, total), wrong_and_num, self.repeat_word)

    def cache_cate(func):
        cached = {}
        def warpper(self):
            return cached.setdefault(self.lang, func(self))
        return warpper

    @property
    @cache_cate
    def cate_page(self):
        return CategoryPage(data.get_cates_under(self.lang))

    def cache_lib(func):
        cached = {}
        def warpper(self):
            return cached.setdefault((self.lang, self.cate), func(self))
        return warpper

    @property
    @cache_lib
    def page_lib(self):
        result = data.get_name_under(self.lang, self.cate)
        return LibPage(result)

    def run(self):

        pygame.key.set_repeat(cfg.key_repeat_delay, cfg.key_repeat_interval)
        pygame.display.set_caption(cfg.title)

        screen = self.screen

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if self.current_page.handle(event):
                    continue
                if self.handle(event):
                    continue

            interval = clock.tick(cfg.tick)
            self.current_page.update(interval)
            screen.fill(color.white)
            self.current_page.draw(screen)
            pygame.display.flip()

        pygame.quit()

    def handle(self, event):
        if event.type == pygame.QUIT:
            logger.info('exit...')
            self.running = False
            return True
        if event.type == events.SWITCHPAGE:
            to = event.to
            logger.debug('switch page %s', event)
            if to == cfg.page_main:
                logger.info('to main page')
                self.current_page = self.main_page
                # if hasattr(self, 'lang'):
                #     del self.lang
            elif to == cfg.page_lang:
                logger.info('to language page')
                self.current_page = self.lang_page
                if hasattr(self, 'lang'):
                    del self.lang
            elif to == cfg.page_cate:
                logger.info('to category page')
                if event.by == cfg.page_lang:
                    self.lang = event.lang
                self.current_page = self.cate_page
            elif to == cfg.page_lib:
                logger.info('to lib page')
                if event.by == cfg.page_cate:
                    self.cate = event.cate
                self.current_page = self.page_lib
            elif to == cfg.page_mode:
                logger.info('to mode page')
                if event.by == cfg.page_lib:
                    self.lib = event.lib
                self.current_page = self.mode_page
            elif to == cfg.page_load:
                self.current_page = self.load_page
            elif to == cfg.page_game:
                self.show_type = event.show_type
                self.show_1st_char = event.show_1st_char
                self.repeat_word = event.repeat

                self.write_word = event.write_word
                self.choose_word = event.choose_word
                self.choose_meaning = event.choose_meaning
                self.play_sound = event.play_sound
                self.shuffle = event.shuffle
                lang = self.lang
                cate = self.cate
                lib  = self.lib
                logger.info('to game page [%s - %s - %s]; '
                            'write_word: %s, choose_word: %s, choose_meaning: %s; '
                            'play_sound: %s; shuffle: %s '
                            'show_type, %s; show_1st_char %s; repeat: %s',
                            lang, cate, lib,
                            self.write_word, self.choose_word, self.choose_meaning,
                            self.play_sound, self.shuffle,
                            self.show_type, self.show_1st_char, self.repeat_word)

                self.game_page.clear()
                self.load_data(lang, cate, lib)
                self.current_page = self.game_page

            elif to == cfg.page_end:
                self.current_page = self.end_page

            logger.debug('event %s handled by game', event)
            return True

        # required to check if the answer is correct
        elif event.type == events.ANSWER:
            # answer = event.answer
            self.handle_answer(event.answer)
            return True

        # required to renew the topic
        elif event.type == events.NEXTTOPIC:
            self.set_new_topic()
            self.set_process()
            logger.debug('event %s handled by game', event)
            return True

        # required to save the game
        elif event.type == events.SAVE and not hasattr(event, 'msg'):
            self.save_game()
            logger.debug('save event %s handled by game', event)
            return True

        # required to load the game
        elif event.type == events.LOAD:
            if data.save_data:
                logger.debug('found save')
                self.load_game()
            logger.debug('save event %s handled by game', event)
            return True

    def get_time(self, strtime=None):
        if strtime is None:
            return time.time()
        timestruct = time.strptime(strtime, '%Y-%m-%d %H:%M:%S')
        return time.mktime(timestruct)

    def format_time(self, thetime=None):
        if thetime is None:
            thetime = time.localtime()
        else:
            thetime = time.localtime(thetime)
        return time.strftime('%Y-%m-%d %H:%M:%S', thetime)

    def save_game(self):
        obj = {}
        obj['config'] = {
            'show_type': self.show_type,
            'show_1st_char': self.show_1st_char,
            'repeat': self.repeat_word,
            'write_word': self.write_word,
            'choose_word': self.choose_word,
            'choose_meaning': self.choose_meaning,
            'play_sound': self.play_sound,
        }

        obj['language'] = self.lang
        obj['category'] = self.cate
        obj['lib'] = self.lib
        obj['time'] = self.get_time()
        obj['used_time'] = self.game_page.get_time()

        source = []
        for word, meaning in self.all_source.items():
            source.append(
                {'word': word,
                 'meaning': meaning}
            )
        obj['source'] = source

        wrong = []
        for word, times in self.wrong.items():
            wrong.append(
                {'word': word,
                 'time': times}
            )
        obj['wrong'] = wrong

        rest = []
        for word, _ in self.rest_source.items():
            rest.append(word)
        obj['rest'] = rest

        evt = events.save()
        try:
            data.save_game(obj)
        except BaseException as e:
            msg = str(e)
            logger.error(msg)
        else:
            msg = None
        evt.msg = msg
        logger.debug('post save done event %s', evt)
        pygame.event.post(evt)

    def load_game(self):
        obj = data.load_game()
        self.game_page.set_time(obj['used_time'])
        self.lang = obj['language']
        self.cate = obj['category']
        self.lib = obj['lib']

        all_source = {}
        for each in obj['source']:
            all_source[tuple(each['word'])] = each['meaning']
        self.all_source = all_source

        rest_source = {}
        for word in obj['rest']:
            word = tuple(word)
            rest_source[word] = all_source[word]
        self.rest_source = rest_source

        wrong = {}
        for each in obj['wrong']:
            wrong[tuple(each['word'])] = each['time']
        self.wrong = wrong

        config = obj['config']
        pygame.event.post(events.switchpage(by=cfg.page_main, to=cfg.page_game, **config))

    def handle_answer(self, answer):

        current_answer = self.current_answer
        current_answer_type = self.current_answer_type

        assert current_answer_type is not None

        if current_answer_type == 'choose':
            result = answer == current_answer
            self.LOGGER.debug('answer=%r, expect=%r, result=%s', answer, current_answer, result)
        else:
            word = self.all_source[self.current_index]
            result = any(answer.lower().strip() == each.lower().strip() for each in word['word'])

        evt = events.result(result, self.current_answer_display)
        logger.info('for answer %s, post %s', answer, evt)
        pygame.event.post(evt)

        if result:    # record the error
            # passed
            self.unpassed_indexes.remove(self.current_index)
        else:
            # self.wrong.append = self.wrong.append(self.current_index)
            self.wrong_indexes.append(self.current_index)
            if self.current_index not in self.unpassed_indexes:
                self.unpassed_indexes.append(self.current_index)

        self.LOGGER.debug('unpass=%s, wrong=%s', self.unpassed_indexes, self.wrong_indexes)

    def switch_end(self):
        assert False

    def load_data(self, lang, cate, lib):
        source_file, source_data = data.get_under(lang, cate, lib)
        self.source_file = source_file

        self.raw_source = source_data
        self.all_source = list(source_data)

        if self.shuffle:
            random.shuffle(self.all_source)

        self.current_index = -1
        self.current_answer = 0
        self.current_answer_type = None

        self.wrong_indexes = []
        self.unpassed_indexes = list(range(0, len(self.all_source)))

        self.set_new_topic()

    def set_process(self):
        page = self.game_page
        allnum = len(self.all_source)
        restnum = len(self.unpassed_indexes)
        result =  (allnum - restnum) * 100 / allnum
        page.set_process(result)

    def set_new_topic(self):

        index_pool = list(self.unpassed_indexes)

        if not index_pool:
            return pygame.event.post(events.switchpage(to=cfg.page_end))

        if len(index_pool) > 1 and self.current_index in index_pool:
            self.LOGGER.debug('remove %s from %s', self.current_index, index_pool)
            index_pool.remove(self.current_index)

        current_index = self.current_index = random.choice(index_pool)

        funcs = []
        if self.write_word:
            funcs.append(self.new_write_word)
        if self.choose_word:
            funcs.append(self.new_choose_word)
        if self.choose_meaning:
            funcs.append(self.new_choose_meaning)

        func = random.choice(funcs)
        current_word = self.all_source[current_index]
        self.LOGGER.debug('picking word %s, %s', current_index, current_word)
        title, options, placeholder, sound = func(current_index, current_word)
        if not self.play_sound:
            sound = None

        if sound:
            sound = dict(sound)  # copy it
            sound_folder = os.path.normpath(os.path.join(PROJECTDIR, self.source_file, '..'))
            if sound['mode'] == 'mixed':
                sound_pathes = sound['value']['soundpaths']
                for index, sound_path in enumerate(sound_pathes):
                    sound_abs = os.path.join(sound_folder,sound_path)
                    sound_pathes[index] = sound_abs
                    self.LOGGER.debug(sound_abs)

            elif sound['mode'] == 'one2one':
                sound_value = sound['value']
                for each_sound in sound_value:
                    sound_abs = os.path.join(sound_folder, each_sound['soundpath'])
                    each_sound['soundpath'] = sound_abs
                    self.LOGGER.debug(sound_abs)

            else:
                assert False, sound['mode']

            self.LOGGER.debug('sound=%s', sound)

        self.game_page.set(title, options, placeholder, sound)

    def new_write_word(self, current_index, current_word):
        '''give meaning and write word'''

        self.current_answer_type = 'spell'
        self.current_answer = current_index

        title_strs = self.merge_meaning(current_word['meaning'])

        if self.show_1st_char:
            frists = set()
            for each in current_word['word']:
                first = each[0]
                firsts.add(first)
            placeholder = '/'.join(firsts)
        else:
            placeholder = cfg.placeholder

        self.current_answer_display = '/'.join(current_word['word'])

        return title_strs, None, placeholder, current_word['pronunciation']

    def new_choose_word(self, current_index, current_word):
        '''give meaning and choose word'''

        use_source = list(self.all_source)
        use_source.pop(current_index)
        random.shuffle(use_source)
        use_source.insert(0, current_word)

        option_count = min(4, len(use_source))

        options = []
        for each in use_source[:option_count]:
            word = '/'.join(each['word'])
            options.append(word)

        answer_word = options[0]
        self.current_answer_display = answer_word
        random.shuffle(options)
        answer_index = options.index(answer_word)

        self.current_answer = answer_index
        self.current_answer_type = 'choose'

        return self.merge_meaning(current_word['meaning'], sep='; '), options, None, None

    def new_choose_meaning(self, current_index, current_word):
        '''give word choose meaning'''

        use_source = list(self.all_source)
        use_source.pop(current_index)
        random.shuffle(use_source)
        use_source.insert(0, current_word)

        option_count = min(4, len(use_source))

        options = []
        for each in use_source[:option_count]:
            meaning = self.merge_meaning(each['meaning'], sep='; ')
            options.append(meaning)

        answer = options[0]
        self.current_answer_display = answer
        random.shuffle(options)
        answer_index = options.index(answer)

        self.current_answer = answer_index
        self.current_answer_type = 'choose'

        title_strs = ', '.join(current_word['word'])

        return title_strs, options, None, current_word['pronunciation']

    def merge_meaning(self, meaning, sep='\n'):
        merge = []
        show_type = self.show_type
        for each_meaning in meaning:
            meaning_types = each_meaning['type']
            meaning_meanings = each_meaning['meaning']
            meanings_join = '; '.join(meaning_meanings)
            if show_type and meaning_types:
                mean = '[{}] {}'.format('/'.join(meaning_types), meanings_join)
            else:
                mean = meanings_join
            merge.append(mean)

        return sep.join(merge)

def main():
    return Game().run()


if __name__ == '__main__':
    getlogger('wordson', logging.DEBUG)
    logging.getLogger('wordson.runline.role').setLevel(logging.CRITICAL)
    main()
