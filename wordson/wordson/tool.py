import os
import sys
import pygame


from wordson import color


def render(font, text, color=color.black, center=False, line_gap=0):
    '''render(font, text, color=color.black, center=False) -> Surface
    center is used when text is multi line. If center=True then each line is centered
    line_gap is used when text is multi line. It decides the gap of each line'''
    if not '\n' in text:
        return font.render(text, True, color, None)

    lines = text.splitlines()
    surfs = []
    for each in lines:
        surfs.append(font.render(each, True, color, None))

    width = 0
    height = 0
    for each in surfs:
        w, h = each.get_rect().size
        width = max(width, w)
        height = max(height, h)
    height = (height + line_gap) * len(surfs) - line_gap
    surf = pygame.Surface((width, height), flags=pygame.SRCALPHA)

    top = 0
    for each in surfs:
        rect = each.get_rect()
        if center:
            w = rect.width
            left = (width - w) / 2
        else:
            left = 0
        surf.blit(each, (left, top))
        top += (line_gap + rect.height)

    return surf

class Timer(object):
    def __init__(self):
        self.time = 0
        self.running = False

    def start(self):
        self.time = 0
        self.running = True

    def stop(self):
        self.running = False
        return self.time

    def pause(self):
        self.running = False
        return self.time

    def unpause(self):
        self.running = True
        return self.time

    def update(self, time):
        if self.running:
            self.time += time
        return self.time

    @property
    def formatted(self):
        seconds = self.time // 1000
        s = seconds % 60
        minutes = seconds // 60
        m = minutes % 60
        hours = minutes // 60
        return '%d:%02d:%02d'%(hours, m, s)
