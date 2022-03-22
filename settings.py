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
