from pygame.event import Event
from pygame import USEREVENT, NUMEVENTS

# __all__ = ('pause', 'unpause', 'jump', 'roll')

PAUSE, UNPAUSE, SWITCHPAGE, ANSWER, RESULT, NEXTTOPIC, WORDSOUND, \
    SAVE, LOAD = list(range(USEREVENT, USEREVENT + 9))
assert LOAD <= NUMEVENTS

TYPESOUNDBUTTONCLICK = 0
TYPESOUNDEND = 1

def pause(**attributes):
    return Event(PAUSE, **attributes)


def unpause(**attributes):
    return Event(UNPAUSE, **attributes)


def switchpage(**attributes):
    return Event(SWITCHPAGE, **attributes)


def answer(answer, **attributes):
    return Event(ANSWER, answer=answer, **attributes)


def result(currect, answer=None, **attributes):
    return Event(RESULT, currect=currect, answer=answer, **attributes)


def nexttopic(**attributes):
    return Event(NEXTTOPIC, **attributes)


def save(**attributes):
    return Event(SAVE, **attributes)


def load(**attributes):
    return Event(LOAD, **attributes)
