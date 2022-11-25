import random
import time
from dataclasses import dataclass
from enum import Enum

import pygame

from core.controls.block_control import BlockControlService
from core.controls.key_control import KeyControlService
from core.display import DisplayService, DisplayUnitOfWorks, DisplayBatch
from core.exceptions import EndOfGameException


class GameStatus(int, Enum):
    NONE = 0
    RUN = 1
    READY = 2
    DESCRIPTION = 3
    EXIT = 4


@dataclass
class MissionCoordinate:
    start_x: int
    start_y: int
    end_x: int
    end_y: int


class MetrisGameService:
    """
    Handles overall game settings
    """
    MAP_RANGE_X = 30  # 33
    MAP_RANGE_Y = 40
    SCREEN_WIDTH = 1200  # 640
    SCREEN_HEIGHT = 900  # 480
    metris_map = []
    status = GameStatus.READY

    def __init__(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.display_service = DisplayService(self.screen, self.MAP_RANGE_X, self.MAP_RANGE_Y)
        self.block_control_service = BlockControlService()
        self.key_control_service = KeyControlService()
        self.display_unit_of_works = DisplayUnitOfWorks
        self.display_service.change_mission_img(self.block_control_service.block_data.current_mission_block_color_num)
        self.current_mission_coordinate = None
        self.reset_mission_coordinate()
        self.stage_level = 1

    def initialize_game(self):
        pygame.init()
        self.metris_map = []
        self.draw_map()

    def reset_mission_coordinate(self):
        self.current_mission_coordinate = MissionCoordinate(
            start_x=random.choice([0, 30]),
            start_y=random.randint(10, 40),
            end_x=random.randint(0, 30),
            end_y=40,
        )

    def reset(self):
        self.initialize_game()
        self.draw_map()

    def play_game(self):
        self.draw_menu()

        while True:
            try:
                if self.status == GameStatus.RUN:
                    self.process_block_key_event()
                    self.draw_basic_display()

                elif self.status == GameStatus.READY:
                    self.draw_menu()
                    self.process_menu_click_event()

                elif self.status == GameStatus.DESCRIPTION:
                    self.process_description_menu_event()

                else:
                    pygame.quit()
                    exit()

            except EndOfGameException:
                self.process_fail()

    def process_block_key_event(self):
        self.block_control_service.remove_full_line(self.metris_map, self.MAP_RANGE_X, self.MAP_RANGE_Y)
        self.block_control_service.drop_block(self.MAP_RANGE_Y)
        self.key_control_service.processing_keyboard_event(self.block_control_service)
        self.key_control_service.check_can_move_left_and_right(self.block_control_service.block_data, self.metris_map)

        # 블럭이 내려 올 수 있는지 체크
        is_block_can_drop = self.key_control_service.is_block_can_drop(
            self.block_control_service.block_data,
            self.MAP_RANGE_Y,
            self.metris_map
        )
        if not is_block_can_drop:
            self.block_control_service.update_next_block(self.metris_map, self.block_control_service.block_direction)

    def process_fail(self):
        uow = self.display_unit_of_works()
        uow.batches.append(DisplayBatch(func=self.display_service.draw_mission_fail))
        with uow:
            uow.allocate()
        self.status = GameStatus.READY
        time.sleep(1)

    def process_menu_click_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # 이미지 y축
                if not 588 >= pos[1] >= 380:
                    continue

                # 이미지 x축
                if 522 >= pos[0] >= 465:
                    self.initialize_game()
                    self.status = GameStatus.RUN

                elif 643 >= pos[0] >= 586:
                    self.draw_description_menu()
                    self.status = GameStatus.DESCRIPTION

                elif 772 >= pos[0] >= 715:
                    self.status = GameStatus.EXIT

            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def process_description_menu_event(self):
        # description 페이지 관련 메소드(사용자 정보 입력 등)
        # gameID = ['d', 'e', 'f', 'a', 'u', 'l', 't']
        # tmpChar  = ''
        # Tetris.drawText(390, 635, ''.join(Tetris.gameID), 27)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                ...
                # inputKey = [K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m,
                #             K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z]
                # if len(Tetris.gameID) < 25 :
                #     for i, inputChar in enumerate(inputKey) :
                #         if event.key == inputChar :
                #             tmpChar = ord('a') + i  # 아스키값
                #             Tetris.gameID.append(chr(tmpChar))  # 아스키값을 char값으로 변환
                #     if event.key == K_SPACE :
                #         Tetris.gameID.append(' ')
                # if event.key == K_BACKSPACE and len(Tetris.gameID) > 0 :
                #     Tetris.gameID.pop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 1065 >= pos[0] >= 865 and 165 >= pos[1] >= 90:
                    self.draw_menu()
                    self.status = GameStatus.READY

            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def draw_menu(self):
        uow = self.display_unit_of_works()
        uow.batches.append(DisplayBatch(func=self.display_service.draw_menu_background))
        with uow:
            uow.allocate()

    def draw_map(self):
        uow = self.display_unit_of_works()
        uow.batches.append(DisplayBatch(
            func=self.display_service.init_map,
            parms={'_map': self.metris_map, 'map_range_y': self.MAP_RANGE_Y, 'map_range_x': self.MAP_RANGE_X})
        )
        uow.batches.append(DisplayBatch(
            func=self.display_service.change_stage, parms={'stage_level': self.stage_level, '_map': self.metris_map})
        )
        uow.batches.append(DisplayBatch(func=self.display_service.draw_map, parms={'_map': self.metris_map}))

        with uow:
            uow.allocate()

    def draw_description_menu(self):
        uow = self.display_unit_of_works()
        uow.batches.append(DisplayBatch(func=self.display_service.draw_description_menu))
        with uow:
            uow.allocate()

    def draw_basic_display(self):
        """
        게임 기본 화면 그리기
        """
        # 화면 갱신
        uow = self.display_unit_of_works()
        # 백그라운드 그리기
        uow.batches.append(DisplayBatch(
            func=self.display_service.draw_map,
            parms={'_map': self.metris_map})
        )
        # 현재 블럭 그리기
        uow.batches.append(DisplayBatch(
            func=self.display_service.draw_current_block,
            parms={'block_data': self.block_control_service.block_data})
        )
        # 다음에 나올 블럭 그리기 (미리보기)
        uow.batches.append(DisplayBatch(
            func=self.display_service.draw_next_block,
            parms={'block_data': self.block_control_service.block_data})
        )
        uow.batches.append(DisplayBatch(
            func=self.display_service.draw_preview_block,
            parms={'block_data': self.block_control_service.block_data,
                   '_map': self.metris_map})
        )
        uow.batches.append(DisplayBatch(
            func=self.display_service.draw_mission_background,
            parms={'mission_coordinate': self.current_mission_coordinate,
                   'current_mission_block_color_num': self.block_control_service.block_data.current_mission_block_color_num})
        )
        with uow:
            uow.allocate()

    # def check_mission_clear(self, x, y, cnt, _map, mission_color):
    #     mapRangeX, mapRangeY = 33, 40
    #     block_x = 15
    #     block_y = 40
    #     min_path = 999  # 최단경로
    #     min_path_location = []
    #
    #     temp_path = []
    #     if _map[y][x] == mission_color:
    #         temp_path.append([y, x])  # 경로 추가
    #
    #         if x == block_x - 1 and y == block_y - 1:  # 최단거리 업데이트
    #             if cnt < min_path:
    #                 min_path = cnt
    #                 min_path_location.clear()
    #                 min_path_location = list(temp_path)  # list 복사
    #
    #         temp_map = _map[y][x]
    #         _map[y][x] = 0
    #         checkMapped = [x < mapRangeX - 3, y < mapRangeY, y > 0, x > 0]
    #         gotoMapped = [(x + 1, y), (x, y + 1), (x, y - 1), (x - 1, y)]
    #
    #         for i, _map in enumerate(checkMapped):
    #             if _map:
    #                 self.check_mission_clear(gotoMapped[i][0], gotoMapped[i][1], cnt + 1)
    #
    #         temp_path.pop()  # 이미 체크한 경로 삭제
    #         _map[y][x] = temp_map
