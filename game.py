import pygame

from game_configuration import GameConfiguration
from player import Player
from settings import GameSettings
from screen import ScreenHandler


class Game:
    def __init__(self) -> None:
        self.game_configuration = GameConfiguration()
        self.game_over = False
        self.done = False
        self.screen_handler = ScreenHandler()
        self.player = Player()

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
        for key, movment_condition in self.player.movement_conditions.items():
            if keys[key] and movment_condition():
                self.player.movement[key]()
                break

        self.screen_handler.update_player_sprite(
            self.player.get_actual_position())
        self.screen_handler.draw()

    def display_screen(self):
        self.screen_handler.draw()
