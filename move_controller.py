import pygame
from random import choice

from move_enums import MoveDirection, BulletState
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

    def __set_direction_y(self, character, direction, status) -> None:
        character.direction.y = direction
        character.direction.x = 0
        character.status = status

    def __set_direction_x(self, character, direction, status) -> None:
        character.direction.x = direction
        character.direction.y = 0
        character.status = status

    def move(self, pressed_keys, character, speed, **groups) -> None:
        for key, move in self.movement.items():
            if pressed_keys[key]:
                move[0](character, move[1], move[2])
                character.rect.x += character.direction.x * speed
                self.collision(MoveDirection.HORIZONTAL,
                               character, groups["obstacle_group"])
                character.rect.y += character.direction.y * speed
                self.collision(MoveDirection.VERTICAL, character,
                               groups["obstacle_group"])
                return
            character.direction.x = 0
            character.direction.y = 0

    def collision(self, direction, character, group):
        if direction == MoveDirection.HORIZONTAL:
            for sprite in group:
                if sprite.rect.colliderect(character.rect):
                    if character.direction.x > 0:  # moving right
                        character.rect.right = sprite.rect.left
                        self.__assist_while_turning(MoveDirection.HORIZONTAL,
                                                    character,
                                                    sprite)
                    if character.direction.x < 0:  # moving left
                        character.rect.left = sprite.rect.right
                        self.__assist_while_turning(MoveDirection.HORIZONTAL,
                                                    character,
                                                    sprite)

        if direction == MoveDirection.VERTICAL:
            for sprite in group:
                if sprite.rect.colliderect(character.rect):
                    if character.direction.y > 0:  # moving down
                        character.rect.bottom = sprite.rect.top
                        self.__assist_while_turning(
                            MoveDirection.VERTICAL, character, sprite)
                    if character.direction.y < 0:  # moving up
                        character.rect.top = sprite.rect.bottom
                        self.__assist_while_turning(
                            MoveDirection.VERTICAL, character, sprite)

    def __assist_while_turning(self, direction, character, obstacle):
        if direction == MoveDirection.VERTICAL:
            if (obstacle.rect.right - character.rect.left) < PlayerSettings.ASSIST_LEVEL:
                character.rect.left = obstacle.rect.right
            if (character.rect.right - obstacle.rect.left) < PlayerSettings.ASSIST_LEVEL:
                character.rect.right = obstacle.rect.left

        if direction == MoveDirection.HORIZONTAL:
            if (obstacle.rect.bottom - character.rect.top) < PlayerSettings.ASSIST_LEVEL:
                character.rect.top = obstacle.rect.bottom
            if (character.rect.bottom - obstacle.rect.top) < PlayerSettings.ASSIST_LEVEL:
                character.rect.bottom = obstacle.rect.top

    def move_bullet(self, keys, shooter, group, destroyable_group, oponent, sh):
        if isinstance(shooter, PlayerDrawer):
            if keys[pygame.K_SPACE]:
                shooter.shoot(shooter.bullet_group, shooter.rect.center)
        else:
            shooter.shoot(shooter.bullet_group, shooter.rect.center)
        if shooter.shot_bullets:
            if MoveDirection.UP in shooter.shot_bullets[0].direction:
                shooter.shot_bullets[0].rect.y -= BulletSettings.SPEED
            if MoveDirection.DOWN in shooter.shot_bullets[0].direction:
                shooter.shot_bullets[0].rect.y += BulletSettings.SPEED
            if MoveDirection.LEFT in shooter.shot_bullets[0].direction:
                shooter.shot_bullets[0].rect.x -= BulletSettings.SPEED
            if MoveDirection.RIGHT in shooter.shot_bullets[0].direction:
                shooter.shot_bullets[0].rect.x += BulletSettings.SPEED
            wall_state = self.bullet_collision_wall(
                shooter, group, destroyable_group)
            if oponent is not None and wall_state == BulletState.WALL_NOT_HIT:
                state = self.bullet_collision_enemy(
                    shooter, oponent, sh)
                return state
            return wall_state
        return BulletState.NO_BULLET

    def bullet_collision_wall(self, object, collision_group, destroyable_group):
        for collision_object in collision_group:
            if collision_object.rect.colliderect(object.shot_bullets[0].rect):
                if collision_object in destroyable_group:
                    collision_object.kill()
                object.shot_bullets[0].kill()
                object.shot_bullets.clear()
                return BulletState.WALL_HIT
        return BulletState.WALL_NOT_HIT

    def bullet_collision_enemy(self, shooter, oponent, sh):
        if oponent.rect.colliderect(shooter.shot_bullets[0].rect):
            shooter.shot_bullets[0].image.fill
            shooter.shot_bullets[0].image.set_alpha(255)
            shooter.shot_bullets[0].kill()
            shooter.shot_bullets.clear()
            oponent.kill()
            return BulletState.TARGET_HIT

    def set_new_enemy_direction(self, enemy, direction):
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
            self.set_new_enemy_direction(enemy, choice(directions))

        enemy.rect.x += enemy.direction.x * EnemySettings.SPEED
        enemy.rect.y += enemy.direction.y * EnemySettings.SPEED
        enemy.set_status()
