# 1 - Import library
import pygame
from pygame.locals import *
import math
import random
import blocklib

class tetris(object) :
    # load images
    block = pygame.image.load("tetrisResource/image/block.jpg")
    missionStartImg = pygame.image.load("tetrisResource/image/Metro4_start.png")
    missionEndImg = pygame.image.load("tetrisResource/image/Metro4_end.png")
    background = pygame.image.load("tetrisResource/image/background.jpg")
    initBackground = pygame.image.load("tetrisResource/image/init_background.jpg")
    #descriptionBackground = pygame.image.load("tetrisResource/image/background.jpg")
    previewBlockImg = pygame.image.load("tetrisResource/image/previewBlock.png")
    # 버튼 이미지
    bigStartImg =pygame.image.load("tetrisResource/image/bigStart.png")
    smallStartImg =pygame.image.load("tetrisResource/image/smallStart.png")
    bigEndImg =pygame.image.load("tetrisResource/image/bigEnd.png")
    smallEndImg =pygame.image.load("tetrisResource/image/smallEnd.png")
    bigDescriptionImg =pygame.image.load("tetrisResource/image/bigDescription.png")
    smallDescriptionImg =pygame.image.load("tetrisResource/image/smallDescription.png")


    width, height = 1200, 900           # screen width, height
    screen = pygame.display.set_mode((width, height))

    mapRangeX, mapRangeY = 33, 41       # 스테이지 length

    # colorvlue list
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (77, 169, 225)
    NAVY = (21, 41, 116)
    WHITE = (255, 255, 255)
    PURPLE = (126, 30, 156)
    BROWN = (101, 55, 0)
    ORANGE = (249, 115, 6)

    # 블럭이 없으면 0, 있으면 1 <- 여기서 랜덤으로 2~5의 값을 주어 1이면 블럭의 색값을 부여한다.
    colors = [BLACK, NAVY, GREEN, ORANGE, BLUE, PURPLE, BROWN]
    metroImgs = ["Metro1_start" ,"Metro2_start", "Metro3_start" ,"Metro4_start", "Metro5_start" ,"Metro6_start",
                 "Metro1_end" ,"Metro2_end", "Metro3_end" ,"Metro4_end", "Metro5_end" ,"Metro6_end",]

    stageLevel = 1                      # 게임 스테이지

    blockTimer = 5000                   # 게임 스피드
    blockTimer1 = 5000

    keys = [0, 0, 0, 0, 0]              # key 값 판단하는 리스트

    Map = []                            # 블럭 1개 = 20 x 20

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
    missionColor = 4                    # 미션 컬러
    minPath = 999                       # 최단경로
    minPathLocation = []                # 최단경로 좌표
    saveLocation = 0                    # 최단경로 좌표 저장 승인 플래그
    startPathX = 0                      # 미션 경로(시작과 끝)
    startPathY = 27
    endPathX = 15
    endPathY = 40

    fastDownFlag = 0                    # 블럭 빨리 내리기

    # 생성자
    def __init__(self) :
        # 블럭 초기화
        tetris.Map = [[0] * tetris.mapRangeX for row in range(tetris.mapRangeY)]
        #self.gameInit()

    # 게임 초기 설정
    def gameInit(self) :
        tetris.nextBlockShape = blocklib.randBlock(random.randint(0, 3))
        tetris.stageChange(tetris.stageLevel)
        # game 배경화면
        tetris.screen.blit(tetris.background, (0, 0))
        pygame.draw.rect(tetris.screen, tetris.BLACK, pygame.Rect(300, 0, 600, 800))
        pygame.display.flip()

    # map 초기화
    def mapInit() :
        tetris.blockTimer1 = 5000
        tetris.blockColor = tetris.nextColor
        tetris.nowBlockShape = tetris.nextBlockShape
        tetris.nextBlockShape = blocklib.randBlock(random.randint(0, 3))
        tetris.nextColor = tetris.colors[random.randint(1, 6)]
        tetris.fastDownFlag = 0

    # 블럭이 바닥에 닿거나 다른 블럭에 닿았을 경우 map에 copy하는 함수
    def copyBlockToMap() :
        for i in range(0, 4) :
            for j in range(0, 4) :
                # 지하철 노선에 따른 색깔
                tempColor = 0
                if tetris.blockColor == tetris.NAVY:
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
        tetris.mapInit()

    def gameClearEvent() :
        pass

    # mission cleear 했다는 이미지 띄우고 3초 뒤에 다음스테이지로 넘어가게 함
    def drawMissionClearEvent(self) :
        for i in range(0, 3) :
            time.sleep(1)

    # 지하철 노선 연결하는 미션 체크하는 함수
    def missionClearEvent() :
        tetris.dfsSerch(tetris.startPathX, tetris.startPathY, 1)
        print("short path cnt : " + str(tetris.minPath))
        # 최단경로 나왔을경우  변수 및 화면 초기화
        if tetris.minPath < 999 :
            # 최단경로 표시
            for i in tetris.minPathLocation :
                tetris.screen.blit(tetris.previewBlockImg, ((i[1] * 20) + 300, (i[0] * 20)))
                print(str(i[0]) + " " + str(i[1]))
            tetris.minPath = 0
            tetris.stageLevel += 1
            # game clear 했을 경우
            if tetris.stageLevel > 4 :
                tetris.gameClearFlag = 1
                tetris.gameClearEvent()
            tetris.missionColor = random.randint(1, 6)
            tetris.startPathX = blocklib.stageLevel[tetris.stageLevel][0]
            tetris.startPathY = blocklib.stageLevel[tetris.stageLevel][1]
            tetris.endPathX = blocklib.stageLevel[tetris.stageLevel][2]
            tetris.endPathY = blocklib.stageLevel[tetris.stageLevel][3]
            tetris.missionStartImg = pygame.image.load("tetrisResource/image/" + tetris.metroImgs[tetris.missionColor - 1] + ".png")
            tetris.missionEndImg = pygame.image.load("tetrisResource/image/" + tetris.metroImgs[(tetris.missionColor - 1) + 6] +".png")
            tetris.missionClearEventFlag = 1
            tetris.Map.clear()
            tetris.Map = [[0] * tetris.mapRangeX for row in range(tetris.mapRangeY)]
            tetris.screen.blit(tetris.background, (0, 0))
            tetris.gameInit()


    # 최단거리 탐색(DFS)
    def dfsSerch(x, y, cnt) :
        if x == tetris.endPathX - 1 and y == tetris.endPathY - 1 :
            if cnt < tetris.minPath :
                tetris.minPath = cnt
                tetris.minPathLocation.clear()
                tetris.saveLocation = 1
            return
        elif x == tetris.endPathX and y == tetris.endPathY - 1 :
            tetris.saveLocation = 0


        tempMap = tetris.Map[y][x]
        tetris.Map[y][x] = 0
        #print("x : " + str(x) + " y : " + str(y))
        if x > 0 and tetris.Map[y][x - 1] == tetris.missionColor : # Left
            tetris.dfsSerch(x - 1, y, cnt + 1)
        if x < tetris.mapRangeX - 3 and tetris.Map[y][x + 1] == tetris.missionColor : #Right
            tetris.dfsSerch(x + 1, y, cnt + 1)
        if y > 0 and tetris.Map[y - 1][x] == tetris.missionColor : # Up
            tetris.dfsSerch(x, y - 1, cnt + 1)
        if y < tetris.mapRangeY - 1 and tetris.Map[y + 1][x] == tetris.missionColor : # Down
            tetris.dfsSerch(x, y + 1, cnt + 1)

        # 원상 복귀
        #print("pop 좌표 : " + str(y) + " " + str(x))
        #tetris.minPathLocation.pop()
        if tetris.saveLocation == 1 :
            tetris.minPathLocation.append([y, x])

        tetris.Map[y][x] = tempMap

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
            tetris.blockTimer1 = 1
            tetris.fastDownFlag = 1
            tetris.keys[1] = 0
        elif tetris.keys[4] == 2 :
            tetris.missionClearEvent()
            tetris.keys[4] = 0

    # 맵 하단에 블럭의 위치 미리보기 해주는 기능
    def drawPreviewBlock(self) :
        for k in range(int(tetris.blockY / 20), 37) :
            for i in range(3, 0, -1) :
                yBlock = tetris.nowBlockShape[(tetris.changeBlockShape * 4) + i]
                for j, xBlock in enumerate(yBlock):
                    if ((xBlock >= 1 and tetris.Map[k + i + 1][int((tetris.blockX - 300) / 20) + j] >= 1)
                            or (k + 3 == tetris.mapRangeY - 2)) :
                        previewY = k + 3
                        self.drawBlock(1, tetris.nowBlockShape, tetris.WHITE, tetris.blockX, (previewY * 20) - 60)
                        return


    # block 모양을 그리는 함수
    def drawBlock(self, choiceBlkOrImg, shape, color, x, y) :
        for i in range(0, 4) :
            tBlock = shape
            yBlock = tBlock[(tetris.changeBlockShape * 4) + i]
            tempX = x
            tempY = y + (20 * i)
            for j, xBlock  in enumerate(yBlock) :
                if xBlock >= 1 :
                    # 블럭을 출력할 것인지 이미지를 출력할 것인지
                    if choiceBlkOrImg == 0 :
                        pygame.draw.rect(tetris.screen, color, pygame.Rect(tempX, tempY, 20, 20))
                    else :
                        tetris.screen.blit(tetris.previewBlockImg, (tempX, tempY))
                tempX += 20

    # map을 화면에서 볼수 있도록 그려주는 함수
    def drawMap(self) :
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

                if xMap >= 1 and j < 30:
                    #pygame.draw.rect(screen, colors[random.randint(0,4)], pygame.Rect(tempX, tempY, 20, 20))
                    pygame.draw.rect(tetris.screen, tempColor, pygame.Rect(tempX, tempY, 20, 20))
                tempX += 20

    # 게임과 관계 없는 화면에 배경을 그려주는 함수
    def drawBackbround(self) :
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
            if i < 6 :
                tetris.screen.blit(tetris.block, (920 + (i * 20), 100))
                tetris.screen.blit(tetris.block, (1020, (i * 20)))

        pygame.draw.rect(tetris.screen, tetris.BLACK, pygame.Rect(920,0, 100, 100))
        # mission start, end  표시
        pygame.draw.rect(tetris.screen, tetris.colors[tetris.missionColor], pygame.Rect((tetris.startPathX * 20) + 280, (tetris.startPathY * 20), 20, 20))
        pygame.draw.rect(tetris.screen, tetris.colors[tetris.missionColor], pygame.Rect((tetris.endPathX * 20) + 280, (tetris.endPathY * 20), 20, 20))

        # mission 경로 이미지 출력(각 호선별로 위치에 따라 다르게 출력)
        if tetris.startPathX == 0 :
            tetris.screen.blit(tetris.missionStartImg, ((tetris.startPathX * 20) + 200 , (tetris.startPathY * 20) - 20))
        elif tetris.startPathX > 0 and tetris.startPathX < 30:
            tetris.screen.blit(tetris.missionStartImg, ((tetris.startPathX * 20) + 260 , (tetris.startPathY * 20) + 20))
        elif tetris.startPathX == 31 :
            tetris.screen.blit(tetris.missionStartImg, ((tetris.startPathX * 20) + 300 , (tetris.startPathY * 20) - 20))

        if tetris.endPathX == 0 :
            tetris.screen.blit(tetris.missionEndImg, ((tetris.endPathX * 20) + 200 , (tetris.endPathY * 20) - 20))
        elif tetris.endPathX > 0 and tetris.endPathX < 30:
            tetris.screen.blit(tetris.missionEndImg, ((tetris.endPathX * 20) + 260 , (tetris.endPathY * 20) + 20))
        elif tetris.endPathX == 31 :
            tetris.screen.blit(tetris.missionEndImg, ((tetris.endPathX * 20) + 300 , (tetris.endPathY * 20) - 20))

    # key 입력 이벤트 처리 함수
    def keyeEventProcess(self) :
        # loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type == pygame.KEYDOWN: # key가 눌렸을때
                if event.key == K_UP and tetris.blockX < 840:
                    tetris.keys[0] = 1
                elif event.key == K_DOWN:
                    tetris.keys[1] = 1
                elif event.key == K_LEFT and tetris.blockX > 300 and tetris.checkMoveL == 1:
                    tetris.keys[2] = 1
                elif event.key == K_RIGHT and tetris.blockX < 900 and tetris.checkMoveR == 1:
                    tetris.keys[3] = 1
                elif event.key == K_SPACE :
                    tetris.keys[4] = 1

            if event.type == pygame.KEYUP: # key가 떨어졌을때
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

            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
        tetris.movePlay()

    # map의 내용을 update 해주는 함수
    def updateMap(self) :
        self.nowBlockShape = tetris.nowBlockShape
        self.nextBlockShape = tetris.nextBlockShape
        self.blockColor = tetris.blockColor
        self.nextColor = tetris.nextColor

        tetris.checkMoveL = tetris.checkMoveR = 1

        # 화면 지우기
        #pygame.draw.rect(tetris.screen, tetris.BLACK, pygame.Rect(300, 0, 600, 800)

        for i in range(3, 0, -1) :
            yBlock = tetris.nowBlockShape[(tetris.changeBlockShape * 4) + i]
            # map에 블럭이 내려올때 바로 아래단에 블럭이 차있는지 확인 or 바닥에 닿았을 경우
            for j, tBlock in enumerate(yBlock) :
                #print(str(tBlock) + " " + str(tetris.blockY + 60) + " " + str(((tetris.mapRangeY - 1) * 20) - 20))
                if ((tBlock == 1 and tetris.Map[int(tetris.blockY / 20) + i + 1][int((tetris.blockX - 300) / 20) + j] >= 1)
                        or (tetris.blockY + 60 == ((tetris.mapRangeY - 1) * 20) - 20)) :
                    tetris.copyBlockToMap()
                    tetris.blockX = 580
                    tetris.blockY = 0
                # 블럭이 좌, 우로 이동 가능한지 체크
                if (tBlock == 1 and tetris.Map[int(tetris.blockY / 20) + i][int((tetris.blockX - 300) / 20) + j - 1] >= 1) :
                    tetris.checkMoveL = 0
                if (tBlock == 1 and tetris.Map[int(tetris.blockY / 20) + i][int((tetris.blockX - 300) / 20) + j + 1] >= 1) :
                    tetris.checkMoveR = 0

        # 블럭 아래로 한칸씩 내리기
        if tetris.blockY < ((tetris.mapRangeY - 1) * 20) - 80 :
            if tetris.fastDownFlag == 0 :
                tetris.blockY += 1
            else :
                tetris.blockY -= (tetris.blockY % 5) # 20의 배수에서 checkFillBlock()을 실행하기 때문에
                tetris.blockY += 5

    # 한 라인이 꽊찼는지 확인하는 함수
    def checkFillBlock(self) :
        for i in range(tetris.mapRangeY - 2, 0, -1) :
            yMap = tetris.Map[i]
            checkLine = 0
            for xMap in yMap : # 라인 체크
                if xMap >= 1 :
                    checkLine += 1
            if checkLine >= 31 : # 라인이 한줄 꽉찰경우
                for t in range(i, 1, -1) :
                    for k in range(0, 31) :
                        tetris.Map[t][k] = tetris.Map[t - 1][k]
                    for k in range(0, 31) :
                        tetris.Map[0][k] = 0
            checkLine = 0

    # 버튼 클릭 함수 (startX, startY, endX, endY (버튼 클릭 범위))
    def clickButton(self) :
        result = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] >= 465 and pos[0] <= 522) and ((pos[1] >= 380 and pos[1] <= 588)) :
                    result = 1
                elif (pos[0] >= 586 and pos[0] <= 643) and ((pos[1] >= 380 and pos[1] <= 588)) :
                    result = 2
                elif (pos[0] >= 715 and pos[0] <= 772) and ((pos[1] >= 380 and pos[1] <= 588)) :
                    result = 3
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        return result

    def stageChange(level) :
        for i in range(0, tetris.mapRangeY) :
            tetris.Map[i][30] = 88
        if level == 1 :
            for i in range(0, 27) :
                tetris.Map[39][i] = 4
                tetris.Map[38][i] = 3
                tetris.Map[35][i] = 2
                tetris.Map[34][i] =  1
            for i in range(2,29) :
                tetris.Map[37][i] = 6
                tetris.Map[36][i] = 5
                tetris.Map[33][i] = 4
                tetris.Map[32][i] = 3
        elif level == 2 :
            for i in range(25, 40) :
                tetris.Map[i][15] = 5
                tetris.Map[i][14] = 5
            for i in range(30, 40) :
                tetris.Map[i][16] = 4
                tetris.Map[i][13] = 4
            for i in range(35, 40) :
                tetris.Map[i][17] = 3
                tetris.Map[i][12] = 3
            for i in range(35, 40) :
                tetris.Map[i][0] = 6
                tetris.Map[i][1] = 6
                tetris.Map[i][28] = 6
                tetris.Map[i][29] = 6
        elif level == 3 :
            for i in range(0, 12) :
                tetris.Map[39][i] = 4
                tetris.Map[38][i] = 3
                tetris.Map[35][i] = 2
                tetris.Map[34][i] =  1
            for i in range(17,30) :
                tetris.Map[37][i] = 6
                tetris.Map[36][i] = 5
                tetris.Map[33][i] = 4
                tetris.Map[32][i] = 3
            for i in range(27, 40) :
                tetris.Map[i][14] = 5
                tetris.Map[i][13] = 5
        elif level == 4 :
            for i in range(20, 40) :
                if i % 2 == 0 :
                    for j in range(1, 29) :
                        tetris.Map[i][j] = random.randint(1, 6)
                else :
                    for j in range(0, 28) :
                        tetris.Map[i][j] = random.randint(1, 6)
