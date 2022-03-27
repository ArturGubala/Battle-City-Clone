import pygame

from settings import GameSettings


class GameConfiguration:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (GameSettings.WINDOW_WIDTH, GameSettings.WINDOW_HEIGHT))
        pygame.display.set_caption(GameSettings.CAPTION)
        self.clock = pygame.time.Clock()
