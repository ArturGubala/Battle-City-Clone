import pygame

from settings import Colors, GameSettings


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, height, width, scale=1):
        super().__init__()
        self.player_width = width
        self.player_height = height
        self.sheet = sprite_sheet
        self.image = pygame.Surface((self.player_width, self.player_height))
        self.image.blit(self.sheet, (0, 0),
                        (0, 0, self.player_width, self.player_height))
        self.image = pygame.transform.scale(
            self.image, (width * scale, height * scale))
        self.image.set_colorkey(Colors.BLACK)

        self.rect = self.image.get_rect(
            center=(GameSettings.WINDOW_WIDTH // 2 - self.player_width // 2, GameSettings.WINDOW_HEIGHT // 2 - self.player_height // 2))
