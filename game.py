import pygame

from game_configuration import GameConfiguration
from settings import GameSettings, PlayerSettings
from screen import ScreenHandler
from move_controller import MoveController


class Game:
    def __init__(self) -> None:
        self.game_configuration = GameConfiguration()
        self.game_over = False
        self.done = False
        self.screen_handler = ScreenHandler()
        self.move_controller = MoveController()

    def play(self):
        while not self.done:

            self.done = self.process_events()

            self.run_logic()

            self.display_screen()

            self.game_configuration.clock.tick(GameSettings.FPS)

        pygame.quit()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False

    def run_logic(self):
        keys = pygame.key.get_pressed()
        self.move_controller.move(keys,
                                  self.screen_handler.player_drawer,
                                  PlayerSettings.SPEED)

        self.screen_handler.update_player_sprite()
        self.screen_handler.draw()

    def display_screen(self):
        self.screen_handler.draw()
