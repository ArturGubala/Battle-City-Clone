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
