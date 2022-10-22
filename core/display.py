import random
from typing import Callable, List, Optional

import pygame
from pydantic import BaseModel
from pygame.surface import Surface

from core.colors import COLORS, ColorType
from core.controls.block_control import BlockType, BlockDirection
from utils.images import IMAGE_LOADER
from utils.uow import AbstractUnitOfWorks


class BackgroundBatch(BaseModel):
    func: Callable
    parms: Optional[dict] = None  # function parameter


class DisplayCoordinate(BaseModel):
    x: int
    y: int


class DisplayUnitOfWorks(AbstractUnitOfWorks):

    def __init__(self):
        self.batches: List[BackgroundBatch] = []
        self.committed = False

    def __exit__(self, *args):
        super().__exit__(*args)
        self.batches.clear()

    def add_batch(self, batch: BackgroundBatch):
        self.batches.append(batch)

    def allocate(self):
        for batch in self.batches:
            if batch.parms:
                batch.func(**batch.parms)
            else:
                batch.func()

    def commit(self):
        # update display
        pygame.display.update()

    def rollback(self):
        pass


class DisplayService:
    """
    디스플레이 전반적인 핸들링을 나루는 클래스
    todo: map을 핸들링 하는 클래스를 나누는게 좋을듯
    """

    # block images
    IMG_BLOCK, IMG_LINE, IMG_MISSION_START, IMG_MISSION_END, \
        IMG_MISSION_CLEAR, IMG_MISSION_FAIL, IMG_PREVIEW_BLOCK, IMG_GAME_CLEAR = map(
            IMAGE_LOADER,
            [
                "block.jpg", "line.png", "Metro2_start.png", "Metro2_end.png", "missionClearImg.png",
                "missionFailImg.png", "previewBlock.png", "gameClearImg.png"
            ]
        )
    # Background images
    BACKGROUND, INIT_BACKGROUND, DESCRIPTION_BACKGROUND = map(
        IMAGE_LOADER, ["background.jpg", "init_background.jpg", "description_background.jpg"]
    )

    def __init__(self, screen: Surface):
        self.screen = screen

    def init_map(self, _map: list, map_range_y: int, map_range_x: int):
        for _ in range(map_range_y):
            _map.append([0] * map_range_x)

    def draw_background(self):
        self.screen.blit(self.BACKGROUND, (0, 0))
        pygame.draw.rect(self.screen, ColorType.BLACK.value, pygame.Rect(300, 0, 600, 800))

    def draw_map(self, _map: list):
        self.draw_background()

        for i, map_y in enumerate(_map):
            # todo: 300, 20 상수로 정의하기 20은 y offset, 300은 배경 x축 중간 좌표
            temp_x = 300
            temp_y = 20 * i
            for j, map_x in enumerate(map_y):
                temp_color = 0
                # 지하철 노선에 따른 색깔
                if 0 < map_x <= 6:
                    temp_color = COLORS[map_x].value
                if 1 <= map_x <= 30:
                    pygame.draw.rect(self.screen, temp_color, pygame.Rect(temp_x, temp_y, 20, 20))
                temp_x += 20

    def draw_block(
        self,
        block_type: BlockType,
        block_direction: BlockDirection,
        block_shape: list,
        color: set,
        coordinate: DisplayCoordinate,
    ):
        for i in range(0, 4):
            y_block = block_shape[(block_direction * 4) + i]
            temp_x = coordinate.x
            temp_y = coordinate.y + (20 * i)  # block 크기 20 X 20(픽셀)

            for j, x_block in enumerate(y_block):
                if x_block >= 1:
                    if block_type == BlockType.IMAGE:
                        self.screen.blit(self.IMG_PREVIEW_BLOCK, (temp_x, temp_y))
                    else:
                        pygame.draw.rect(self.screen, color, pygame.Rect(temp_x, temp_y, 20, 20))
                temp_x += 20

    def change_stage(self, stage_level: int, _map: list, map_range_y: int):
        for i in range(0, map_range_y):
            _map[i][30] = 88

        if stage_level == 0:
            for i in range(0, 28):
                _map[39][i] = 4
                _map[38][i] = 3
                _map[35][i] = 2
                _map[34][i] = 1
            for i in range(2, 29):
                _map[37][i] = 6
                _map[36][i] = 5
                _map[33][i] = 4
                _map[32][i] = 3

        elif stage_level == 1:
            for i in range(25, 40):
                _map[i][15] = 5
                _map[i][14] = 5
            for i in range(30, 40):
                _map[i][16] = 4
                _map[i][13] = 4
            for i in range(35, 40):
                _map[i][17] = 3
                _map[i][12] = 3
            for i in range(35, 40):
                _map[i][0] = 6
                _map[i][1] = 6
                _map[i][28] = 6
                _map[i][29] = 6

        elif stage_level == 2:
            for i in range(0, 20):
                _map[39][i] = 4
                _map[38][i] = 3
                _map[37][i] = 2
                _map[36][i] = 1
            for i in range(18, 29):
                _map[35][i] = 6
                _map[34][i] = 5
                _map[33][i] = 4
                _map[32][i] = 3

        elif stage_level == 3:
            for i in range(20, 40):
                if i % 2 == 0:
                    for j in range(1, 29):
                        _map[i][j] = random.randint(1, 6)
                else:
                    for j in range(0, 28):
                        _map[i][j] = random.randint(1, 6)
