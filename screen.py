from abc import ABC
import pygame

from settings import GameSettings, Colors, PlayerSettings


class ScreenHandler:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(
            (GameSettings.WINDOW_WIDTH, GameSettings.WINDOW_HEIGHT))
        self.all_sprites_list = pygame.sprite.Group()
        self.sprite_sheet_image = pygame.image.load(
            GameSettings.SPRITE_SHEET).convert()

        self.player_drawer = PlayerDrawer(self.sprite_sheet_image,
                                          player_width=PlayerSettings.PLAYER_WIDTH,
                                          player_height=PlayerSettings.PLAYER_HEIGHT,
                                          scale=PlayerSettings.SCALE)
        self.add_to_screen(self.player_drawer)

    def draw(self):
        self.screen.fill(Colors.BG)
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()

    def add_to_screen(self, *sprites):
        for sprite in sprites:
            self.all_sprites_list.add(sprite)

    def update_player_sprite(self, actual_player_cords):
        self.player_drawer.create_sprite(actual_player_cords["actual_pos_x"],
                                         actual_player_cords["actual_pos_y"],
                                         actual_player_cords["angle"])


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

    def create_sprite(self, pos_x, pos_y, angle) -> None:
        self.image = pygame.transform.rotate(
            self.pattern, angle)
        self.image.set_colorkey(Colors.BLACK)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))


class ScreenDrawer:
    pass


class BulletDrawer:
    pass


class EnemyDrawer:
    pass
