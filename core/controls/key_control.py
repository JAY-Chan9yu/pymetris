from enum import Enum

import pygame

from core.controls.block_control import BlockControlService


class ControlKey(int, Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    SPACE = 4


class KeyControlService:
    BLOCK_COMMON_OFFSET = 20
    BLOCK_X_CENTER_OFFSET = 300

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
            if event.type == pygame.KEYDOWN:
                self.current_key_event = [
                    event.key == pygame.K_UP and block_control_service.current_block_x < 840,
                    event.key == pygame.K_DOWN,
                    event.key == pygame.K_LEFT,
                    event.key == pygame.K_RIGHT,
                    event.key == pygame.K_SPACE
                ]
                # pygame.mixer.Sound.play(Tetris.btnSound)

            # key가 떨어졌을때
            if event.type == pygame.KEYUP:
                for i in range(0, 5):
                    self.current_key_event[i] = False

            # if it is quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.move_block_by_keyboard_event(block_control_service)

    def move_block_by_keyboard_event(
        self,
        block_control_service: BlockControlService,
    ):
        current_block_x = block_control_service.current_block_x
        current_block_y = block_control_service.current_block_y

        print(f'--------------------------------------------')
        print(f'current_block_x= {current_block_x}, current_block_y = {current_block_y}')
        print(f'key event : {self.current_key_event}')
        print(f'{self.move_left_cnt}, {self.move_right_cnt}')
        print(f'--------------------------------------------')

        if self.current_key_event[ControlKey.LEFT] and current_block_x > 300 and self.can_move_left:
            # self.move_left_cnt += 1
            # if self.move_left_cnt == 10000:
            #     current_block_x -= 20
            #     self.move_left_cnt = 0
            current_block_x -= 20

        elif self.current_key_event[ControlKey.RIGHT] and current_block_x < 860 and self.can_move_right:
            # self.move_right_cnt += 1
            # if self.move_right_cnt == 10000:
            #     current_block_x += 20
            #     self.move_right_cnt = 0
            current_block_x += 20

        # 이전 입력과 현재입력이 다를때 (중복실행 방지)
        elif self.previous_key_event[ControlKey.UP] != self.current_key_event[ControlKey.UP]:
            self.previous_key_event = self.current_key_event
            # Tetris.changeBlockShape = (Tetris.changeBlockShape + 1) % 4

        # 이전 입력과 현재입력이 다를때 (중복실행 방지)
        elif self.previous_key_event[ControlKey.DOWN] != self.current_key_event[ControlKey.DOWN]:
            # 게임 스피드 증가시키는 로직
            self.previous_key_event = self.current_key_event
            # Tetris.blockTimer1 = 1
            # Tetris.fastDownFlag = 1

        elif self.current_key_event[4]:
            ...
            # Tetris.missionClearEvent()

        block_control_service.update_block_coordinate(current_block_x, current_block_y)

    def is_block_can_drop(
        self,
        current_block_shape: list,
        block_direction: int,
        map_range_y: int,
        current_block_y: int,
        current_block_x: int,
        _map: list
    ) -> bool:
        for block_y_line in range(3, 0, -1):
            for block_x_line, tiny_block in enumerate(current_block_shape[(block_direction * 4) + block_y_line]):
                # map에 블럭이 내려올때 바로 아래단에 블럭이 차있는지 확인 or 바닥에 닿았을 경우
                if ((tiny_block == 1 and (_map[int(current_block_y / 20) + block_y_line + 1][int((current_block_x - 300) / 20) + block_x_line] >= 1))
                        or (current_block_y + 60 == ((map_range_y - 1) * 20) - 20)):
                    # 미션 실패(더 이상 내려올 곳이 없을때)
                    if current_block_y == 0:
                        return False

                    return False

        return True

    def check_can_move_left_and_right(
        self,
        current_block_shape: list,
        block_direction: int,
        current_block_y: int,
        current_block_x: int,
        _map: list
    ) -> bool:
        check_can_move_left = True
        check_can_move_right = True

        for block_y_line in range(3, 0, -1):
            for block_x_line, tiny_block in enumerate(current_block_shape[(block_direction * 4) + block_y_line]):
                if check_can_move_left == 1:
                    if tiny_block == 1 and \
                            (self._is_exists_block(block_y_line, block_x_line, current_block_y, current_block_x, _map, True)):
                        self.can_move_left = False
                        check_can_move_left = False
                    else:
                        self.can_move_left = True

                if check_can_move_right == 1:
                    if tiny_block == 1 and \
                            (self._is_exists_block(block_y_line, block_x_line, current_block_y, current_block_x, _map, False)):
                        self.can_move_right = False
                        check_can_move_right = False
                    else:
                        self.can_move_right = True

        return True

    def _is_exists_block(
        self,
        block_y_line: int,
        block_x_line: int,
        current_block_y: int,
        current_block_x: int,
        _map: list,
        is_left: bool = True
    ) -> bool:
        direction = -1 if is_left else 1
        return _map[int(current_block_y / self.BLOCK_COMMON_OFFSET) + block_y_line][
                   int((current_block_x - self.BLOCK_X_CENTER_OFFSET)
                       / self.BLOCK_COMMON_OFFSET) + block_x_line + direction] >= 1
