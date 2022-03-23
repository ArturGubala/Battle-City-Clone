import pygame

from settings import GameSettings


class GameConfiguration:
    def __init__(self) -> None:
        pygame.init()
        self.size = (GameSettings.WINDOW_WIDTH, GameSettings.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(GameSettings.CAPTION)
        self.clock = pygame.time.Clock()
