import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from core.colors import COLORS, ColorType
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
BLOCK_COMMON_OFFSET = 20
BLOCK_X_CENTER_OFFSET = 300


@dataclass
class BlockData:
    current_block_x: int
    current_block_y: int
    current_block_color: ColorType
    current_block_shape: list
    next_block_color: ColorType
    next_block_shape: list
    block_drop_speed: int
    block_direction: BlockDirection


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

    @property
    def block_data(self) -> BlockData:
        """블럭 데이터를 참조하는 곳에서 데이터를 사용할 수 있는 블럭 데이터 클래스를 반환한다"""
        return BlockData(
            current_block_x=self.current_block_x,
            current_block_y=self.current_block_y,
            current_block_color=self.current_block_color,
            current_block_shape=self.current_block_shape,
            next_block_color=self.next_block_color,
            next_block_shape=self.next_block_shape,
            block_drop_speed=self.block_drop_speed,
            block_direction=self.block_direction
        )

    def update_next_block(self, _map: list, block_direction: BlockDirection):
        self.copy_block_to_map(_map, block_direction)
        self.current_block_x = 580
        self.current_block_y = 0
        self.current_block_color = self.next_block_color
        self.current_block_shape = self.next_block_shape
        self.next_block_color = COLORS[random.randint(1, 6)]
        self.next_block_shape = get_next_block(random.randint(0, 6))
        self.block_drop_speed = DEFAULT_BLOCK_SPEED
        self.block_direction = BlockDirection.UP

    def drop_block(self, map_range_y: int, is_fast_drop=False):
        """
        Increases the block's coordinates to create the effect of a falling block.
        """
        self.block_drop_count += 1
        if self.block_drop_count < self.block_drop_speed:
            return
        else:
            self.block_drop_count = 0

        if self.current_block_y < (map_range_y * BLOCK_COMMON_OFFSET) - 80:
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
                    _map[int((self.current_block_y / BLOCK_COMMON_OFFSET) + i)][
                        int(((self.current_block_x - BLOCK_X_CENTER_OFFSET) / BLOCK_COMMON_OFFSET) + j)
                    ] = temp_color

    def change_block_direction(self):
        self.block_direction = BLOCK_LIST[(self.block_direction + 1) % 4]

    def up_speed(self):
        self.block_drop_speed = 0

    @staticmethod
    def remove_full_line(_map: list, map_range_x: int, map_range_y: int):
        """꽉찬 라인을 제거 하고 한칸 내린다"""
        for i in range(map_range_y - 1, 0, -1):

            if not all(_map[i]):
                continue
            for t in range(i, 1, -1):
                _map[t] = _map[t - 1]
                _map[0] = [0 * map_range_x]
