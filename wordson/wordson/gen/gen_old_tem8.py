import random
import time
import json
import tempfile
import sys
import os
import logging
import base64

import requests

from wordson.gen.gensource import GenSource

if sys.version_info[0] < 3:
    try:
        from io import open
    except ImportError:
        from codecs import open


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class GenOldTEM8(GenSource):

    SEED = 0
    LOGGER = logging.getLogger('wordson.gen.gen_old_tem8.GenOldTEM8')

    def __init__(self, practice_day):
        name = time.strftime('%Y-%m-%d', time.localtime())
        super(GenOldTEM8, self).__init__('English', u'daily-tem8', name)
        self.start = (practice_day - 1) * 20
        self.end = self.start + 20

    def get_source(self):
        source_file = os.path.join(self.WORDSDIR, 'TEM8-old', 'tem8_all.json')
        with open(source_file, 'r', encoding='utf-8') as f:
            source_all = json.load(f)
        random.seed(self.SEED)
        random.shuffle(source_all)
        source_need = source_all[self.start: self.end]

        self.old_source_id_to_info = dict(('_'.join(each['word']), each) for each in source_need)

        return ((key, value['word']) for key, value in self.old_source_id_to_info.items())

    def get_meaning(self, word_id):
        info = self.old_source_id_to_info[word_id]
        old_meaning_info = info['meaning']
        result = []
        for old_type, old_meaning in old_meaning_info:
            if old_type is None:
                new_type = None
            else:
                new_type = [old_type]
            new_meaning = [old_meaning]
            result.append({
                'type': new_type,
                'meaning': new_meaning,
            })
        return result

    def get_pronunciation(self, word_id):
        words = self.old_source_id_to_info[word_id]['word']
        word = words[0]

        result = []

        temp_dir = tempfile.gettempdir()
        info_file = os.path.join(temp_dir, word + '.json')

        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                pr_info = json.load(f)
        except (FileNotFoundError, IOError):
            self.LOGGER.info('get from merriam for %s', word)
            pr_info = self.pronunciation_from_merriam(word)

            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(pr_info, f)

        for sound_mark, sound_url in pr_info.items():
            # sound_mark_b64 = self.str_b64(sound_mark)
            # sound_mark_b64 = word
            sound_mark_safe = sound_mark
            sound_wav = os.path.join(temp_dir, sound_mark_safe + '.wav')
            sound_mp3 = os.path.join(temp_dir, sound_mark_safe + '.mp3')
            try:
                with open(sound_wav, 'rb') as f:
                    wav_bin = f.read()
            except (FileNotFoundError, IOError):
                if not os.path.isfile(sound_mp3):
                    self.LOGGER.info('get from merriam for %s, mp3 %s', word, sound_url)
                    resp = requests.get(sound_url)
                    assert 200 <= resp.status_code < 300

                    self.LOGGER.info('save mp3 to %s', sound_mp3)
                    with open(sound_mp3, 'wb') as f:
                        f.write(resp.content)

                    assert os.path.isfile(sound_mp3)

                self.LOGGER.info('conver %s to %s', sound_mp3, sound_wav)
                try:
                    self.ffmpeg_convert(sound_mp3, sound_wav)
                except BaseException:
                    try:
                        os.remove(sound_wav)
                    except BaseException:
                        pass
                    raise
                with open(sound_wav, 'rb') as f:
                    wav_bin = f.read()

                result.append((sound_mark, wav_bin))
            else:
                result.append((sound_mark, wav_bin))

        return self.ONE2ONE, result

    @staticmethod
    def str_b64(s):
        return base64.b64encode(s.encode('utf-8')).decode('utf-8')

if __name__ == '__main__':
    from wordson.bashlog import getlogger
    getlogger(None, logging.DEBUG)

    _, day_str = sys.argv

    pract = int(day_str)

    saver = GenOldTEM8(pract)
    saver.run()
    saver.save()
