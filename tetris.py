import pygame
from sys import exit
from pygame.locals import *
import math
from math import floor
import random
import blocklib
import datetime
import requests
import threading
import time
import datetime

pygame.mixer.init()
class Tetris(object) :
    # 게임 결과(data)를 보낼 Server IP(local Test 중)
    #url = 'http://127.0.0.1:8000/'
    url = 'http://13.115.233.106/'
    # Load sounds
    btnSound = pygame.mixer.Sound("TetrisResource/audio/effect1.wav")
    # load images
    _image_load = lambda x: pygame.image.load("TetrisResource/image/%s"%x)
    # 블럭 관련 이미지
    block, line, missionStartImg, missionEndImg, missionClearImg, missionFailImg, previewBlockImg, gameClearImg = map(_image_load, [
        "block.jpg", "line.png", "Metro2_start.png", "Metro2_end.png", "missionClearImg.png","missionFailImg.png","previewBlock.png", "gameClearImg.png"])
    # Background 이미지
    background, initBackground, descriptionBackground = map(_image_load, [
        "background.jpg", "init_background.jpg", "description_background.jpg"])
    # 버튼 이미지 관련
    bigStartImg, smallStartImg, bigEndImg, smallEndImg, bigDescriptionImg, smallDescriptionImg = map(_image_load, [
        "bigStart.png", "smallStart.png", "bigEnd.png", "smallEnd.png", "bigDescription.png", "smallDescription.png" ])

    width, height = 1200, 900           # screen width, height
    screen = pygame.display.set_mode((width, height))

    mapRangeX, mapRangeY = 33, 41       # 스테이지 length

    # colorvlue list
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 176, 80)
    BLUE = (0, 176, 240)
    NAVY = (0, 32, 96)
    WHITE = (255, 255, 255)
    PURPLE = (112, 48, 160)
    BROWN = (191, 144, 0)
    ORANGE = (237, 125, 49)

    # 블럭이 없으면 0, 있으면 1 <- 여기서 랜덤으로 2~5의 값을 주어 1이면 블럭의 색값을 부여한다.
    colors = [BLACK, NAVY, GREEN, ORANGE, BLUE, PURPLE, BROWN]
    metroImgs = ["Metro1_start" ,"Metro2_start", "Metro3_start" ,"Metro4_start", "Metro5_start" ,"Metro6_start",
                 "Metro1_end" ,"Metro2_end", "Metro3_end" ,"Metro4_end", "Metro5_end" ,"Metro6_end",]

    stageLevel = 0                     # 게임 스테이지

    blockTimer = 5000                   # 게임 스피드
    blockTimer1 = 5000

    keys = [False, False, False, False, False] # key 값 판단하는 리스트

    Map = []                            # 블럭 1개 = 20 x 20

    gameSequence = 0                    # game play 진행 순서
    changeBlockShape = 0                # 블럭의 모양을 변경하는 변수
    nowBlockShape = blocklib.block1     # 현재 나오는 블럭의 모양
    nextBlockShape = blocklib.block1    # 다음 블럭
    blockColor = ORANGE                 # 블럭 색상
    nextColor = BLUE                    # 다음 블럭 색상
    checkMoveR = 0                      # 좌, 우 이동 체크 플래그
    checkMoveL = 0
    blockX = 580                        # 현재 나오는 블럭의 x,y 좌표
    blockY = 0

    gameClearFlag = 0                   # game clear 이벤트 플래그
    missionClearEventFlag = 0           # mission clear 이벤틀 플래그
    missionColor = 2                    # 미션 컬러
    minPath = 999                       # 최단경로
    minPathLocation = []                # 최단경로 좌표
    saveLocation = 0                    # 최단경로 좌표 저장 승인 플래그
    startPathX = 0                      # 미션 경로(시작과 끝)
    startPathY = 27
    endPathX = 15
    endPathY = 40

    fastDownFlag = 0                    # 블럭 빨리 내리기

    sendDataToServer = 0                # 서버로 데이터를 보내는 flag
    gamePlayTime = []                   # 게임 진행 시간
    resultScore = 0                     # 최종 게임 스코어
    resultTime = 0                      # 최종 게임 진행시간(초단위)

    # 생성자
    def __init__(self) :
        # 블럭 초기화
        Tetris.Map = [[0] * Tetris.mapRangeX for row in range(Tetris.mapRangeY)]

    # 게임 초기 설정
    @staticmethod
    def gameInit() :
        Tetris.mapInit()
        # Next mission Initialize
        Tetris.minPath = 999
        Tetris.missionColor = random.randint(1, 6)
        Tetris.startPathX = blocklib.stageLevel[Tetris.stageLevel][0]
        Tetris.startPathY = blocklib.stageLevel[Tetris.stageLevel][1]
        Tetris.endPathX = blocklib.stageLevel[Tetris.stageLevel][2]
        Tetris.endPathY = blocklib.stageLevel[Tetris.stageLevel][3]
        Tetris.missionStartImg = Tetris._image_load(Tetris.metroImgs[Tetris.missionColor - 1] + ".png")
        Tetris.missionEndImg = Tetris._image_load(Tetris.metroImgs[(Tetris.missionColor - 1) + 6] +".png")
        Tetris.Map.clear()
        Tetris.missionClearEventFlag = 0
        Tetris.gameClearMessage = ''
        Tetris.Map = [[0] * Tetris.mapRangeX for row in range(Tetris.mapRangeY)]
        Tetris.nextBlockShape = blocklib.randBlock(random.randint(0, 3))
        Tetris.stageChange(Tetris.stageLevel)
        # 게임 시작 시간 저장
        Tetris.gamePlayTime = time.time()
        # game 배경화면
        Tetris.screen.blit(Tetris.background, (0, 0))
        pygame.draw.rect(Tetris.screen, Tetris.BLACK, pygame.Rect(300, 0, 600, 800))
        Tetris.drawText(1050, 180,'스테이지 레벨 : '+ str(Tetris.stageLevel + 1), 35)
        pygame.display.flip()

    # map 초기화
    def mapInit() :
        Tetris.blockTimer1 = 5000
        Tetris.blockColor = Tetris.nextColor
        Tetris.changeBlockShape = 0
        Tetris.nowBlockShape = Tetris.nextBlockShape
        Tetris.nextBlockShape = blocklib.randBlock(random.randint(0, 6))
        Tetris.nextColor = Tetris.colors[random.randint(1, 6)]
        Tetris.fastDownFlag = 0

    # 블럭이 바닥에 닿거나 다른 블럭에 닿았을 경우 map에 copy하는 함수
    def copyBlockToMap() :
        for i in range(0, 4) :
            for j in range(0, 4) :
                # 지하철 노선에 따른 색깔
                tempColor = 0
                for idx,x in enumerate(Tetris.colors):
                    if Tetris.blockColor == x:
                        tempColor = idx
                if Tetris.nowBlockShape[(Tetris.changeBlockShape * 4) + i][j] >= 1 :
                    Tetris.Map[int((Tetris.blockY / 20) + i)][int(((Tetris.blockX - 300) / 20) + j)] = tempColor
        Tetris.mapInit()

    # 모든 스테이지를 끝냈을때
    gameClearMessage = ''
    def gameClearEvent(self) :
        if Tetris.gameClearFlag :
            Tetris.gameClearFlag = 0
            Tetris.gameClearMessage = ' [* MVP *]'
            Tetris.screen.blit(Tetris.gameClearImg, (400, 250))
            pygame.display.flip()
            Tetris.missionClearEventFlag = 1
            self.sendDataToServer = 1
            self.gameSequence = 0
            time.sleep(1)

    # 게임 플레이 시간 현시
    def showPlayTime() :
        # 첫 시간 - 현재시간 = 실행시간
        tmpTime = time.time() - Tetris.gamePlayTime
        tmHour = tmpTime / 3600
        tmMin = (tmpTime % 3600) / 60
        tmSec = (tmpTime % 3600) % 60
        Tetris.drawText(390, 425, str(floor(tmHour)) + ':' + str(floor(tmMin)) + ':' + str(floor(tmSec)), 30)

    # 지하철 노선 연결하는 미션 체크하는 함수
    def missionClearEvent() :
        Tetris.dfsSerch(Tetris.startPathX, Tetris.startPathY, 1)
        # 최단경로 나왔을경우  변수 및 화면 초기화
        if Tetris.minPath < 999 :
            # 최단경로 표시
            Tetris.resultScore += Tetris.minPath
            for i in Tetris.minPathLocation :
                Tetris.screen.blit(Tetris.line, ((i[1] * 20) + 300, (i[0] * 20)))
            Tetris.stageLevel += 1
            # game clear 했을 경우
            if Tetris.stageLevel > 3 :
                Tetris.gameClearFlag = 1
            else :
                # 점수, 실행시간 표시
                Tetris.screen.blit(Tetris.missionClearImg, (315, 250))
                Tetris.drawText(598, 345, str(Tetris.stageLevel), 30)
                Tetris.drawText(815, 425, str(Tetris.minPath), 30)
                Tetris.resultTime += floor(time.time() - Tetris.gamePlayTime)
                Tetris.showPlayTime()
                pygame.display.flip()
                Tetris.missionClearEventFlag = 0
                time.sleep(2)
            Tetris.gameInit()

    # 최단거리 탐색(DFS)
    tempPath = []
    def dfsSerch(x, y, cnt) :
        if Tetris.Map[y][x] == Tetris.missionColor :
            Tetris.tempPath.append([y, x]) # 경로 추가
            if x == Tetris.endPathX - 1 and y == Tetris.endPathY - 1: # 최단거리 업데이트
                if cnt < Tetris.minPath :
                    Tetris.minPath = cnt
                    Tetris.minPathLocation.clear()
                    Tetris.minPathLocation = list(Tetris.tempPath) # list 복사
            tempMap = Tetris.Map[y][x]
            Tetris.Map[y][x] = 0
            checkMapped = [x < Tetris.mapRangeX - 3, y < Tetris.mapRangeY - 1, y > 0, x > 0]
            gotoMapped = [(x + 1, y), (x, y + 1), (x, y - 1), (x - 1, y)]
            for i, _map in enumerate(checkMapped) :
                if _map :
                    Tetris.dfsSerch(gotoMapped[i][0], gotoMapped[i][1], cnt + 1)
            Tetris.tempPath.pop() # 이미 체크한 경로 삭제
            Tetris.Map[y][x] = tempMap

    @staticmethod
    def drawText(x, y, text, size) :
        # text 만들기
        fontObj = pygame.font.Font('TetrisResource/font/BMYEONSUNG.ttf', size)
        textSurfaceObj = fontObj.render(text, True, Tetris.BLACK)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x, y)
        Tetris.screen.blit(textSurfaceObj, textRectObj)

    # 맵 하단에 블럭의 위치 미리보기 해주는 기능
    def drawPreviewBlock(self) :
        for k in range(int(Tetris.blockY / 20), 37) :
            for i in range(3, 0, -1) :
                yBlock = Tetris.nowBlockShape[(Tetris.changeBlockShape * 4) + i]
                for j, xBlock in enumerate(yBlock):
                    if ((xBlock >= 1 and Tetris.Map[k + i + 1][int((Tetris.blockX - 300) / 20) + j] >= 1)
                            or (k + 3 == Tetris.mapRangeY - 2)) :
                        previewY = k + 3
                        self.drawBlock(1, Tetris.nowBlockShape, Tetris.WHITE, Tetris.blockX, (previewY * 20) - 60)
                        return

    # block 모양을 그리는 함수
    def drawBlock(self, choiceBlkOrImg, shape, color, x, y) :
        for i in range(0, 4) :
            changeB = [(Tetris.changeBlockShape * 4), (Tetris.changeBlockShape * 4), 0]
            tBlock = shape
            yBlock = tBlock[changeB[choiceBlkOrImg] + i]
            tempX = x
            tempY = y + (20 * i) # block 크기 20 X 20(픽셀)
            for j, xBlock  in enumerate(yBlock) :
                if xBlock >= 1 :
                    # 블럭을 출력할 것인지 이미지를 출력할 것인지(1이면 미리보기용 이미지)
                    if choiceBlkOrImg == 1:
                        Tetris.screen.blit(Tetris.previewBlockImg, (tempX, tempY))
                    else :
                        pygame.draw.rect(Tetris.screen, color, pygame.Rect(tempX, tempY, 20, 20))
                tempX += 20

    # map을 화면에서 볼수 있도록 그려주는 함수i
    @staticmethod
    def drawMap() :
        # draw map.
        for i, yMap in enumerate(Tetris.Map) :
            tempX = 300
            tempY = 20 * i
            for j, xMap  in enumerate(yMap) :
                tempColor = 0
                # 지하철 노선에 따른 색깔
                if 0 < xMap <= 6:
                    tempColor = Tetris.colors[xMap]
                if 30 > xMap >= 1 :
                    pygame.draw.rect(Tetris.screen, tempColor, pygame.Rect(tempX, tempY, 20, 20))
                tempX += 20

    # 게임과 관계 없는 화면에 배경을 그려주는 함수
    def insertImgPosition(x, y, image) :
        _indx = lambda xy : xy * 20
        Mapped = [(_indx(x) + 200 , _indx(y) - 20), (_indx(x) + 260 , _indx(y) + 20), (_indx(x) + 300 , _indx(y) - 20)]
        positionMapped = [x == 0, 30 > x > 0, x == 31]
        for i, m in enumerate(positionMapped) :
            if m :
                Tetris.screen.blit(image, (Mapped[i][0], Mapped[i][1]))

    @staticmethod
    def drawBackbround() :
        tempN = 0
        for i in range(0, 2) :
            tempW = [280, 900]
            tempN = 0
            for j in range(0, Tetris.mapRangeY) :
                Tetris.screen.blit(Tetris.block, (tempW[i], tempN))
                tempN += 20
        tempN = 280
        for i in range(0, Tetris.mapRangeX - 2) :
            Tetris.screen.blit(Tetris.block, (tempN, (Tetris.mapRangeY - 1) * 20))
            tempN += 20
            if i < 6 :
                Tetris.screen.blit(Tetris.block, (920 + (i * 20), 100))
                Tetris.screen.blit(Tetris.block, (1020, (i * 20)))

        pygame.draw.rect(Tetris.screen, Tetris.BLACK, pygame.Rect(920,0, 100, 100))
        # mission start, end  표시
        pygame.draw.rect(Tetris.screen, Tetris.colors[Tetris.missionColor], pygame.Rect((Tetris.startPathX * 20) + 280, (Tetris.startPathY * 20), 20, 20))
        tempVal = 0
        if Tetris.endPathX == 30 :
            tempVal = 1
        pygame.draw.rect(Tetris.screen, Tetris.colors[Tetris.missionColor], pygame.Rect(((Tetris.endPathX + tempVal) * 20) + 280, ((Tetris.endPathY - tempVal)* 20), 20, 20))
        # mission 경로 이미지 출력(각 호선별로 위치에 따라 다르게 출력)
        Tetris.insertImgPosition(Tetris.startPathX, Tetris.startPathY, Tetris.missionStartImg)
        Tetris.insertImgPosition((Tetris.endPathX + tempVal), (Tetris.endPathY - tempVal), Tetris.missionEndImg)

    moveLeftCnt = 0
    moveRightCnt = 0
    oldval = [False, False, False, False, False] # 이전 키 입력
    # key값 에 따른 움직임 함수
    def movePlay() :
        if Tetris.keys[2] and Tetris.blockX > 300 and Tetris.checkMoveL:
            Tetris.moveLeftCnt += 1
            if Tetris.moveLeftCnt == 10000 :
                Tetris.blockX -= 20
                Tetris.moveLeftCnt = 0
        elif Tetris.keys[3] and Tetris.blockX < 900 and Tetris.checkMoveR:
            Tetris.moveRightCnt += 1
            if Tetris.moveRightCnt == 10000 :
                Tetris.blockX += 20
                Tetris.moveRightCnt = 0
        elif Tetris.oldval[0] != Tetris.keys[0] : # 이전 입력과 현재입력이 다를때(중복실행 방지)
            Tetris.oldval = Tetris.keys
            Tetris.changeBlockShape = (Tetris.changeBlockShape + 1) % 4
        elif Tetris.oldval[1] != Tetris.keys[1] :  # 이전 입력과 현재입력이 다를때(중복실행 방지)
            Tetris.oldval = Tetris.keys
            Tetris.blockTimer1 = 1
            Tetris.fastDownFlag = 1
        elif Tetris.keys[4] :
            Tetris.missionClearEvent()

    # key 입력 이벤트 처리 함수
    @staticmethod
    def keyeEventProcess() :
        # loop through the events
        for event in pygame.event.get():
            # key가 눌렸을때
            if event.type == pygame.KEYDOWN:
                Tetris.keys= [event.key == K_UP and Tetris.blockX < 840, event.key == K_DOWN,
                              event.key == K_LEFT, event.key == K_RIGHT, event.key == K_SPACE]
                pygame.mixer.Sound.play(Tetris.btnSound)
            # key가 떨어졌을때
            if event.type == pygame.KEYUP:
                for i in range(0, 5) :
                    Tetris.keys[i] = False
            # if it is quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Tetris.movePlay()

    # map의 내용을 update 해주는 함수
    def updateMap(self) :
        Tetris.checkMoveL = Tetris.checkMoveR = 1
        for i in range(3, 0, -1) :
            yBlock = Tetris.nowBlockShape[(Tetris.changeBlockShape * 4) + i]
            # map에 블럭이 내려올때 바로 아래단에 블럭이 차있는지 확인 or 바닥에 닿았을 경우
            for j, tBlock in enumerate(yBlock) :
                if ((tBlock == 1 and Tetris.Map[int(Tetris.blockY / 20) + i + 1][int((Tetris.blockX - 300) / 20) + j] >= 1)
                        or (Tetris.blockY + 60 == ((Tetris.mapRangeY - 1) * 20) - 20)) :
                    # 미션 실패(더 이상 내려올 곳이 없을때)
                    if Tetris.blockY == 0 :
                        Tetris.screen.blit(Tetris.missionFailImg, (315, 250))
                        Tetris.showPlayTime()
                        Tetris.drawText(598, 345, str(Tetris.stageLevel + 1), 30)
                        pygame.display.flip()
                        if Tetris.stageLevel > 0 :
                            self.sendDataToServer = 1
                        self.gameSequence = 0
                        time.sleep(1)
                    Tetris.copyBlockToMap()
                    Tetris.blockX = 580
                    Tetris.blockY = 0
                # 블럭이 좌, 우로 이동 가능한지 체크
                if tBlock == 1 and Tetris.Map[int(Tetris.blockY / 20) + i][int((Tetris.blockX - 300) / 20) + j - 1] >= 1 :
                    Tetris.checkMoveL = 0
                if tBlock == 1 and Tetris.Map[int(Tetris.blockY / 20) + i][int((Tetris.blockX - 300) / 20) + j + 1] >= 1 :
                    Tetris.checkMoveR = 0
        # 블럭 아래로 한칸씩 내리기
        if Tetris.blockY < ((Tetris.mapRangeY - 1) * 20) - 80 :
            if Tetris.fastDownFlag == 0 :
                Tetris.blockY += 1
            else :
                Tetris.blockY -= (Tetris.blockY % 10) # 20의 배수에서 checkFillBlock()을 실행하기 때문에
                Tetris.blockY += 10

    # 한 라인이 꽊찼는지 확인하는 함수
    def checkFillBlock(self) :
        for i in range(Tetris.mapRangeY - 2, 0, -1) :
            yMap = Tetris.Map[i]
            checkLine = 0
            for xMap in yMap : # 라인 체크
                if xMap >= 1 :
                    checkLine += 1
            if checkLine >= 31 : # 라인이 한줄 꽉찰경우
                for t in range(i, 1, -1) :
                    for k in range(0, 31) :
                        Tetris.Map[t][k] = Tetris.Map[t - 1][k]
                        Tetris.Map[0][k] = 0
            checkLine = 0

    # 버튼 클릭 함수 (startX, startY, endX, endY (버튼 클릭 범위))
    def clickButton(self) :
        result = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 588 >= pos[1] >= 380 :
                    indx = [(522 >= pos[0] >= 465),(643 >= pos[0] >= 586), (772 >= pos[0] >= 715)]
                    for i, _indx in enumerate(indx) :
                        if _indx :
                            result = i + 1
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        return result

    # 버튼 선택 효과 보여주는 함수 들
    def _buildStartImage(x,y,z):
        if x:
            Tetris.screen.blit(Tetris.smallStartImg, (455, 380))
        for _img, _pos in [(Tetris.smallStartImg, (455, 380)), (Tetris.smallEndImg, (715, 380)),(Tetris.smallDescriptionImg, (586, 380))]:
            Tetris.screen.blit(_img, _pos)

    def _play_btn_sound(flag):
        if not flag:
            pygame.mixer.Sound.play(Tetris.btnSound)
        return True

    btnSoundflag = False
    @staticmethod
    def effectMenueBtn() :
        pos = pygame.mouse.get_pos()
        x_inx =[ 522 >= pos[0] >= 455 , 643 >= pos[0] >= 586,  772 >= pos[0] >= 715 ]
        b_mapped = zip(x_inx , [(Tetris.bigStartImg, (445, 340)), (Tetris.bigDescriptionImg, (576, 340)), (Tetris.bigEndImg, (705, 340) )])
        s_mapped = [(Tetris.smallStartImg, (455, 380)), (Tetris.smallEndImg, (715, 380)), (Tetris.smallDescriptionImg, (586, 380))]

        for k in s_mapped :
            Tetris.screen.blit(k[0], k[1])

        if 588 >= pos[1] >= 380 :
            if True in x_inx :
                Tetris.btnSoundflag = Tetris._play_btn_sound(Tetris.btnSoundflag)
            else:
                Tetris.btnSoundflag = False
            for j, k in b_mapped:
                if j :
                    Tetris.screen.blit(k[0], k[1])
        else:
            Tetris.btnSoundflag = False

    # description 페이지 관련 메소드(사용자 정보 입력 등)
    gameID = ['d','e','f','a','u','l','t']
    def inputInform(self) :
        tmpChar  = ''
        Tetris.drawText(390, 635, ''.join(Tetris.gameID), 27)
        for event in pygame.event.get():
            # 키보드 눌렀을때
            if event.type == pygame.KEYDOWN:
                inputKey = [K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m,
                            K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z]
                if len(Tetris.gameID) < 25 :
                    for i, inputChar in enumerate(inputKey) :
                        if event.key == inputChar :
                            tmpChar = ord('a') + i  # 아스키값
                            Tetris.gameID.append(chr(tmpChar))  # 아스키값을 char값으로 변환
                    if event.key == K_SPACE :
                        Tetris.gameID.append(' ')
                if event.key == K_BACKSPACE and len(Tetris.gameID) > 0 :
                    Tetris.gameID.pop()
            # 마우스 클릭
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (1065 >= pos[0] >= 865) and (165 >= pos[1] >= 90) :
                    self.gameSequence = 0
            # 게임 끝내기
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    #게임 데이터 서버로 전송
    @staticmethod
    def sendGameData() :
        tName = ''.join(Tetris.gameID)
        tgameScore = Tetris.resultScore
        tgameTime = str(datetime.datetime.now())
        tIntroduction = '게임시간 : ' + tgameTime + Tetris.gameClearMessage
        data = {"secret_key" : '시크릿키', "name" : tName, "introduction" : tIntroduction,
                "gamescore" : tgameScore, "gamelevel" : Tetris.stageLevel ,"gametime" : Tetris.resultTime, "emailladdress" : 'default'}

        try :
            res = requests.post(Tetris.url, data = data, timeout = 1)
        # 서버가 실행되고 있지 않을때 예외처리
        except :
            res = None

        Tetris.resultScore = 0
        Tetris.stageLevel = 0
        Tetris.resultTime = 0

    @staticmethod
    def viewTimer() :
        print(str(datetime.datetime.now()))
        timer = threading.Timer(1, Tetris.viewTimer)

    # 스테이지 별로 맵 바꿔주는 함수(리팩토링 예정)
    def stageChange(level) :
        for i in range(0, Tetris.mapRangeY) :
            Tetris.Map[i][30] = 88
        if level == 0 :
            for i in range(0, 28) :
                Tetris.Map[39][i] = 4
                Tetris.Map[38][i] = 3
                Tetris.Map[35][i] = 2
                Tetris.Map[34][i] = 1
            for i in range(2,29) :
                Tetris.Map[37][i] = 6
                Tetris.Map[36][i] = 5
                Tetris.Map[33][i] = 4
                Tetris.Map[32][i] = 3
        elif level == 1 :
            for i in range(25, 40) :
                Tetris.Map[i][15] = 5
                Tetris.Map[i][14] = 5
            for i in range(30, 40) :
                Tetris.Map[i][16] = 4
                Tetris.Map[i][13] = 4
            for i in range(35, 40) :
                Tetris.Map[i][17] = 3
                Tetris.Map[i][12] = 3
            for i in range(35, 40) :
                Tetris.Map[i][0] = 6
                Tetris.Map[i][1] = 6
                Tetris.Map[i][28] = 6
                Tetris.Map[i][29] = 6
        elif level == 2 :
            for i in range(0, 20) :
                Tetris.Map[39][i] = 4
                Tetris.Map[38][i] = 3
                Tetris.Map[37][i] = 2
                Tetris.Map[36][i] = 1
            for i in range(18,29) :
                Tetris.Map[35][i] = 6
                Tetris.Map[34][i] = 5
                Tetris.Map[33][i] = 4
                Tetris.Map[32][i] = 3
        elif level == 3 :
            for i in range(20, 40) :
                if i % 2 == 0 :
                    for j in range(1, 29) :
                        Tetris.Map[i][j] = random.randint(1, 6)
                else :
                    for j in range(0, 28) :
                        Tetris.Map[i][j] = random.randint(1, 6)
