import pygame
from random import randint, choice

from move_enums import MoveDirection
from screen import PlayerDrawer
from settings import EnemySettings, PlayerSettings, BulletSettings


class MoveController:
    def __init__(self) -> None:

        self.movement = {
            pygame.K_UP: [self.__set_direction_y, -1, MoveDirection.UP],
            pygame.K_DOWN: [self.__set_direction_y, 1, MoveDirection.DOWN],
            pygame.K_RIGHT: [self.__set_direction_x, 1, MoveDirection.RIGHT],
            pygame.K_LEFT: [self.__set_direction_x, -1, MoveDirection.LEFT]
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
                return
            object.direction.x = 0
            object.direction.y = 0

    def collision(self, direction, object, group):
        if direction == 'horizontal':
            for sprite in group:
                if sprite.rect.colliderect(object.rect):
                    if object.direction.x > 0:  # moving right
                        object.rect.right = sprite.rect.left
                        self.__assist_while_turning("horizontal",
                                                    object,
                                                    sprite)
                    if object.direction.x < 0:  # moving left
                        object.rect.left = sprite.rect.right
                        self.__assist_while_turning("horizontal",
                                                    object,
                                                    sprite)

        if direction == 'vertical':
            for sprite in group:
                if sprite.rect.colliderect(object.rect):
                    if object.direction.y > 0:  # moving down
                        object.rect.bottom = sprite.rect.top
                        self.__assist_while_turning("vertical", object, sprite)
                    if object.direction.y < 0:  # moving up
                        object.rect.top = sprite.rect.bottom
                        self.__assist_while_turning("vertical", object, sprite)

    def __assist_while_turning(self, direction, turning_object, obstacle):
        if direction == 'vertical':
            if (obstacle.rect.right - turning_object.rect.left) < PlayerSettings.ASSIST_LEVEL:
                turning_object.rect.left = obstacle.rect.right
            if (turning_object.rect.right - obstacle.rect.left) < PlayerSettings.ASSIST_LEVEL:
                turning_object.rect.right = obstacle.rect.left

        if direction == 'horizontal':
            if (obstacle.rect.bottom - turning_object.rect.top) < PlayerSettings.ASSIST_LEVEL:
                turning_object.rect.top = obstacle.rect.bottom
            if (turning_object.rect.bottom - obstacle.rect.top) < PlayerSettings.ASSIST_LEVEL:
                turning_object.rect.bottom = obstacle.rect.top

    def move_bullet(self, keys, object, group, destroyable_group):
        if isinstance(object, PlayerDrawer):
            if keys[pygame.K_SPACE]:
                object.shoot(object.bullet_group, object.rect.center)
        else:
            object.shoot(object.bullet_group, object.rect.center)
        if object.shot_bullets:
            if MoveDirection.UP in object.shot_bullets[0].direction:
                object.shot_bullets[0].rect.y -= BulletSettings.SPEED
            if MoveDirection.DOWN in object.shot_bullets[0].direction:
                object.shot_bullets[0].rect.y += BulletSettings.SPEED
            if MoveDirection.LEFT in object.shot_bullets[0].direction:
                object.shot_bullets[0].rect.x -= BulletSettings.SPEED
            if MoveDirection.RIGHT in object.shot_bullets[0].direction:
                object.shot_bullets[0].rect.x += BulletSettings.SPEED
            self.bullet_collision(
                object, group, destroyable_group)

    def bullet_collision(self, object, collision_group, destroyable_group):
        for collision_object in collision_group:
            if collision_object.rect.colliderect(object.shot_bullets[0].rect):
                if collision_object in destroyable_group:
                    collision_object.kill()
                object.shot_bullets[0].kill()
                object.shot_bullets.clear()
                return

    def randomize_direction(self, enemy, direction):
        if direction == MoveDirection.UP:
            enemy.direction = pygame.math.Vector2(0, -1)
        elif direction == MoveDirection.DOWN:
            enemy.direction = pygame.math.Vector2(0, 1)
        elif direction == MoveDirection.LEFT:
            enemy.direction = pygame.math.Vector2(-1, 0)
        elif direction == MoveDirection.RIGHT:
            enemy.direction = pygame.math.Vector2(1, 0)

    def collision_enemy(self, group, enemy, side=""):

        for sprite in group:
            if sprite.rect.colliderect(enemy.rect):
                if (enemy.direction.x > 0) or (side == MoveDirection.RIGHT and enemy.rect.right - sprite.rect.left > 0):  # moving right
                    enemy.rect.right = sprite.rect.left
                elif (enemy.direction.x < 0) or (side == MoveDirection.LEFT and enemy.rect.left - sprite.rect.right < 0):  # moving left
                    enemy.rect.left = sprite.rect.right
                elif (enemy.direction.y > 0) or (side == MoveDirection.DOWN and enemy.rect.bottom - sprite.rect.top > 0):  # moving down
                    enemy.rect.bottom = sprite.rect.top
                elif (enemy.direction.y < 0) or (side == MoveDirection.UP and enemy.rect.top - sprite.rect.bottom < 0):  # moving up
                    enemy.rect.top = sprite.rect.bottom

    def move_enemy(self, enemy, obstacles):
        directions = [MoveDirection.UP, MoveDirection.DOWN,
                      MoveDirection.RIGHT, MoveDirection.LEFT]
        for obs in obstacles:
            for side, detector in enemy.object_detector.detectors.items():
                if (detector[0].colliderect(obs.rect) and detector[1].colliderect(obs.rect)):
                    self.collision_enemy(
                        obstacles, enemy, side)
                    if side in directions:
                        directions.remove(side)

        if enemy.status == MoveDirection.UP:
            if MoveDirection.DOWN in directions:
                directions.remove(MoveDirection.DOWN)
        elif enemy.status == MoveDirection.DOWN:
            if MoveDirection.UP in directions:
                directions.remove(MoveDirection.UP)
        elif enemy.status == MoveDirection.RIGHT:
            if MoveDirection.LEFT in directions:
                directions.remove(MoveDirection.LEFT)
        elif enemy.status == MoveDirection.LEFT:
            if MoveDirection.RIGHT in directions:
                directions.remove(MoveDirection.RIGHT)
        if len(directions) < 3:
            enemy.direction = pygame.math.Vector2(0, 0)
            self.randomize_direction(enemy, choice(directions))

        enemy.rect.x += enemy.direction.x * EnemySettings.SPEED
        enemy.rect.y += enemy.direction.y * EnemySettings.SPEED
        enemy.set_status()
