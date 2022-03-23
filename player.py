from turtle import speed
import pygame

from settings import Colors, GameSettings


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, height, width, scale=1) -> None:
        super().__init__()
        self.player_width = width
        self.player_height = height
        self.scale = scale
        self.angle = 0
        self.pos_x = GameSettings.WINDOW_WIDTH // 2 - self.player_width // 2
        self.pos_y = GameSettings.WINDOW_HEIGHT // 2 - self.player_height // 2
        self.speed = 3
        self.sheet = sprite_sheet

        self.draw_player()

    def move_player(self, move_x, move_y) -> None:
        self.pos_x += 1 * move_x * self.speed
        self.pos_y += 1 * move_y * self.speed

    def draw_player(self):
        self.image = pygame.Surface((self.player_width, self.player_height))
        self.image.blit(self.sheet, (0, 0),
                        (0, 0, self.player_width, self.player_height))
        self.image = pygame.transform.scale(
            self.image, (self.player_width * self.scale, self.player_height * self.scale))
        self.image = pygame.transform.rotate(
            self.image, self.angle)
        self.image.set_colorkey(Colors.BLACK)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
