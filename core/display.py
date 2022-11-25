import random
from typing import Callable, List, Optional

import pygame
from pydantic import BaseModel
from pygame.surface import Surface

from utils.colors import COLORS, ColorType
from core.controls.block_control import BlockType, BlockDirection, BLOCK_X_CENTER_OFFSET, BLOCK_COMMON_OFFSET, BlockData
from utils.images import IMAGE_LOADER
from utils.uow import AbstractUnitOfWorks


class DisplayBatch(BaseModel):
    func: Callable
    parms: Optional[dict] = None  # function parameter


class DisplayCoordinate(BaseModel):
    x: int
    y: int


class DisplayUnitOfWorks(AbstractUnitOfWorks):

    def __init__(self):
        self.batches: List[DisplayBatch] = []
        self.committed = False

    def __exit__(self, *args):
        super().__exit__(*args)
        self.batches.clear()

    def add_batch(self, batch: DisplayBatch):
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

    metro_img_names = [
        "Metro1_start", "Metro2_start", "Metro3_start", "Metro4_start", "Metro5_start", "Metro6_start",
        "Metro1_end", "Metro2_end", "Metro3_end", "Metro4_end", "Metro5_end", "Metro6_end",
    ]

    # block images
    BLOCK_IMG, LINE_IMG, MISSION_START_IMG, MISSION_END_IMG, MISSION_CLEAR_IMG, MISSION_FAIL_IMG, PREVIEW_BLOCK_IMG, \
        IMG_GAME_CLEAR = map(
            IMAGE_LOADER,
            [
                "block.jpg", "line.png", "Metro2_start.png", "Metro2_end.png", "missionClearImg.png",
                "missionFailImg.png", "previewBlock.png", "gameClearImg.png"
            ]
        )
    # Background images
    BACKGROUND, MENU_BACKGROUND, DESCRIPTION_BACKGROUND = map(
        IMAGE_LOADER,
        ["background.jpg", "init_background.jpg", "description_background.jpg"]
    )

    # 버튼 이미지 관련
    BIG_START_IMG, SMALL_START_IMG, BIG_END_IMG, SMALL_END_IMG, BIG_DESCRIPTION_IMG, SMALL_DESCRIPTION_IMG = map(
        IMAGE_LOADER,
        ["bigStart.png", "smallStart.png", "bigEnd.png", "smallEnd.png", "bigDescription.png", "smallDescription.png"]
    )

    def __init__(self, screen: Surface, map_range_x: int, map_range_y: int):
        self.screen = screen
        self.map_range_x = map_range_x
        self.map_range_y = map_range_y

    @staticmethod
    def init_map(_map: list, map_range_y: int, map_range_x: int):
        for _ in range(map_range_y + 1):
            _map.append([0] * map_range_x)

    def draw_background(self):
        self.screen.blit(self.BACKGROUND, (0, 0))
        pygame.draw.rect(self.screen, ColorType.BLACK.value, pygame.Rect(300, 0, 600, 800))

    def draw_mission_background(self, mission_coordinate, current_mission_block_color_num: int):
        self.draw_mission_img(mission_coordinate.start_x, mission_coordinate.start_y, current_mission_block_color_num, self.MISSION_START_IMG)
        self.draw_mission_img(mission_coordinate.end_x, mission_coordinate.end_y - 1, current_mission_block_color_num, self.MISSION_END_IMG)

    def draw_map(self, _map: list):
        self.draw_background()

        for i, map_y in enumerate(_map):
            # todo: 300, 20 상수로 정의하기 20은 y offset, 300은 배경 x축 중간 좌표
            temp_x = BLOCK_X_CENTER_OFFSET
            temp_y = BLOCK_COMMON_OFFSET * i
            for j, map_x in enumerate(map_y):
                temp_color = 0
                # 지하철 노선에 따른 색깔
                if 0 < map_x <= 6:
                    temp_color = COLORS[map_x].value
                if 1 <= map_x <= 30:
                    pygame.draw.rect(
                        self.screen,
                        temp_color,
                        pygame.Rect(temp_x, temp_y, BLOCK_COMMON_OFFSET, BLOCK_COMMON_OFFSET)
                    )
                temp_x += BLOCK_COMMON_OFFSET

    def draw_mission_fail(self):
        self.screen.blit(self.MISSION_FAIL_IMG, (315, 250))
        # Tetris.drawText(598, 345, str(Tetris.stageLevel + 1), 30)

    def draw_menu_background(self):
        self.screen.blit(self.MENU_BACKGROUND, (0, 0))
        # 메뉴 이미지 그리기
        pos = pygame.mouse.get_pos()
        x_inx = [522 >= pos[0] >= 455, 643 >= pos[0] >= 586, 772 >= pos[0] >= 715]
        big_mapped = zip(
            x_inx,
            [(self.BIG_START_IMG, (445, 340)),
             (self.BIG_DESCRIPTION_IMG, (576, 340)),
             (self.BIG_END_IMG, (705, 340))]
        )
        small_menu_img_map = [
            (self.SMALL_START_IMG, (455, 380)),
            (self.SMALL_END_IMG, (715, 380)),
            (self.SMALL_DESCRIPTION_IMG, (586, 380))
        ]

        for img_map in small_menu_img_map:
            self.screen.blit(img_map[0], img_map[1])

        # 마우스가 메뉴 위에 올라가면 큰 이미지로 보이기
        if 588 >= pos[1] >= 380:
            for p, image_map in big_mapped:
                if not p:
                    continue
                self.screen.blit(image_map[0], image_map[1])

    def draw_current_block(self, block_data: BlockData):
        self.draw_block(
            block_type=BlockType.COLOR,
            block_shape=block_data.current_block_shape,
            color=block_data.current_block_color,
            coordinate=DisplayCoordinate(x=block_data.current_block_x, y=block_data.current_block_y),
            block_direction=block_data.block_direction
        )

    def draw_preview_block(self, block_data: BlockData, _map):
        """
        블럭 미리보기
        """
        block_size_y_offset = 3  # 바닥에 닿을때 블럭 사이즈 만큼 오프셋
        for y in range(int(block_data.current_block_y / BLOCK_COMMON_OFFSET), self.map_range_y - block_size_y_offset):
            # 가장 아래 라인부터 체크
            for block_shape_x_line in range(3, 0, -1):
                current_block_shape_line = block_data.current_block_shape[
                    (block_data.block_direction * 4) + block_shape_x_line
                ]

                for idx, tiny_block in enumerate(current_block_shape_line):
                    under_line = y + block_shape_x_line + 1
                    x = int((block_data.current_block_x - BLOCK_X_CENTER_OFFSET) / BLOCK_COMMON_OFFSET) + idx
                    if x >= self.map_range_x:
                        continue

                    check_under_line_block = _map[under_line][x]
                    preview_y = y + block_size_y_offset
                    if (tiny_block and check_under_line_block) or preview_y >= self.map_range_y - 1:
                        self.draw_block(
                            block_type=BlockType.IMAGE,
                            block_shape=block_data.current_block_shape,
                            color=block_data.current_block_color,
                            coordinate=DisplayCoordinate(
                                x=block_data.current_block_x,
                                y=(preview_y * BLOCK_COMMON_OFFSET) - 60
                            ),
                            block_direction=block_data.block_direction
                        )
                        return

    def draw_next_block(self, block_data: BlockData):
        self.draw_block(
            block_type=BlockType.COLOR,
            block_shape=block_data.next_block_shape,
            color=block_data.next_block_color,
            coordinate=DisplayCoordinate(x=940, y=0)
        )

    def draw_block(
        self,
        block_type: BlockType,
        block_shape: list,
        color: ColorType,
        coordinate: DisplayCoordinate,
        block_direction: BlockDirection = BlockDirection.UP,
    ):
        for i in range(0, 4):
            y_block = block_shape[(block_direction * 4) + i]
            temp_x = coordinate.x
            temp_y = coordinate.y + (BLOCK_COMMON_OFFSET * i)  # block 크기 20 X 20(픽셀)

            for j, x_block in enumerate(y_block):
                if x_block >= 1:
                    if block_type == BlockType.IMAGE:
                        self.screen.blit(self.PREVIEW_BLOCK_IMG, (temp_x, temp_y))
                    else:
                        pygame.draw.rect(
                            self.screen,
                            color.value,
                            pygame.Rect(temp_x, temp_y, BLOCK_COMMON_OFFSET, BLOCK_COMMON_OFFSET)
                        )
                temp_x += BLOCK_COMMON_OFFSET

    def draw_description_menu(self):
        self.screen.blit(self.DESCRIPTION_BACKGROUND, (0, 0))

    def draw_mission_img(self, x: int, y: int, current_mission_block_color_num: int, image):
        offset_x = x * BLOCK_COMMON_OFFSET
        offset_y = y * BLOCK_COMMON_OFFSET
        mapped = [
            (offset_x + 200, offset_y - 40, 280, -20),
            (offset_x + 260, offset_y + 40, 280, 20),
            (offset_x + 320, offset_y - 40, 300, -20)
        ]
        position_mapped = [x == 0, 0 < x < 29, x == 30]

        for idx, m in enumerate(position_mapped):
            if not m:
                continue
            self.screen.blit(image, (mapped[idx][0], mapped[idx][1]))
            pygame.draw.rect(
                self.screen, COLORS[current_mission_block_color_num].value,
                pygame.Rect(
                    (x * BLOCK_COMMON_OFFSET) + mapped[idx][2],
                    (y * BLOCK_COMMON_OFFSET) + mapped[idx][3],
                    BLOCK_COMMON_OFFSET,
                    BLOCK_COMMON_OFFSET
                )
            )

    def change_mission_img(self, current_mission_block_color_num: int):
        self.MISSION_START_IMG = IMAGE_LOADER(self.metro_img_names[current_mission_block_color_num - 1] + ".png")
        self.MISSION_END_IMG = IMAGE_LOADER(self.metro_img_names[current_mission_block_color_num - 1] + ".png")

    @staticmethod
    def change_stage(stage_level: int, _map: list):
        if stage_level == 1:
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

        elif stage_level == 2:
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

        elif stage_level == 3:
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

        elif stage_level == 4:
            for i in range(20, 40):
                if i % 2 == 0:
                    for j in range(1, 29):
                        _map[i][j] = random.randint(1, 6)
                else:
                    for j in range(0, 28):
                        _map[i][j] = random.randint(1, 6)
