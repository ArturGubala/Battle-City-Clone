from abc import ABC
import pygame


from settings import Colors, PlayerSettings, SpriteSettings
from file_system_handler import FileSystemHandler


class ScreenHandler:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.player_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()

        self.player_drawer = PlayerDrawer(pos=PlayerSettings.STARTING_POS,
                                          player_size=PlayerSettings.PLAYER_SIZE,
                                          group=self.player_group)

        self.stage = StageDrawer()
        self.stage.create_map(self.obstacle_group)

    def draw(self) -> None:
        self.display_surface.fill(Colors.BG)
        self.obstacle_group.draw(self.display_surface)
        self.player_group.draw(self.display_surface)

    def update(self) -> None:
        self.player_drawer.update()
        pygame.display.update()


class Drawer(ABC):
    pass


class PlayerDrawer(pygame.sprite.Sprite):
    def __init__(self, **player_info) -> None:
        super().__init__(player_info["group"])
        self.image = pygame.transform.scale(pygame.image.load(
            'Sprites/Player/player.png').convert_alpha(), player_info["player_size"])
        self.direction = pygame.math.Vector2()
        self.rect = self.image.get_rect(bottomright=(player_info["pos"]))

        # graphics setup
        self.import_player_assets()
        self.status = 'up'
        self.frame_index = 0
        self.animation_speed = 0.1

    def update(self) -> None:
        self.get_status()
        self.animate()

    def get_status(self) -> None:
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'

    def animate(self) -> None:
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image.set_colorkey(Colors.BLACK)

    def import_player_assets(self) -> None:
        character_path = 'Sprites/Player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = FileSystemHandler.import_folder(
                full_path)


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

    def create_map(self, group):
        layouts = {
            'obstacles': FileSystemHandler.import_csv_layout('Stages/Stage_0/stage_0.csv')
        }
        graphics = {
            'obstacles': FileSystemHandler.import_folder('Sprites/Obstacles')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * SpriteSettings.SPRITESIZE
                        y = row_index * SpriteSettings.SPRITESIZE
                        if style == 'obstacles':
                            surf = graphics['obstacles'][int(col)]
                            ObstacleDrawer((x, y), group,
                                           'obstacles', surf)


class BulletDrawer:
    pass


class EnemyDrawer:
    pass
