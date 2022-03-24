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
        self.movement = {
            pygame.K_UP: self.__move_up,
            pygame.K_DOWN: self.__move_down,
            pygame.K_RIGHT: self.__move_right,
            pygame.K_LEFT: self.__move_left
        }
        self.movement_conditions = {
            pygame.K_UP: self.__can_move_up,
            pygame.K_DOWN: self.__can_move_down,
            pygame.K_RIGHT: self.__can_move_right,
            pygame.K_LEFT: self.__can_move_left,
        }

    def draw_player(self) -> None:
        self.image = pygame.Surface((self.player_width, self.player_height))
        self.image.blit(self.sheet, (0, 0),
                        (0, 0, self.player_width, self.player_height))
        self.image = pygame.transform.scale(
            self.image, (self.player_width * self.scale, self.player_height * self.scale))
        self.image = pygame.transform.rotate(
            self.image, self.angle)
        self.image.set_colorkey(Colors.BLACK)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def __move_player(self, move_x, move_y, angle) -> None:
        self.pos_x += 1 * move_x * self.speed
        self.pos_y += 1 * move_y * self.speed
        self.angle = angle

    def __move_up(self) -> None:
        self.__move_player(0, -1, 0)

    def __move_down(self) -> None:
        self.__move_player(0, 1, -180)

    def __move_right(self) -> None:
        self.__move_player(1, 0, -90)

    def __move_left(self) -> None:
        self.__move_player(-1, 0, -270)

    def __can_move_up(self) -> bool:
        return (self.pos_y - (self.player_height // 2) * self.scale) + self.speed > 0

    def __can_move_down(self) -> bool:
        return (self.pos_y + (self.player_height // 2) * self.scale) + self.speed < GameSettings.WINDOW_HEIGHT

    def __can_move_right(self) -> bool:
        return (self.pos_x + (self.player_height // 2) * self.scale) + self.speed < GameSettings.WINDOW_WIDTH

    def __can_move_left(self) -> bool:
        return (self.pos_x - (self.player_height // 2) * self.scale) + self.speed > 0
