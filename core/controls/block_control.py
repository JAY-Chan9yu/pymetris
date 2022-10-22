import random
from enum import Enum
from typing import Optional

from core.colors import COLORS
from utils.blocks import get_next_block


class BlockType(int, Enum):
    IMAGE = 0
    COLOR = 1


class BlockDirection(int, Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


BLOCK_LIST = [BlockDirection.UP, BlockDirection.RIGHT, BlockDirection.DOWN, BlockDirection.LEFT]
DEFAULT_BLOCK_SPEED = 10


class BlockControlService:
    """
    Handles the overall movement of Tetris.
    """
    block_drop_count = 10

    def __init__(
        self,
        block_drop_speed: int = DEFAULT_BLOCK_SPEED,
        current_block_x: Optional[int] = None,
        current_block_y: Optional[int] = None
    ):
        self.current_block_x = current_block_x if current_block_x else 580
        self.current_block_y = current_block_y if current_block_x else 30
        self.current_block_color = COLORS[random.randint(1, 6)]
        self.current_block_shape = get_next_block(random.randint(0, 6))
        self.next_block_color = COLORS[random.randint(1, 6)]
        self.next_block_shape = get_next_block(random.randint(0, 6))
        self.block_drop_speed = block_drop_speed  # controls the speed at which blocks fall
        self.block_direction = BLOCK_LIST[random.randint(0, 3)]

    def update_next_block(self, _map: list, block_direction: BlockDirection):
        self.copy_block_to_map(_map, block_direction)
        self.current_block_x = 580
        self.current_block_y = 0
        self.current_block_color = self.next_block_color
        self.current_block_shape = self.next_block_shape
        self.next_block_color = COLORS[random.randint(1, 6)]
        self.next_block_shape = get_next_block(random.randint(0, 6))
        self.block_drop_speed = DEFAULT_BLOCK_SPEED

    def drop_block(self, map_range_y: int, is_fast_drop=False):
        """
        Increases the block's coordinates to create the effect of a falling block.
        """
        self.block_drop_count += 1
        if self.block_drop_count < self.block_drop_speed:
            return
        else:
            self.block_drop_count = 0

        if self.current_block_y < ((map_range_y - 1) * 20) - 80:
            if is_fast_drop:
                self.current_block_y += 1
            else:
                self.current_block_y -= (self.current_block_y % 10)  # 20의 배수에서 checkFillBlock()을 실행하기 때문에
                self.current_block_y += 10

    def update_block_coordinate(self, update_x: int, update_y: int):
        self.current_block_y = update_y
        self.current_block_x = update_x

    def copy_block_to_map(
        self,
        _map: list,
        block_direction: int,
    ):
        for i in range(0, 4):
            for j in range(0, 4):
                # 지하철 노선에 따른 색깔
                temp_color = 0
                for color_idx, color in enumerate(COLORS):
                    if self.current_block_color == color:
                        temp_color = color_idx
                if self.current_block_shape[(block_direction * 4) + i][j] >= 1:
                    # todo: 이해하기 쉽게 함수로 정의하기
                    #       20 = offeset 이라고 보면 됨
                    _map[int((self.current_block_y / 20) + i)][int(((self.current_block_x - 300) / 20) + j)] = temp_color

        # todo: initialize map
        # Tetris.mapInit()

    def change_block_direction(self):
        self.block_direction = BLOCK_LIST[(self.block_direction + 1) % 4]

    def up_speed(self):
        self.block_drop_speed = 0
