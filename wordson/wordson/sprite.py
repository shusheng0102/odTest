import pygame


class Sprite(pygame.sprite.Sprite):

    def draw(self, surface):
        return surface.blit(self.image, self.rect)

    def handle(self, event):
        pass

    def sprites(self):
        return [self]


class Group(pygame.sprite.Group):

    def extend(self, *group):
        for each_group in group:
            for sprite in each_group.sprites():
                self.add(sprite)

    def handle(self, event):
        for sprite in self.sprites():
            if sprite.handle(event):
                return True

    def kill(self):
        for sprite in self.sprites():
            sprite.kill()

class OrderedUpdates(pygame.sprite.OrderedUpdates):

    def extend(self, *group):
        for each_group in group:
            for sprite in each_group.sprites():
                self.add(sprite)

    def handle(self, event):
        for sprite in self.sprites():
            if sprite.handle(event):
                return True

    def kill(self):
        for sprite in self.sprites():
            sprite.kill()
