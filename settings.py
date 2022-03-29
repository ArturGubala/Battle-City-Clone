from dataclasses import dataclass

import os.path


@dataclass
class GameSettings:
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 960
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
    PLAYER_SIZE = (64, 64)
    STARTING_POS = (GameSettings.WINDOW_WIDTH // 2 - PLAYER_SIZE[0] // 2,
                    GameSettings.WINDOW_HEIGHT // 2 - PLAYER_SIZE[1] // 2)
    SPEED = 6
