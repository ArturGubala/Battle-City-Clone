from abc import ABC
import pygame

from settings import Colors, PlayerSettings
import support


class ScreenHandler:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.all_sprites_list = pygame.sprite.Group()

        self.player_drawer = PlayerDrawer(pos=PlayerSettings.STARTING_POS,
                                          player_size=PlayerSettings.PLAYER_SIZE)
        self.add_to_screen(self.player_drawer)

    def draw(self) -> None:
        self.display_surface.fill(Colors.BG)
        self.all_sprites_list.draw(self.display_surface)
        pygame.display.flip()

    def add_to_screen(self, *sprites) -> None:
        for sprite in sprites:
            self.all_sprites_list.add(sprite)

    def update_player_sprite(self) -> None:
        self.player_drawer.update()


class Drawer(ABC):
    pass


class PlayerDrawer(pygame.sprite.Sprite):
    def __init__(self, **player_info) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            'Sprites/Player/player.png').convert_alpha(), player_info["player_size"])
        self.direction = pygame.math.Vector2()
        self.rect = self.image.get_rect(center=(player_info["pos"]))

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
            self.animations[animation] = support.import_folder(full_path)


class ScreenDrawer:
    pass


class BulletDrawer:
    pass


class EnemyDrawer:
    pass
