from typing import Dict
from settings import PlayerSettings


class Player():
    def __init__(self) -> None:
        self.pos_x = PlayerSettings.STARTING_POS_X
        self.pos_y = PlayerSettings.STARTING_POS_Y
        self.angle = PlayerSettings.ANGLE

    def get_actual_position(self) -> dict:
        return {
            "actual_pos_x": self.pos_x,
            "actual_pos_y": self.pos_y,
            "angle": self.angle
        }
