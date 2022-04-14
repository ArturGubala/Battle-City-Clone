import pygame
from move_enums import MoveDirection
from random import choice

from settings import Colors, PlayerSettings, SpriteSettings, EnemySettings
from file_system_handler import FileSystemHandler


class ScreenHandler:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.player_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.destroyable_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.player_drawer = PlayerDrawer(pos=PlayerSettings.STARTING_POS,
                                          player_size=PlayerSettings.PLAYER_SIZE,
                                          player_group=[
                                              self.player_group, self.destroyable_group],
                                          bullet_group=self.bullet_group)

        self.enemy_drawer = EnemyDrawer(pos=EnemySettings.STARTING_POS,
                                        enemy_size=EnemySettings.ENEMY_SIZE,
                                        enemy_group=[
                                            self.enemy_group, self.destroyable_group],
                                        bullet_group=self.bullet_group,
                                        display_surface=self.display_surface)

        self.stage = StageDrawer()
        self.stage.create_map(self.obstacle_group, self.destroyable_group)

    def draw(self) -> None:
        self.display_surface.fill(Colors.BG)
        self.obstacle_group.draw(self.display_surface)
        self.player_group.draw(self.display_surface)
        self.enemy_group.draw(self.display_surface)
        self.bullet_group.draw(self.display_surface)

    def update(self) -> None:
        self.player_drawer.update()
        self.enemy_group.update()
        self.bullet_group.update()
        self.enemy_drawer.object_detector.update()
        self.enemy_drawer.update()
        pygame.display.update()


