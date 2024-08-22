import pygame
from wordson.config import Config

__all__ = (
    'config', 'screen'
)

config = Config()
pygame.init()
screen = pygame.display.set_mode(config.screen)
