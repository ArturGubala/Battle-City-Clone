from abc import ABC
import pygame

from settings import GameSettings, Colors, PlayerSettings


class ScreenHandler:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.all_sprites_list = pygame.sprite.Group()
        self.sprite_sheet_image = pygame.image.load(
            GameSettings.SPRITE_SHEET).convert()

        self.player_drawer = PlayerDrawer(self.sprite_sheet_image,
                                          pos=PlayerSettings.STARTING_POS,
                                          player_width=PlayerSettings.PLAYER_WIDTH,
                                          player_height=PlayerSettings.PLAYER_HEIGHT,
                                          scale=PlayerSettings.SCALE)
        self.add_to_screen(self.player_drawer)

    def draw(self):
        self.display_surface.fill(Colors.BG)
        self.all_sprites_list.draw(self.display_surface)
        pygame.display.flip()

    def add_to_screen(self, *sprites):
        for sprite in sprites:
            self.all_sprites_list.add(sprite)

    def update_player_sprite(self):
        self.player_drawer.create_sprite()


class Drawer(ABC):
    pass


class PlayerDrawer(pygame.sprite.Sprite):
    def __init__(self, sheet, **player_info) -> None:
        super().__init__()
        self.pattern = pygame.Surface(
            (player_info["player_width"], player_info["player_height"]))
        self.pattern.blit(sheet, (0, 0),
                          (0, 0, player_info["player_width"], player_info["player_height"]))
        self.pattern = pygame.transform.scale(
            self.pattern, (player_info["player_width"] * player_info["scale"], player_info["player_height"] * player_info["scale"],))
        self.pattern.set_colorkey(Colors.BLACK)
        self.direction = pygame.math.Vector2()
        self.angle = PlayerSettings.ANGLE
        self.rect = self.pattern.get_rect(center=(player_info["pos"]))

    def create_sprite(self) -> None:
        self.image = pygame.transform.rotate(
            self.pattern, self.angle)


class ScreenDrawer:
    pass


class BulletDrawer:
    pass


class EnemyDrawer:
    pass
