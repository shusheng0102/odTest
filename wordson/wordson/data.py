import json
import os
import sys
import logging

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.minsix import open
from wordson.minsix import input
from wordson.config import Config
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.data')


cfg = Config()


class Data(object):
    '''Model part of the game. Deal data only.'''
    _ins = None

    def __new__(cls):
        if cls._ins is None:
            ins = super(Data, cls).__new__(cls)

            # load the words data
            fullpath = os.path.normpath(os.path.abspath(os.path.join(PROJECTDIR, cfg.data_cfg)))
            logger.info('full data config path: %s', fullpath)
            if not os.path.exists(fullpath):
                logger.warning('%s not found. create a empty one', fullpath)
                cls.makeconfig(fullpath, [])

            ins._data_file = open(fullpath, 'r+', encoding='utf-8')
            ins.attr = json.load(ins._data_file)
            path = os.path.dirname(fullpath)    # it's abs path
            ins._data_path = path

            # path is abspath, so this is abspath
            known = set(os.path.normpath(os.path.join(path, attr['folder'])) for attr in ins.attr)
            for dirpath, dirnames, filenames in os.walk(path):
                for eachfile in filenames:
                    # seems path is abspath, then this is abspath
                    filepath = os.path.join(dirpath, eachfile)
                    if not filepath.endswith('.json') or filepath == fullpath:
                        logger.debug('%s is not a json file or is config file', eachfile)
                        continue
                    assert os.path.isabs(filepath)
                    if filepath not in known:
                        relpath = os.path.relpath(filepath, path)
                        name = os.path.split(filepath)[-1]
                        name = os.path.splitext(name)[0]
                        ins.attr.append({
                            'name': name,
                            'path': relpath,
                            'language': None,
                            'category': None
                        })

            # load the saving
            # todo: support multi save point
            fullpath = os.path.normpath(os.path.abspath(os.path.join(PROJECTDIR, cfg.save_cfg)))
            if os.path.isfile(fullpath):
                cls._save_file = open(fullpath, 'r+', encoding='utf-8')
                try:
                    cls.save_data = json.load(cls._save_file)
                except BaseException as e:
                    logger.error(e)
                    cls.save_data = None
            else:
                cls.save_data = None
            cls._save_file_path = fullpath
            # if not os.path.exists(fullpath):
            #     logger.warning('%s not exists, create', fullpath)
            #     cls.makeconfig(fullpath, [])
            # ins._save_file = open(fullpath, 'r+', encoding='utf-8')
            # ins.saved = json.load(ins._save_file)
            #
            # for dirpath, dirnames, filenames in os.walk(os.path.dirname(fullpath)):
            #     for eachfile in filenames:
            #         filepath = os.path.join(dirpath, eachfile)
            #         if not filepath.endswith('.json') or filepath == fullpath:
            #             logger.debug('%s is not a json file or is config file', eachfile)
            #             continue
            #         pass

            cls._ins = ins

        return cls._ins


    def get_cates(self):
        '''get_cates() -> set
        get all categories
        None in set means unknown'''
        return {each['category'] for each in self.attr}

    def get_langs(self):
        '''get_langs -> set
        get all languages
        None in set means unknown'''
        return {each['language'] for each in self.attr}

    def get_cates_under(self, language):
        '''get_cates_under(language) -> set
        get all categories under language
        language=None means unknown language'''
        logger.debug('language %s', language)
        result = set()
        for each in self.attr:
            if each['language'] == language:
                result.add(each['category'])
        return result

    def get_name_under(self, language, category):
        '''get_name_path_under(language, category) -> set'''
        logger.debug('language %s; category %s', language, category)
        # result = set()
        result = []
        for each in self.attr:
            if each['language'] == language and each['category'] == category:
                # result.add(each['name'])
                result.append(each['name'])
        return result

    def get_under(self, language, category, lib):
        '''get_under(language, category, lib) -> dict'''
        for each in self.attr:
            if (each['language'] == language
                    and each['category'] == category
                    and each['name'] == lib):
                path = os.path.join(each['folder'], each['words'])
                abspath = os.path.join(self._data_path, path)
                logger.info('open %s', abspath)
                with open(abspath, 'r', encoding='utf-8') as f:
                    return abspath, json.load(f)

    def set_current(self, path):
        with open(path, 'r', encoding='utf-8'):
            self.source = json.load(path)

    @staticmethod
    def makeconfig(path, obj):
        dirname = os.path.dirname(path)
        if os.path.exists(dirname):
            if not os.path.isdir(dirname):
                msg = '%s exists and is not a folder'
                logger.critical(msg)
                raise ValueError(msg)
        else:
            os.makedirs(dirname)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)

    def save_game(self, obj):
        path = os.path.dirname(self._save_file_path)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(self._save_file_path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)

        self.__class__.save_data = obj

    def load_game(self):
        with open(self._save_file_path, 'r', encoding='utf-8') as f:
            obj = json.load(f)
        self.__class__.save_data = obj
        return obj

    def __del__(self):
        self._data_file.close()


if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)
    data = Data()

    print(data.get_cates())
    lang = data.get_langs()
    for each in lang:
        for cate in data.get_cates_under(each):
            print(each, cate, ':')
