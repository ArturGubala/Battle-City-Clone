import pygame

#from player import Player
from settings import GameSettings, PlayerSettings


class MoveController:
    def __init__(self) -> None:

        self.player_movement = {
            pygame.K_UP: self.__move_player_up,
            pygame.K_DOWN: self.__move_player_down,
            pygame.K_RIGHT: self.__move_player_right,
            pygame.K_LEFT: self.__move_player_left
        }
        self.movement_conditions = {
            pygame.K_UP: self.__can_move_up,
            pygame.K_DOWN: self.__can_move_down,
            pygame.K_RIGHT: self.__can_move_right,
            pygame.K_LEFT: self.__can_move_left,
        }

    def __move_player_up(self, object) -> None:
        object.pos_x += 1 * 0 * PlayerSettings.SPEED
        object.pos_y += 1 * (-1) * PlayerSettings.SPEED
        object.angle = 0

    def __move_player_down(self, object) -> None:
        object.pos_x += 1 * 0 * PlayerSettings.SPEED
        object.pos_y += 1 * (1) * PlayerSettings.SPEED
        object.angle = -180

    def __move_player_right(self, object) -> None:
        object.pos_x += 1 * 1 * PlayerSettings.SPEED
        object.pos_y += 1 * (0) * PlayerSettings.SPEED
        object.angle = -90

    def __move_player_left(self, object) -> None:
        object.pos_x += 1 * (-1) * PlayerSettings.SPEED
        object.pos_y += 1 * (0) * PlayerSettings.SPEED
        object.angle = -270

    def __can_move_up(self, object) -> bool:
        return (object.pos_y - (PlayerSettings.PLAYER_HEIGHT // 2) * PlayerSettings.SCALE) + PlayerSettings.SPEED > 0

    def __can_move_down(self, object) -> bool:
        return (object.pos_y + (PlayerSettings.PLAYER_HEIGHT // 2) * PlayerSettings.SCALE) + PlayerSettings.SPEED < GameSettings.WINDOW_HEIGHT

    def __can_move_right(self, object) -> bool:
        return (object.pos_x + (PlayerSettings.PLAYER_HEIGHT // 2) * PlayerSettings.SCALE) + PlayerSettings.SPEED < GameSettings.WINDOW_WIDTH

    def __can_move_left(self, object) -> bool:
        return (object.pos_x - (PlayerSettings.PLAYER_HEIGHT // 2) * PlayerSettings.SCALE) + PlayerSettings.SPEED > 0

    def move_player(self, pressed_keys, object) -> None:
        for key, movment_condition in self.movement_conditions.items():
            if pressed_keys[key] and movment_condition(object):
                self.player_movement[key](object)
                break
