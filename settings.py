from dataclasses import dataclass


import os.path


@dataclass
class GameSettings:
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    FPS = 60
    CAPTION = "Battle City Clone"
    SPRITE_SHEET = os.path.join(
        "Sprites", "NES - Battle City JPN - General Sprites.png")


@dataclass
class Colors:
    BLACK = (0, 0, 1)
    BG = (50, 50, 50)


@dataclass
class PlayerSettings:
    PLAYER_WIDTH = 16
    PLAYER_HEIGHT = 15
    SCALE = 3
    STARTING_POS_X = GameSettings.WINDOW_WIDTH // 2 - PLAYER_WIDTH // 2
    STARTING_POS_Y = GameSettings.WINDOW_HEIGHT // 2 - PLAYER_HEIGHT // 2
    SPEED = 3
    ANGLE = 0
