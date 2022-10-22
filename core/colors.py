from enum import Enum


class ColorType(Enum):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 176, 80)
    BLUE = (0, 176, 240)
    NAVY = (0, 32, 96)
    WHITE = (255, 255, 255)
    PURPLE = (112, 48, 160)
    BROWN = (191, 144, 0)
    ORANGE = (237, 125, 49)


COLORS = [ColorType.BLACK, ColorType.NAVY, ColorType.GREEN, ColorType.ORANGE,
          ColorType.BLUE, ColorType.PURPLE, ColorType.BROWN]
