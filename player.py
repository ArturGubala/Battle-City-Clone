import pygame

from settings import GameSettings, PlayerSettings


class Player():
    def __init__(self) -> None:
        self.pos_x = PlayerSettings.STARTING_POS_X
        self.pos_y = PlayerSettings.STARTING_POS_Y
        self.angle = PlayerSettings.ANGLE
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

    def __move_player(self, move_x, move_y, angle) -> None:
        self.pos_x += 1 * move_x * PlayerSettings.SPEED
        self.pos_y += 1 * move_y * PlayerSettings.SPEED
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
        return (self.pos_y - (PlayerSettings.PLAYER_HEIGHT // 2) * PlayerSettings.SCALE) + PlayerSettings.SPEED > 0

    def __can_move_down(self) -> bool:
        return (self.pos_y + (PlayerSettings.PLAYER_HEIGHT // 2) * PlayerSettings.SCALE) + PlayerSettings.SPEED < GameSettings.WINDOW_HEIGHT

    def __can_move_right(self) -> bool:
        return (self.pos_x + (PlayerSettings.PLAYER_HEIGHT // 2) * PlayerSettings.SCALE) + PlayerSettings.SPEED < GameSettings.WINDOW_WIDTH

    def __can_move_left(self) -> bool:
        return (self.pos_x - (PlayerSettings.PLAYER_HEIGHT // 2) * PlayerSettings.SCALE) + PlayerSettings.SPEED > 0

    def get_actual_position(self):
        return {
            "actual_pos_x": self.pos_x,
            "actual_pos_y": self.pos_y,
            "angle": self.angle
        }
