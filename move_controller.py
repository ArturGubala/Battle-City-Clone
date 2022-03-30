import pygame


class MoveController:
    def __init__(self) -> None:

        self.movement = {
            pygame.K_UP: [self.__set_direction_y, -1, 'up'],
            pygame.K_DOWN: [self.__set_direction_y, 1, 'down'],
            pygame.K_RIGHT: [self.__set_direction_x, 1, 'right'],
            pygame.K_LEFT: [self.__set_direction_x, -1, 'left']
        }

    def __set_direction_y(self, object, direction, status) -> None:
        object.direction.y = direction
        object.direction.x = 0
        object.status = status

    def __set_direction_x(self, object, direction, status) -> None:
        object.direction.x = direction
        object.direction.y = 0
        object.status = status

    def move(self, pressed_keys, object, speed, **groups) -> None:
        for key, move in self.movement.items():
            if pressed_keys[key]:
                move[0](object, move[1], move[2])
                object.rect.x += object.direction.x * speed
                self.collision('horizontal', object, groups["obstacle_group"])
                object.rect.y += object.direction.y * speed
                self.collision('vertical', object, groups["obstacle_group"])
                break
            else:
                object.direction.x = 0
                object.direction.y = 0

    def collision(self, direction, object, group):
        if direction == 'horizontal':
            for sprite in group:
                if sprite.rect.colliderect(object.rect):
                    if object.direction.x > 0:  # moving right
                        object.rect.right = sprite.rect.left
                    if object.direction.x < 0:  # moving left
                        object.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in group:
                if sprite.rect.colliderect(object.rect):
                    if object.direction.y > 0:  # moving down
                        object.rect.bottom = sprite.rect.top
                    if object.direction.y < 0:  # moving up
                        object.rect.top = sprite.rect.bottom
