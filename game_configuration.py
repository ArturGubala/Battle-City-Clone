import pygame

from settings import GameSettings


class GameConfiguration:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(GameSettings.CAPTION)
        self.clock = pygame.time.Clock()
