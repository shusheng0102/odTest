import os
import sys
import logging
import subprocess
import json

from bs4 import BeautifulSoup
import requests

from wordson.util import PROJECTDIR

if sys.version_info[0] < 3:
    try:
        from io import open
    except ImportError:
        from codecs import open

try:
    FileExistsError
except NameError:
    FileExistsError = OSError

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

class GenSource(object):

    LOGGER = logging.getLogger('wordson.gen.gensource.GenSource')

    WORDSDIR = os.path.join(PROJECTDIR, 'words')

    MIXED = 0
    ONE2ONE = 1

    def __init__(self, language, category, name):
        self.language = language
        self.category = category
        self.name = name

        self.rel_folder = os.path.join(language, category, name)
        self.save_folder = os.path.join(self.WORDSDIR, self.rel_folder)
        self.save_file = os.path.join(self.save_folder, 'index.json')

        self.result = []

    def run(self):
        result = self.result
        try:
            os.makedirs(self.save_folder)
        except (FileExistsError, OSError):
            pass

        for word_id, word in self.get_source():
            meaning = self.get_meaning(word_id)
            pr = self.get_pronunciation(word_id)
            if pr is None:
                pronunciation = None
            else:
                # pronunciation = None
                if pr[0] == self.MIXED:
                    _, sound_marks, wav_binaries = pr
                    sound_fnames = []
                    for index, wav_bin in enumerate(wav_binaries):
                        fname = '{}-{}.wav'.format(word_id, index)
                        fpath = os.path.join(self.save_folder, fname)
                        with open(fpath, 'wb') as f:
                            f.write(wav_bin)
                        sound_fnames.append(fname)
                    pronunciation = {
                      "mode": "mixed",
                      "value": {
                        "soundmarks": sound_marks,
                        "soundpaths": sound_fnames
                      }
                    }

                elif pr[0] == self.ONE2ONE:
                    _, marks_binaries_pari = pr
                    value = []
                    for index, (sound_mark, wav_bin) in enumerate(marks_binaries_pari):
                        fname = '{}-{}.wav'.format(word_id, index)
                        fpath = os.path.join(self.save_folder, fname)
                        with open(fpath, 'wb') as f:
                            f.write(wav_bin)
                        value.append({
                            "soundmark": sound_mark,
                            "soundpath": fname
                        })
                    pronunciation = {
                      "mode": "one2one",
                      "value": value
                    }
                else:
                    pronunciation = None
                    assert False

            word_info = {
                'word': word,
                'meaning': meaning,
                'pronunciation': pronunciation,
            }

            self.LOGGER.info(word_info)
            result.append(word_info)

    def save(self):
        try:
            os.makedirs(self.save_folder)
        except FileExistsError:
            pass

        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(self.result, f, indent=4, ensure_ascii=False)

        config = {
            'name': self.name,
            'language': self.language,
            'category': self.category,
            'folder': self.rel_folder,
            'words': 'index.json',
        }

        config_file = os.path.join(self.WORDSDIR, 'index.json')
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_full = json.load(f)
        except (FileNotFoundError, IOError):
            config_full = []

        for each in config_full:
            # no dup save
            if each == config:
                break
        else:
            config_full.append(config)

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_full, f, indent=4, ensure_ascii=False)

    def get_source(self):
        """
        e.g.

        {
            'word_id': ['spell1', 'spell2'],  // list, required
        }.items()
        """
        pass

    def get_meaning(self, word_id):
        """
        e.g.

        [
            {
              "type": ["n"],  // list, None when not avaliable
              "meaning": ["测试"]  // required, list
            },
            {
              "type": ["v"],
              "meaning": ["测试动词"]
            }
        ]
        """
        pass

    def get_pronunciation(self, word_id):
        """
        three mode:

        return self.MIXED, ["soundmark1", "soundmark2"], [<wav-binary>, <wav-binary>, <wav-binary>]
        return self.ONE2ONE, [
            ("soundmark1", <wav-binary>),
            ("soundmark2", <wav-binary>),
        ]
        """
        pass

    @staticmethod
    def pronunciation_from_merriam(word):
        page_url = 'https://www.merriam-webster.com/dictionary/{}'.format(word)
        resp = requests.get(page_url)
        assert 200 <= resp.status_code < 300, resp.status_code
        soup = BeautifulSoup(resp.content, 'html5lib')

        result = {}

        for pr in soup.find_all(class_='pr'):
            # print(pr)
            sound_mark = pr.text.strip()
            print(sound_mark)
            prs = pr.parent
            # print(prs)
            a = prs.find('a')
            a_data_file = a.get('data-file')
            assert a_data_file is not None
            a_data_dir = a.get('data-dir')
            assert a_data_dir is not None
            sound_url = 'https://media.merriam-webster.com/audio/prons/en/us/mp3/{}/{}.mp3'.format(a_data_dir, a_data_file)
            print(sound_url)
            result[sound_mark] = sound_url

        return result

    @staticmethod
    def ffmpeg_convert(infile, outfile, ffmpeg='/usr/bin/ffmpeg'):
        cmd = [
            ffmpeg,
            '-y',
            '-i', infile,
            '-strict', '-2',
            # '-an',
            outfile
        ]

        return subprocess.check_call(cmd)


if __name__ == '__main__':
    import sys
    resp = GenSource.pronunciation_from_merriam(sys.argv[1])
    print(resp)
