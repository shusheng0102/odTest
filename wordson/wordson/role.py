import os
import sys
import logging
import pygame

from wordson.bashlog import getlogger, DEBUG
from wordson.tracemore import get_exc_plus
from wordson.config import Config
from wordson.sprite import Sprite
from wordson.util import PROJECTDIR


logger = logging.getLogger('wordson.role')


cfg = Config()


class Role(Sprite):
    RUN = 0
    ROLL = 1
    JUMP = 2
    ROLL = 3
    WAIT = 4
    PAUSE = 5

    JUMPREADY = -1
    JUMPUP = -2
    JUMPTOP = -3
    JUMPDOWN = -4


    def __init__(self):
        super(Role, self).__init__()
        mainsurf = pygame.image.load(os.path.join(PROJECTDIR, 'img', 'role.png')).convert_alpha()
        logger.debug(mainsurf.get_rect())
        self.run_imgs = []
        for x in range(0, 8):
            # # todo: fix this bug
            if x in (1, 2, 3 ,4, 5):
                rect = pygame.Rect(x*99, 0, 96, 99)
            else:
                rect = pygame.Rect(x*99, 0, 91, 99)
            # rect = pygame.Rect(x*99, 0, 91, 99)

            sub = mainsurf.subsurface(rect)

            self.run_imgs.append(sub)
            # path = os.path.join(PROJECTDIR, 'img', 'run200[%d].png'%x)
            # img = pygame.image.load(path).convert_alpha()
            # self.run_imgs.append(img)

        self.jump_imgs = []
        for x in range(7):
            rect = pygame.Rect(x*99, 99, 91, 99)
            # todo: fix this
            if x in (2, 3):
                rect.width += 5
            sub = mainsurf.subsurface(rect)
            self.jump_imgs.append(sub)
            # path = os.path.join(PROJECTDIR, 'img', 'jump_200[%d].png'%x)
            # img = pygame.image.load(path).convert_alpha()
            # self.jump_imgs.append(img)
        self.jump_imgs.extend(self.jump_imgs[1::-1])
        # 0, 1 -> ready to jump
        # 2, 3 -> jumping
        # 4 -> till the top
        # 5, 6 -> falling
        # 7, 8 -> hit the ground

        self.roll_imgs = []
        for x in range(5):
            rect = pygame.Rect(x*99, 205, 99, 99)
            sub = mainsurf.subsurface(rect)
            self.roll_imgs.append(sub)
            # path = os.path.join(PROJECTDIR, 'img', 'roll_120[%d].png'%x)
            # img = pygame.image.load(path).convert_alpha()
            # self.roll_imgs.append(img)

        self.wait_img = mainsurf.subsurface((0, 303, 89, 99))

        self.image = self.run_imgs[0]
        self.rect = self.image.get_rect()
        self.ground = cfg.ground
        self.interval = cfg.role_interval
        self.rect.bottom = self.ground
        self.time = 0

        self.status = self.RUN
        self._prev_status = self.RUN
        self.run_idx = 0
        self.jump_status = self.JUMPUP
        self.jump_idx = 0
        self.forward_speed = 0
        self.roll_idx = 0

        # self.jump_speed = 10
        self.grav = cfg.gravity
        self.upward_speed = cfg.role_upward_speed
        self.now_speed = self.upward_speed

    def update(self, time):
        if self.status == self.RUN:
            result = self.run(time)
        elif self.status == self.JUMP:
            result = self.jump(time)
        elif self.status == self.ROLL:
            result = self.roll(time)
        elif self.status == self.WAIT:
            result = self.wait(time)
        elif self.status == self.PAUSE:
            result = None

        self.time += time
        return result



    def run(self, time):
        a_loop = False
        run_imgs = self.run_imgs
        length = len(run_imgs)
        idx = self.time // self.interval    # floor devide
        if idx >= length:
            a_loop = True
            idx = 0
            self.time = 0    # dont make it too big
        # logger.debug('run time %sms (%sms), idx %s', time, self.time, idx)
        self.image = self.run_imgs[idx]
        self.rect.x += self.forward_speed*time
        self.rect.bottom = self.ground
        return a_loop

    pre_jump_step = 0
    def jump(self, time):
        step = self.time // self.interval

        # logger.debug('jump time %sms (%sms), step %s', time, self.time, step)

        if step < 2:
            # logger.debug('jump %s', step)
            self.jump_idx = step
            self.image = self.jump_imgs[step]
            self.jump_status = self.JUMPREADY

            return False

        elif self.rect.bottom <= self.ground:    # jumpping
            if self.now_speed < 0:
                self.jump_status = self.JUMPUP
            else:
                self.jump_status = self.JUMPDOWN
            if self.jump_idx in (0, 1):
                self.jump_idx = 2
            # logger.debug('bottom %s; ground %s; now_speed %.3f. %s', self.rect.bottom, self.ground, self.now_speed, 'up' if self.jump_status==self.JUMPUP else 'maybe down')

            self.now_speed += self.grav*time
            self.rect.y += self.now_speed*time*0.5


            if self.rect.bottom > self.ground:    # hit the ground
                logger.debug('hit the ground')
                self.rect.bottom = self.ground
                # self.jump_idx = 7
                self.pre_jump_step = step
                return True


            if self.now_speed >= 0 and self.jump_status == self.JUMPUP:    # hit the top
                self.now_speed = 0.2
                self.image = self.jump_imgs[4]
                self.jump_status = self.JUMPTOP
                self.jump_idx = 5
                self.pre_jump_step = step
                return False

            # if step != self.pre_jump_step:
            if step % 2 == 0:
                # jump up
                if self.jump_idx == 2:
                    self.pre_jump_step = 2
                    self.jump_idx = 3
                elif self.jump_idx == 3:
                    self.pre_jump_step = 3
                    self.jump_idx = 2
                # jump down
                elif self.jump_idx == 5:
                    self.pre_jump_step = 5
                    self.jump_idx = 6
                else:
                    self.pre_jump_step = 6
                    self.jump_idx = 5
            self.image = self.jump_imgs[self.jump_idx]
            self.rect.x += self.forward_speed*time

            return False

        else:
            logger.debug('jump finished')
            self.image = self.jump_imgs[8]
            self.rect.bottom = self.ground
            self.time = 0
            # self.time = 0
            # self.to_jump()
            return True

    def roll(self, time):
        step = self.time // self.interval# // 2
        a_loop = False
        length = len(self.roll_imgs)
        if step < length:
            # logger.debug('rolling...')
            self.image = self.roll_imgs[step]
            # logger.debug(self.rect.x)
            self.rect.x += (self.forward_speed*time)
            # logger.debug(self.rect.x)
            # self.roll_idx += 1

        elif step < length+4:
            # logger.debug('roll on ground')
            self.image = self.roll_imgs[length-1]
            # self.rect.x += self.forward_speed
            # self.roll_idx += 1
        else:
            # self.roll_idx = 0
            # self.to_run()
            self.time = 0
            a_loop = True
        return a_loop

    def wait(self, time):
        return True

    def to_run(self, speed=None):
        self.status = self.RUN
        self.time = 0
        if speed is not None:
            self.forward_speed = speed
        # self.image = self.run_imgs[0]
        # self.rect = kwds.get('rect', self.image.get_rect())
        logger.debug('run at %s', self.rect)

    def to_jump(self, ground=None, speed=None, height=None):
        self.status = self.JUMP
        self.jump_status = self.JUMPREADY
        self.jump_idx = 0
        if speed:
            self.upward_speed = speed
        self.now_speed = self.upward_speed
        self.time = 0

        if height is not None:
            self.jump_height = height
        if ground is not None:
            self.ground = ground
        if speed is not None:
            self.forward_speed = speed
        if self.rect.bottom > self.ground:
            self.rect.bottom = self.ground

        logger.debug('to jump')

    def to_roll(self, speed=None):
        self.status = self.ROLL
        self.roll_idx = 0
        self.time = 0
        if speed is not None:
            self.forward_speed = speed

        logger.debug('to roll')

    def to_wait(self):
        self.status = self.WAIT
        self.image = self.wait_img

    def pause(self):
        if self.status == self.PAUSE:
            return None
        self._prev_status = self.status
        self.status = self.PAUSE
        logger.info('pause -> %s', self._prev_status)

    def unpause(self):
        if self.status != self.PAUSE:
            return None
        self.status = self._prev_status
        logger.info('unpause -> %s', self.status)

    prev_speed = 0
    def stop_roll(self):
        if self.forward_speed != 0:
            self.prev_speed = self.forward_speed
            self.forward_speed = 0

    def resume_roll(self):
        if self.prev_speed != 0:
            self.forward_speed = self.prev_speed


if __name__ == '__main__':
    getlogger(logger, DEBUG, True)
    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    group = pygame.sprite.Group()
    role = Role()
    # role.to_run()
    # role.to_jump()
    role.to_roll()
    # role.to_wait()
    role.rect.bottom = 400
    role.ground = 400
    role.forward_speed = 0
    group.add(role)
    run = True
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # role.update(clock.tick(100))
        if role.update(clock.tick(cfg.tick)):
            # role.to_run()
            # role.to_jump()
            role.to_roll()
            # if role.status == role.JUMP:
            #     role.to_roll()
            # elif role.status == role.ROLL:
            #     role.to_wait()
            # else:
            #     role.to_run()

        screen.fill((255, 255, 255))
        group.draw(screen)
        pygame.display.flip()

    pygame.quit()
