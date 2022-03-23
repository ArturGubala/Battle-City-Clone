import pygame

from game_configuration import GameConfiguration
from player import Player
from settings import GameSettings, Colors


class Game:
    def __init__(self) -> None:
        self.game_configuration = GameConfiguration()
        self.game_over = False

        self.sprite_sheet_image = pygame.image.load(
            GameSettings.SPRITE_SHEET).convert_alpha()

        self.all_sprites_list = pygame.sprite.Group()

        player = Player(sprite_sheet=self.sprite_sheet_image,
                        width=16, height=15, scale=2)
        self.all_sprites_list.add(player)

    def play(self):
        done = False
        while not done:

            done = self.process_events()

            self.run_logic()

            self.display_frame(self.game_configuration.screen)

            self.game_configuration.clock.tick(GameSettings.FPS)

        pygame.quit()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False

    def run_logic(self):
        pass

    def display_frame(self, screen):
        screen.fill(Colors.BG)

        if self.game_over:
            pass

        if not self.game_over:
            self.all_sprites_list.draw(screen)

        pygame.display.flip()
