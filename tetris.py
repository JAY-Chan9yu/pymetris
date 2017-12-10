# 1 - Import library
import pygame
from pygame.locals import *
import math
import random
import blocklib

class tetris :
    # load images
    block = pygame.image.load("tetrisResource/image/block.jpg")
    width, height = 1200, 820
    screen=pygame.display.set_mode((width, height))

    mapRangeX, mapRangeY = 33, 41

    keys = [0, 0, 0, 0, 0]              # key 값 판단하는 리스트

    # colorvlue list
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    PURPLE = (126, 30, 156)
    BROWN = (101, 55, 0)
    ORANGE = (249, 115, 6)

    #블록데이터 구조 설정
    b1 = { 'rect':pygame.Rect(300,80,50,100), 'color':RED}
    b2 = { 'rect':pygame.Rect(200,200,20,20), 'color':GREEN}
    b3 = { 'rect':pygame.Rect(100,150,60,60), 'color':BLUE}
    blocks = [b1,b2,b3]

    # 블럭이 없으면 0, 있으면 1 <- 여기서 랜덤으로 2~5의 값을 주어 1이면 블럭의 색값을 부여한다.
    colors = [BLACK, BLUE, GREEN, ORANGE, BLUE, PURPLE, BROWN]

    missionClearEventFlag = 0           # mission clear 이벤틀 플래그
    blockTimer = 5000                   # 게임 스피드
    blockTimer1 = 5000
    changeBlockShape = 0                # 블럭의 모양을 변경하는 변수
    nowBlockShape = blocklib.block1     # 현재 나오는 블럭의 모양
    nextBlockShape = blocklib.block1    # 다음 블럭
    blockColor = ORANGE                 # 블럭 색상
    nextColor = BLUE                    # 다음 블럭 색상
    checkMoveR = 0
    checkMoveL = 0
    blockX = 500                        # 현재 나오는 블럭의 x,y 좌표
    blockY = 0
    missionColor = 3                    # 미션 컬러
    minPath = 999                       # 최단경로
    startPathX = 0                      # 미션 경로(시작과 끝)
    startPathY = 29
    endPathX = 10
    endPathY = 40
    Map = [[0] * 33 for row in range(41)]  # 20 x 20  30 * 20 = 600 픽셀

    # 생성자
    def __init__(self) :
        pass
        #self.map = [[0] * tetris.mapRangeX for row in range(tetris.mapRangeY)]

    # 블럭이 바닥에 닿거나 다른 블럭에 닿았을 경우 map에 copy하는 함수
    def copyBlockToMap() :
        for i in range(0, 4) :
            for j in range(0, 4) :
                # 지하철 노선에 따른 색깔
                tempColor = 0
                if tetris.blockColor == tetris.BLUE:
                    tempColor = 1
                elif tetris.blockColor == tetris.GREEN:
                    tempColor = 2
                elif tetris.blockColor == tetris.ORANGE :
                    tempColor = 3
                elif tetris.blockColor == tetris.BLUE :
                    tempColor = 4
                elif tetris.blockColor == tetris.PURPLE :
                    tempColor = 5
                elif tetris.blockColor == tetris.BROWN :
                    tempColor = 6

                if tetris.nowBlockShape[(tetris.changeBlockShape * 4) + i][j] >= 1 :
                    tetris.Map[int((tetris.blockY / 20) + i)][int(((tetris.blockX - 300) / 20) + j)] = tempColor

        tetris.blockTimer1 = 5000
        tetris.blockColor = tetris.nextColor
        tetris.nowBlockShape = tetris.nextBlockShape
        tetris.nextBlockShape = blocklib.randBlock(random.randint(0, 3))
        tetris.nextColor = tetris.colors[random.randint(1, 6)]

    # 지하철 노선 연결하는 미션 체크하는 함수
    def missionClearEvent() :
        tetris.dfsSerch(0, 30, 1)
        print("short path cnt : " + str(tetris.minPath))

    # 최단거리 탐색
    def dfsSerch(x, y, cnt) :
        if x == (tetris.endPathX - 1) and y == (tetris.endPathY - 1) :
            if cnt < tetris.minPath :
                tetris.minPath = cnt
            return

        tetris.Map[y][x] = 0

        print("x : " + str(x) + " y : " + str(y))
        if x > 0 and tetris.Map[y][x - 1] == tetris.missionColor : # Left
            tetris.dfsSerch(x - 1, y, cnt + 1)
        if x < tetris.mapRangeX - 3 and tetris.Map[y][x+1] == tetris.missionColor :
            tetris.dfsSerch(x + 1, y, cnt + 1)
        if y > 0 and tetris.Map[y - 1][x] == tetris.missionColor :
            tetris.dfsSerch(x, y - 1, cnt + 1)
        if y < tetris.mapRangeY - 1 and tetris.Map[y + 1][x] == tetris.missionColor : # Down
            tetris.dfsSerch(x, y + 1, cnt + 1)
        # 원상 복귀
        tetris.Map[y][x] = tetris.missionColor

    # key값 에 따른 움직임 함수
    def movePlay() :
        if tetris.keys[2] == 2 :
            tetris.blockX -= 20
            tetris.keys[2] = 0
        elif tetris.keys[3] == 2 :
            tetris.blockX += 20
            tetris.keys[3] = 0
        elif tetris.keys[0] == 2 :
            tetris.changeBlockShape += 1
            if tetris.changeBlockShape >= 4 :
                tetris.changeBlockShape = 0
            tetris.keys[0] = 0
        elif tetris.keys[1] == 2 :
            tetris.blockTimer1 = 5
            tetris.keys[1] = 0
        elif tetris.keys[4] == 2 :
            tetris.missionClearEventFlag = 1
            tetris.missionClearEvent()
            tetris.keys[4] = 0

    # block 모양을 그리는 함수
    def drawBlock(shape, color, x, y) :
        for i in range(0, 4) :
            tBlock = shape
            yBlock = tBlock[(tetris.changeBlockShape * 4) + i]
            tempX = x
            tempY = y + (20 * i)
            for j, xBlock  in enumerate(yBlock) :
                if xBlock >= 1 :
                    pygame.draw.rect(tetris.screen, color, pygame.Rect(tempX, tempY, 20, 20))
                tempX += 20

    # map을 화면에서 볼수 있도록 그려주는 함수
    def drawMap() :
        # draw map.
        for i, yMap in enumerate(tetris.Map) :
            tempX = 300
            tempY = 20 * i
            for j, xMap  in enumerate(yMap) :
                tempColor = 0
                # 지하철 노선에 따른 색깔
                if xMap == 1:
                    tempColor = tetris.colors[1]
                elif xMap == 2:
                    tempColor = tetris.colors[2]
                elif xMap == 3 :
                    tempColor = tetris.colors[3]
                elif xMap == 4 :
                    tempColor = tetris.colors[4]
                elif xMap == 5 :
                    tempColor = tetris.colors[5]
                elif xMap == 6 :
                    tempColor = tetris.colors[6]

                if xMap >= 1 :
                    #pygame.draw.rect(screen, colors[random.randint(0,4)], pygame.Rect(tempX, tempY, 20, 20))
                    pygame.draw.rect(tetris.screen, tempColor, pygame.Rect(tempX, tempY, 20, 20))
                tempX += 20

    # 게임과 관계 없는 화면에 배경을 그려주는 함수
    def drawBackbround() :
        tempN = 0
        for i in range(0, 2) :
            tempW = 280
            if i == 1 :
                tempW = 900
            tempN = 0
            for j in range(0, tetris.mapRangeY) :
                tetris.screen.blit(tetris.block, (tempW, tempN))
                tempN += 20
        tempN = 280
        for i in range(0, tetris.mapRangeX - 2) :
            tetris.screen.blit(tetris.block, (tempN, (tetris.mapRangeY - 1) * 20))
            tempN += 20
        pygame.draw.rect(tetris.screen, tetris.ORANGE, pygame.Rect((tetris.startPathX * 20) + 280, (tetris.startPathY * 20), 20, 20))
        pygame.draw.rect(tetris.screen, tetris.ORANGE, pygame.Rect((tetris.endPathX * 20) + 280, (tetris.endPathY * 20), 20, 20))

    # key 입력 이벤트 처리 함수
    def keyeEventProcess() :
        # loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.KEYDOWN: # key가 눌렸을때
                if event.key == K_UP:
                    tetris.keys[0] = 1
                elif event.key == K_DOWN:
                    tetris.keys[1] = 1
                elif event.key == K_LEFT and tetris.blockX > 300 and tetris.checkMoveL == 1:
                    tetris.keys[2] = 1
                elif event.key == K_RIGHT and tetris.blockX < 900 and tetris.checkMoveR == 1:
                    tetris.keys[3] = 1
                elif event.key == K_SPACE :
                    tetris.keys[4] = 1

            if event.type==pygame.KEYUP: # key가 떨어졌을때
                if tetris.keys[0] == 1 and event.key == K_UP:
                    tetris.keys[0] = 2
                elif tetris.keys[1] == 1 and event.key == K_DOWN:
                    tetris.keys[1] = 2
                elif tetris.keys[2] == 1 and event.key == K_LEFT:
                    tetris.keys[2] = 2
                elif tetris.keys[3] == 1 and event.key == K_RIGHT:
                    tetris.keys[3] = 2
                elif tetris.keys[4] == 1 and event.key == K_SPACE :
                    tetris.keys[4] = 2

            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
        tetris.movePlay()

    # map의 내용을 update 해주는 함수
    def updateMap() :
        tetris.checkMoveL = tetris.checkMoveR = 1
        for i in range(3, 0, -1) :
            yBlock = tetris.nowBlockShape[(tetris.changeBlockShape * 4) + i]
            # map에 블럭이 내려올때 바로 아래단에 블럭이 차있는지 확인 or 바닥에 닿았을 경우
            for j, tBlock in enumerate(yBlock) :
                if ((tBlock == 1 and tetris.Map[int(tetris.blockY / 20) + i + 1][int((tetris.blockX - 300) / 20) + j] >= 1)
                        or (tetris.blockY + 60 == ((tetris.mapRangeY - 1) * 20) - 20)) :
                    tetris.copyBlockToMap()
                    tetris.blockX = 500
                    tetris.blockY = 0
                # 블럭이 좌, 우로 이동 가능한지 체크
                if (tBlock == 1 and tetris.Map[int(tetris.blockY / 20) + i][int((tetris.blockX - 300) / 20) + j - 1] >= 1) :
                    tetris.checkMoveL = 0
                if (tBlock == 1 and tetris.Map[int(tetris.blockY / 20) + i][int((tetris.blockX - 300) / 20) + j + 1] >= 1) :
                    tetris.checkMoveR = 0

    # 한 라인이 꽊찼는지 확인하는 함수
    def checkFillBlock() :
        for i in range(tetris.mapRangeY - 2, 0, -1) :
            yMap = tetris.Map[i]
            checkLine = 0
            for xMap in yMap : # 라인 체크
                if xMap >= 1 :
                    checkLine += 1
            if checkLine >= 31 : # 라인이 한줄 꽉찰경우
                for t in range(tetris.mapRangeY - 2, 1, -1) :
                    for k in range(0, 31) :
                        tetris.Map[t][k] = tetris.Map[t - 1][k]
                    for k in range(0, 31) :
                        tetris.Map[0][k] = 0
                checkLine = 0
