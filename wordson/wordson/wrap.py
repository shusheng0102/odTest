# coding: utf-8
import re

try:
    reduce
except NameError:
    from functools import reduce


class Wrapper(object):

    p = re.compile("([\u2e80-\uffff])")  #, re.UNICODE)
    width = 50
    seps = [' ','\n', '']

    def __init__(self, text='', width=50):
        self.text = text
        self.width = width

    def _to_line(self, line, word):
        idx = (len(line)-line.rfind('\n')-1 + len(word.split('\n',1)[0]) >= self.width
                    or line[-1:] == '\0'
                    and 2)
        sep = self.seps[idx]
        return '%s%s%s' % (line, sep, word)

    def wrap(self, text=None):
        if text is None:
            text = self.text
        replaced = self.p.sub(r'\1\0 ', text).split(' ')
        # return [self._to_line(x) for x in replaced]
        return reduce(self._to_line, replaced).replace('\0', '')


if __name__ == '__main__':
    s = '''中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文
    中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文
    中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文
    中文 中文
    中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文
    中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文 中文
    中文 中文 中文 中文 中文
    中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文中文
    中英ChineseEnglish中英ChineseEnglish中英ChineseEnglish中英ChineseEnglish中英ChineseEnglish中英ChineseEnglish中英ChineseEnglish中英ChineseEnglish中英Chin'''

    wrapper = Wrapper(s, 40)
    print(wrapper.wrap())
