class MoveDirection:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    IDLE = "_idle"
    UP_IDLE = "up_idle"
    DOWN_IDLE = "down_idle"
    LEFT_IDLE = "left_idle"
    RIGHT_IDLE = "right_idle"
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class BulletState:
    TARGET_NOT_HIT = 0
    TARGET_HIT = 1
    WALL_HIT = 2
    WALL_NOT_HIT = 3
    NO_BULLET = 4
