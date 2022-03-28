import pygame

from settings import GameSettings


class MoveController:
    def __init__(self) -> None:

        self.movement = {
            pygame.K_UP: [self.__set_direction_y, -1, 0],
            pygame.K_DOWN: [self.__set_direction_y, 1, -180],
            pygame.K_RIGHT: [self.__set_direction_x, 1, -90],
            pygame.K_LEFT: [self.__set_direction_x, -1, -270]
        }
        self.movement_conditions = {
            pygame.K_UP: self.__can_move_up,
            pygame.K_DOWN: self.__can_move_down,
            pygame.K_RIGHT: self.__can_move_right,
            pygame.K_LEFT: self.__can_move_left,
        }

    def __set_direction_y(self, object, direction, angle) -> None:
        object.direction.y = direction
        object.direction.x = 0
        object.angle = angle

    def __set_direction_x(self, object, direction, angle) -> None:
        object.direction.x = direction
        object.direction.y = 0
        object.angle = angle

    def __can_move_up(self, object) -> bool:
        return object.rect.top > 0

    def __can_move_down(self, object) -> bool:
        return object.rect.bottom < GameSettings.WINDOW_HEIGHT

    def __can_move_right(self, object) -> bool:
        return object.rect.right < GameSettings.WINDOW_WIDTH

    def __can_move_left(self, object) -> bool:
        return object.rect.left > 0

    def move(self, pressed_keys, object, speed) -> None:
        for key, movment_condition in self.movement_conditions.items():
            if pressed_keys[key] and movment_condition(object):
                self.movement[key][0](object,
                                      self.movement[key][1],
                                      self.movement[key][2])
                object.rect.center += object.direction * speed
                break
