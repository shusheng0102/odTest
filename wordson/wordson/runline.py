import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson.role import Role
from wordson.block import Block
from wordson.block import BlockGroup
from wordson.sprite import Group
from wordson.sprite import Sprite
from wordson import events
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.runline')


cfg = Config()


class RunLine(Group):
    event_list = []
    def __init__(self, ground=None, rolepos=None, speed=None):
        super(RunLine, self).__init__()
        self.ground = ground if ground is not None else cfg.ground
        self.role = Role()
        self.block_group = BlockGroup()

        # self.width = width or cfg.screen[1]

        if rolepos is None:
            rolepos = cfg.rolepos
        self.role.rect.x = rolepos
        self.role.bottom = self.ground
        self.role.to_run()

        width = cfg.screen[-1]
        gap = cfg.gap
        posation = width

        rest = width - rolepos
        num = rest // gap
        for idx in range(num+1):
            x = (idx + 1) * gap + rolepos
            block = self.newblock(x)
            logger.debug('new block at %s', block.rect)
            self.block_group.add(block)
            self.add(block)

        ground_line = Sprite()
        ground_line.image = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'ground.png')).convert_alpha()
        ground_line.rect = ground_line.image.get_rect()
        ground_line.rect.y = self.ground - 5
        self.ground_line = ground_line


        self.extend(self.role, self.block_group, self.ground_line)

    # wait = False
    def update(self, time):
        sprites = self.block_group.sprites()
        screen_w, screen_h = cfg.screen

        # add block if nessessary
        if not sprites:
            need_add = True    # no block. Add one
        else:
            last_sprite = sprites[-1]
            need_add = (screen_w - last_sprite.rect.right >= cfg.gap)    # over the gap. Add a new one

        if need_add:
            block = self.newblock()
            logger.debug('add block at %s', block.rect)
            self.block_group.add(block)
            self.add(block)

        first_sprite = sprites[0] if sprites else self.block_group.sprites()[0]    # sprites can be empty

        collide = (self.role.rect.right >= first_sprite.rect.left-20 and self.role.rect.right < first_sprite.rect.right)

        if collide:
            # logger.debug('collide')
            if not self.event_list:
                if self.role.status == self.role.RUN:
                    self.role.to_wait()
                    self.stop_roll()
                    # self.wait = True
            elif not first_sprite.acted:
                evt = self.event_list.pop(0)
                if evt == self.role.JUMP and self.role.status != self.role.JUMP:
                    self.resume_roll()
                    self.role.to_jump()
                    first_sprite.acted = True
                elif evt == self.role.ROLL and self.role.status != self.role.ROLL:
                    self.resume_roll()
                    self.role.to_roll()
                    first_sprite.acted = True

        role_status = self.role.status
        role_result = self.role.update(time)

        if role_status not in (self.role.RUN, self.role.WAIT) and role_result:
            self.role.to_run()
        self.block_group.update(time)


    @classmethod
    def newblock(self, x=None):
        block = Block()
        block.rect.bottom = cfg.ground + 10
        block.rect.left = cfg.screen[0] if x is None else x
        return block


    def draw(self, surface):
        self.block_group.draw(surface)
        # self.role.draw(surface)
        self.ground_line.draw(surface)
        surface.blit(self.role.image, self.role.rect)


    def pause(self):
        self.role.pause()
        self.block_group.pause()

    def unpause(self):
        self.role.unpause()
        self.block_group.unpause()

    def stop_roll(self):
        self.role.stop_roll()
        self.block_group.stop_roll()

    def resume_roll(self):
        self.role.resume_roll()
        self.block_group.resume_roll()

    def handle(self, event):
        event_type = event.type

        if event_type == events.PAUSE:
            self.role.pause()
            self.block_group.pause()
            return

        if event_type == events.UNPAUSE:
            self.role.unpause()
            self.block_group.unpause()
            return

    def jump_next(self):
        self.event_list.append(self.role.JUMP)

    def roll_next(self):
        self.event_list.append(self.role.ROLL)

    def clear(self):
        self.event_list[:] = list()


if __name__ == '__main__':
    getlogger(logger, logging.DEBUG)
    import random

    pygame.init()
    screen = pygame.display.set_mode(cfg.screen)

    group = RunLine()

    run = True
    clock = pygame.time.Clock()
    pygame.display.flip()
    while run:
        run += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            group.handle(event)

        inter = clock.tick(cfg.tick)
        group.update(inter)
        # if run % 2:
        #     pygame.event.post(events.roll())
        # else:
        #     pygame.event.post(events.jump())
        screen.fill((255, 255, 255))
        group.draw(screen)
        pygame.display.flip()

    pygame.quit()