class PlayerDrawer(pygame.sprite.Sprite):
    def __init__(self, **player_info) -> None:
        super().__init__(player_info["player_group"])
        self.image = pygame.transform.scale(pygame.image.load(
            'Sprites/Player/player.png').convert_alpha(), player_info["player_size"])
        self.rect = self.image.get_rect(bottomright=(player_info["pos"]))
        self.bullet_group = player_info["bullet_group"]
        self.shot_bullets = []

        self.direction = pygame.math.Vector2()
        self.import_player_assets()
        self.status = MoveDirection.UP
        self.frame_index = 0
        self.animation_speed = 0.1

    def update(self) -> None:
        self.get_status()
        self.animate()

    def get_status(self) -> None:
        if self.direction.x == 0 and self.direction.y == 0:
            if not MoveDirection.IDLE in self.status:
                self.status = self.status + MoveDirection.IDLE

    def animate(self) -> None:
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image.set_colorkey(Colors.BLACK)

    def import_player_assets(self) -> None:
        character_path = 'Sprites/Player/'
        self.animations = {MoveDirection.UP: [], MoveDirection.DOWN: [], MoveDirection.LEFT: [], MoveDirection.RIGHT: [],
                           MoveDirection.UP_IDLE: [], MoveDirection.DOWN_IDLE: [], MoveDirection.LEFT_IDLE: [], MoveDirection.RIGHT_IDLE: []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = FileSystemHandler.import_folder(
                full_path)

    def shoot(self, bullet_group, pos):
        if not self.shot_bullets:
            self.shot_bullets.append(BulletDrawer(
                bullet_group, pos, self.status))


class ObstacleDrawer(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = pygame.transform.scale(surface, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.set_colorkey(Colors.BLACK)


class StageDrawer:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.layouts = {
            'border': FileSystemHandler.import_csv_layout('Stages/Stage_0/stage_0_border.csv'),
            'stage': FileSystemHandler.import_csv_layout('Stages/Stage_0/stage_0_stage.csv'),
            'target': FileSystemHandler.import_csv_layout('Stages/Stage_0/stage_0_target.csv')
        }
        self.graphics = {
            'obstacles': FileSystemHandler.import_folder('Sprites/Obstacles')
        }

    def create_map(self, obstacle_group, destroyable_group):
        for style, layout in self.layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    self.create_obstacle(
                        sprite_id=col, sprite_style=style, row_index=row_index, col_index=col_index, group=[obstacle_group, destroyable_group])

    def create_obstacle(self, **sprite_info) -> None:
        if sprite_info["sprite_id"] != '-1':
            x = sprite_info["col_index"] * SpriteSettings.SPRITESIZE
            y = sprite_info["row_index"] * SpriteSettings.SPRITESIZE
            if sprite_info["sprite_style"] == 'border':
                surf = self.graphics['obstacles'][int(
                    sprite_info["sprite_id"])]
                ObstacleDrawer((x, y), sprite_info["group"][0],
                               'border', surf)
            else:
                surf = self.graphics['obstacles'][int(
                    sprite_info["sprite_id"])]
                ObstacleDrawer((x, y), sprite_info["group"],
                               'border', surf)


class BulletDrawer(pygame.sprite.Sprite):
    def __init__(self, group, pos, direction) -> None:
        super().__init__(group)
        self.image = pygame.Surface((16, 16))
        self.image.fill("black")
        self.rect = self.image.get_rect(center=(pos))
        self.direction = direction


class EnemyDrawer(pygame.sprite.Sprite):
    def __init__(self, **enemy_info) -> None:
        super().__init__(enemy_info["enemy_group"])
        self.image = pygame.transform.scale(pygame.image.load(
            'Sprites/Player/player.png').convert_alpha(), enemy_info["enemy_size"])
        self.rect = self.image.get_rect(topleft=(enemy_info["pos"]))
        self.bullet_group = enemy_info["bullet_group"]
        self.shot_bullets = []
        self.object_detector = ObjectDetectorDrawer(
            self.rect, enemy_info["display_surface"])

        self.direction = pygame.math.Vector2(-1, 0)
        self.import_enemy_assets()
        self.status = ""
        self.frame_index = 0
        self.animation_speed = 0.1

        self.set_status()

    def set_status(self):
        if self.direction.y == -1:
            self.status = MoveDirection.UP
        elif self.direction.y == 1:
            self.status = MoveDirection.DOWN
        if self.direction.x == -1:
            self.status = MoveDirection.LEFT
        elif self.direction.x == 1:
            self.status = MoveDirection.RIGHT

    def animate(self) -> None:
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image.set_colorkey(Colors.BLACK)

    def import_enemy_assets(self) -> None:
        character_path = 'Sprites/Enemy/'
        self.animations = {MoveDirection.UP: [], MoveDirection.DOWN: [],
                           MoveDirection.LEFT: [], MoveDirection.RIGHT: []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = FileSystemHandler.import_folder(
                full_path)

    def shoot(self, bullet_group, pos):
        if not self.shot_bullets:
            self.shot_bullets.append(BulletDrawer(
                bullet_group, pos, self.status))

    def update(self):
        self.animate()
        self.set_status()


class ObjectDetectorDrawer():
    def __init__(self, enemy_rect, surface) -> None:
        self.detectors = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }
        self.enemy_rect = enemy_rect
        self.surface = surface
        self.add_detector()

    def add_detector(self):
        self.detectors["up"] = [
            pygame.draw.line(self.surface, pygame.Color('red'), self.enemy_rect.topleft,
                             (self.enemy_rect.topleft[0], self.enemy_rect.topleft[1] - 1)),
            pygame.draw.line(self.surface, pygame.Color(
                'red'), (self.enemy_rect.topright[0] - 1, self.enemy_rect.topright[1]), (self.enemy_rect.topright[0] - 1, self.enemy_rect.topright[1] - 1))
        ]

        self.detectors["down"] = [
            pygame.draw.line(self.surface, pygame.Color(
                'red'), (self.enemy_rect.bottomright[0] - 1, self.enemy_rect.bottomright[1]), (self.enemy_rect.bottomright[0] - 1, self.enemy_rect.bottomright[1] + 1)),
            pygame.draw.line(self.surface, pygame.Color(
                'red'), self.enemy_rect.bottomleft, (self.enemy_rect.bottomleft[0], self.enemy_rect.bottomleft[1] + 1))
        ]

        self.detectors["left"] = [
            pygame.draw.line(self.surface, pygame.Color(
                'red'), self.enemy_rect.topleft, (self.enemy_rect.topleft[0] - 1, self.enemy_rect.topleft[1])),
            pygame.draw.line(self.surface, pygame.Color(
                'red'), (self.enemy_rect.bottomleft[0], self.enemy_rect.bottomleft[1] - 1), (self.enemy_rect.bottomleft[0] - 1, self.enemy_rect.bottomleft[1] - 1))
        ]

        self.detectors["right"] = [
            pygame.draw.line(self.surface, pygame.Color(
                'red'), self.enemy_rect.topright, (self.enemy_rect.topright[0] + 1, self.enemy_rect.topright[1])),
            pygame.draw.line(self.surface, pygame.Color(
                'red'), (self.enemy_rect.bottomright[0], self.enemy_rect.bottomright[1] - 1), (self.enemy_rect.bottomright[0] + 1, self.enemy_rect.bottomright[1] - 1))
        ]

    def update(self):
        self.add_detector()
