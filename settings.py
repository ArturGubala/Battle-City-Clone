from dataclasses import dataclass


@dataclass
class GameSettings:
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 960
    FPS = 60
    CAPTION = "Battle City Clone"


@dataclass
class Colors:
    BLACK = (0, 0, 1)
    BG = (50, 50, 50)


@dataclass
class PlayerSettings:
    PLAYER_SIZE = (64, 64)
    STARTING_POS = (448, 896)
    SPEED = 6
    ASSIST_LEVEL = 15
    STARTING_SPRITE_PATH = "Sprites/Player/player.png"
    ANIMATION_SPRITES_PATH = "Sprites/Player/"


@dataclass
class SpriteSettings:
    SPRITESIZE = 64


@dataclass
class BulletSettings:
    SPEED = 15


@dataclass
class EnemySettings:
    ENEMY_SIZE = (64, 64)
    STARTING_POS = (960, 64)
    SPEED = 6
    ASSIST_LEVEL = 15
    STARTING_SPRITE_PATH = "Sprites/Player/player.png"
    ANIMATION_SPRITES_PATH = "Sprites/Enemy/"


@dataclass
class StageSettings:
    BORDER_LAYOUT = "Stages/Stage_0/stage_0_border.csv"
    STAGE_LAYOUT = "Stages/Stage_0/stage_0_stage.csv"
    TARGET_LAYOUT = "Stages/Stage_0/stage_0_target.csv"
    STAGE_SPRITES = "Sprites/Obstacles"
