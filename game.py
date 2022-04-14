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

    def play(self) -> None:
        while not self.done:

            self.done = self.process_events()

            self.run_logic()

            self.display_screen()

            self.game_configuration.clock.tick(GameSettings.FPS)

        pygame.quit()

    def process_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False

    def run_logic(self) -> None:
        keys = pygame.key.get_pressed()
        self.move_controller.move(
            keys,
            self.screen_handler.player_drawer,
            PlayerSettings.SPEED,
            obstacle_group=self.screen_handler.obstacle_group,
        )
        self.move_controller.move_bullet(
            keys,
            self.screen_handler.player_drawer,
            self.screen_handler.obstacle_group,
            self.screen_handler.destroyable_group
        )
        self.move_controller.move_bullet(
            keys,
            self.screen_handler.enemy_drawer,
            self.screen_handler.obstacle_group,
            self.screen_handler.destroyable_group
        )
        self.move_controller.move_enemy(self.screen_handler.enemy_drawer,
                                        self.screen_handler.obstacle_group)

    def display_screen(self) -> None:
        self.screen_handler.draw()
        self.screen_handler.update()
