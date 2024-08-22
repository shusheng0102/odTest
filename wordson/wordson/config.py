import os
import sys
import imp
import logging
import json
import pygame

from wordson.minsix import open
from wordson.bashlog import getlogger
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.config')


class Config(object):
    _ins = None

    page_main = 0
    page_lang = 1
    page_cate = 2
    page_lib  = 3
    page_mode = 4
    page_game = 5
    page_load = 6
    page_end  = 7

    def __new__(cls):
        if cls._ins is None:
            ins = super(Config, cls).__new__(cls)
            ins.file = open(os.path.join(PROJECTDIR, 'config.json'))
            obj = json.load(ins.file)
            ins.screen = tuple(obj.pop('screen'))

            ins._fontpath = obj.pop('font')
            ins._fontsize = obj.pop('fontsize')
            ins._font = None

            for k, v in obj.items():
                setattr(ins, k, v)

            with open(os.path.join(PROJECTDIR, 'i18n', 'wordson_zh_CN.json'), 'r', encoding='utf-8') as f:
                lang = json.load(f)
                _lang = lang.pop('_lang')
                for k, v in lang.items():
                    setattr(ins, k, v)

            cls._ins = ins
        return cls._ins

    @property
    def font(self):
        # lazy load
        if self._font is None:
            self._font = pygame.font.Font(os.path.join(PROJECTDIR, self._fontpath), self._fontsize)
        return self._font

    def new_font(self, size=None, path=None):
        if size is None:
            size = self._fontsize
        if path is None:
            path = self._fontpath
        return pygame.font.Font(os.path.join(PROJECTDIR, path), size)

    def __del__(self):
        self.file.close()


if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)
    config = Config()
    print(config.tick)
    print(config.screen)
