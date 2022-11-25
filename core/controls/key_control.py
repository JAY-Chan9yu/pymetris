from enum import Enum

import pygame

from core.controls.block_control import BlockControlService, BLOCK_COMMON_OFFSET, BLOCK_X_CENTER_OFFSET, BlockData
from core.exceptions import EndOfGameException
from core.sound import SoundService


class ControlKey(int, Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    SPACE = 4


class KeyControlService:
    sound_service = SoundService

    def __init__(self):
        self.current_key_event = [False, False, False, False, False]  # 현재 키 입력
        self.previous_key_event = [False, False, False, False, False]  # 이전 키 입력
        self.move_left_cnt = 0
        self.move_right_cnt = 0
        self.can_move_left = False  # 좌, 우 이동 체크 플래그
        self.can_move_right = False

    def processing_keyboard_event(
        self,
        block_control_service: BlockControlService,
    ):
        # loop through the events
        for event in pygame.event.get():
            # 키가 눌렸을때
            if event.type == pygame.KEYDOWN:
                self.current_key_event = [
                    event.key == pygame.K_UP and block_control_service.current_block_x < 840,
                    event.key == pygame.K_DOWN,
                    event.key == pygame.K_LEFT,
                    event.key == pygame.K_RIGHT,
                    event.key == pygame.K_SPACE
                ]
                self.sound_service.play_clik_sound()

            # key가 떨어졌을때
            if event.type == pygame.KEYUP:
                for i in range(0, 5):
                    self.current_key_event[i] = False

            # if it is quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.move_block_by_keyboard_event(block_control_service)

    def move_block_by_keyboard_event(self, block_control_service: BlockControlService):
        """
        키보드 입력에 따라 블럭을 움직이는 함수
        """
        current_block_x = block_control_service.current_block_x
        current_block_y = block_control_service.current_block_y

        print(f'--------------------------------------------')
        print(f'current_block_x= {current_block_x}, current_block_y = {current_block_y}')
        print(f'key event : {self.current_key_event}')
        print(f'--------------------------------------------')

        if self.current_key_event[ControlKey.LEFT] and self.can_move_left:
            self.move_left_cnt += 1
            if self.move_left_cnt == 5:
                current_block_x -= BLOCK_COMMON_OFFSET
                self.move_left_cnt = 0

        elif self.current_key_event[ControlKey.RIGHT] and self.can_move_right:
            self.move_right_cnt += 1
            if self.move_right_cnt == 5:
                current_block_x += BLOCK_COMMON_OFFSET
                self.move_right_cnt = 0

        # 이전 입력과 현재입력이 다를때 (중복실행 방지)
        elif self.previous_key_event[ControlKey.UP] != self.current_key_event[ControlKey.UP]:
            self.previous_key_event = self.current_key_event
            block_control_service.change_block_direction()

        # 이전 입력과 현재입력이 다를때 (중복실행 방지)
        elif self.previous_key_event[ControlKey.DOWN] != self.current_key_event[ControlKey.DOWN]:
            self.previous_key_event = self.current_key_event
            block_control_service.up_speed()

        elif self.current_key_event[4]:
            ...
            # Tetris.missionClearEvent()

        block_control_service.update_block_coordinate(current_block_x, current_block_y)

    def is_block_can_drop(
        self,
        block_data: BlockData,
        map_range_y: int,
        _map: list
    ) -> bool:
        """
        블럭이 계속 내려올 수 있는지 판단하는 함수
        """
        # 미션 실패(더 이상 내려올 곳이 없을때)
        for block_y_line in range(3, 0, -1):
            for block_x_line, tiny_block in enumerate(
                block_data.current_block_shape[(block_data.block_direction * 4) + block_y_line]
            ):
                if tiny_block == 1 and self.check_underline(block_y_line, block_x_line, block_data, _map):
                    if block_data.current_block_y == 0:  # 게임 종료
                        raise EndOfGameException

                    return False
                # 바닥에 닿았을 경우
                if block_data.current_block_y + 60 == (map_range_y * BLOCK_COMMON_OFFSET) - BLOCK_COMMON_OFFSET:
                    return False

        return True

    def check_can_move_left_and_right(
        self,
        block_data: BlockData,
        _map: list
    ) -> bool:
        """
        블럭이 좌, 우로 이동할 수 있는지 체크하는 함수
        """
        check_can_move_left = True
        check_can_move_right = True

        for block_y_line in range(3, 0, -1):
            for block_x_line, tiny_block in enumerate(
                block_data.current_block_shape[(block_data.block_direction * 4) + block_y_line]
            ):
                if check_can_move_left == 1:
                    if tiny_block == 1 and self._is_exists_block(block_y_line, block_x_line, block_data, _map, True):
                        self.can_move_left = False
                        check_can_move_left = False
                    else:
                        self.can_move_left = True

                if check_can_move_right == 1:
                    if tiny_block == 1 and self._is_exists_block(block_y_line, block_x_line, block_data, _map, False):
                        self.can_move_right = False
                        check_can_move_right = False
                    else:
                        self.can_move_right = True
        return True

    @staticmethod
    def check_underline(
        block_y_line: int,
        block_x_line: int,
        block_data: BlockData,
        _map: list
    ) -> bool:
        """
         map에 블럭이 내려올때 바로 아래라인에 블럭이 차있는지 확인
        """
        y = int(block_data.current_block_y / BLOCK_COMMON_OFFSET) + block_y_line + 1
        x = int((block_data.current_block_x - BLOCK_X_CENTER_OFFSET) / BLOCK_COMMON_OFFSET) + block_x_line
        return _map[y][x] >= 1

    @staticmethod
    def _is_exists_block(
        block_y_line: int,
        block_x_line: int,
        block_data: BlockData,
        _map: list,
        is_left: bool = True
    ) -> bool:
        """
        해당 좌표에 블럭이 존재하는지 체크하는 함수
        """
        direction = -1 if is_left else 1
        y = int(block_data.current_block_y / BLOCK_COMMON_OFFSET) + block_y_line
        x = int((block_data.current_block_x - BLOCK_X_CENTER_OFFSET) / BLOCK_COMMON_OFFSET) + block_x_line + direction
        # 화면 밖으로 나가는 경우 블럭이 있다고 가정
        if x >= 30 or x < 0:
            return True
        return _map[y][x] >= 1
