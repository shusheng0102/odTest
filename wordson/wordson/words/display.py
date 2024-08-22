import json
import sys
import itertools

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    wordlist = json.load(f)

templ = """
{word} | {typ} | {mean}
"""

print("""
word | type | meaning
-----|------|------------
""".strip())
for record in wordlist:
    words = record['word']
    meanings = record['meaning']

    for word, meaning in itertools.zip_longest(words, meanings):
        if meaning is None:
            typ = ''
            mean = ''
        else:
            typ = meaning[0] or None
            mean = meaning[1] or None
        line = templ.format(
            word=word or '',
            typ=typ,
            mean=mean
        )
        print(line.strip())
