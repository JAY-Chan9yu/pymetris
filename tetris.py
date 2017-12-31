# 1 - Import library
import pygame
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
class tetris(object) :
    # 게임 결과(data)를 보낼 Server IP(local Test 중)
    #url = 'http://127.0.0.1:8000/'
    url = 'http://13.115.233.106/'
    # Load sounds
    btnSound = pygame.mixer.Sound("tetrisResource/audio/effect1.wav")
    # load images
    _image_load = lambda x: pygame.image.load("tetrisResource/image/%s"%x)
    # 블럭 관련 이미지
    block, line, missionStartImg, missionEndImg, missionClearImg, missionFailImg, previewBlockImg, gameClearImg = map(_image_load, [
        "block.jpg", "line.png", "Metro4_start.png", "Metro4_end.png", "missionClearImg.png","missionFailImg.png","previewBlock.png", "gameClearImg.png"])
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
    missionColor = 4                    # 미션 컬러
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

    # 생성자
    def __init__(self) :
        # 블럭 초기화
        tetris.Map = [[0] * tetris.mapRangeX for row in range(tetris.mapRangeY)]

    # 게임 초기 설정
    @staticmethod
    def gameInit() :
        tetris.mapInit()
        tetris.missionClearEventFlag = 0
        tetris.gameClearMessage = ''
        tetris.Map = [[0] * tetris.mapRangeX for row in range(tetris.mapRangeY)]
        tetris.nextBlockShape = blocklib.randBlock(random.randint(0, 3))
        tetris.stageChange(tetris.stageLevel)
        # 게임 시작 시간 저장
        tetris.gamePlayTime = time.time()
        # game 배경화면
        tetris.screen.blit(tetris.background, (0, 0))
        pygame.draw.rect(tetris.screen, tetris.BLACK, pygame.Rect(300, 0, 600, 800))
        #tetris.stageLevel = 0
        tetris.drawText(1050, 180,'스테이지 레벨 : '+ str(tetris.stageLevel + 1), 35)
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
                for idx,x in enumerate(tetris.colors):
                    if tetris.blockColor == x:
                        tempColor = idx
                if tetris.nowBlockShape[(tetris.changeBlockShape * 4) + i][j] >= 1 :
                    tetris.Map[int((tetris.blockY / 20) + i)][int(((tetris.blockX - 300) / 20) + j)] = tempColor
        tetris.mapInit()

    # 모든 스테이지를 끝냈을때
    gameClearMessage = ''
    def gameClearEvent(self) :
        if tetris.gameClearFlag :
            tetris.gameClearFlag = 0
            tetris.gameClearMessage = ' [* MVP *]'
            tetris.screen.blit(tetris.gameClearImg, (400, 250))
            pygame.display.flip()
            tetris.missionClearEventFlag = 1
            self.sendDataToServer = 1
            self.gameSequence = 0
            time.sleep(1)

    # 게임 플레이 시간 현시
    def showPlayTime() :
        # 첫 시간 - 현재시간 = 실행시간
        tmpTime = time.time() - tetris.gamePlayTime
        tmHour = tmpTime / 3600
        tmMin = (tmpTime % 3600) / 60
        tmSec = (tmpTime % 3600) % 60
        tetris.drawText(390, 425, str(floor(tmHour)) + ':' + str(floor(tmMin)) + ':' + str(floor(tmSec)), 30)

    # 지하철 노선 연결하는 미션 체크하는 함수
    def missionClearEvent() :
        tetris.dfsSerch(tetris.startPathX, tetris.startPathY, 1)
        # 최단경로 나왔을경우  변수 및 화면 초기화
        if tetris.minPath < 999 :
            # 최단경로 표시
            tetris.resultScore += tetris.minPath
            for i in tetris.minPathLocation :
                tetris.screen.blit(tetris.line, ((i[1] * 20) + 300, (i[0] * 20)))
            tetris.stageLevel += 1
            # game clear 했을 경우
            if tetris.stageLevel > 3 :
                tetris.gameClearFlag = 1
                #tetris.gameClearEvent()
            else :
                # 점수, 실행시간 표시
                tetris.screen.blit(tetris.missionClearImg, (315, 250))
                tetris.drawText(598, 345, str(tetris.stageLevel), 30)
                tetris.drawText(815, 425, str(tetris.minPath), 30)
                tetris.showPlayTime()
                pygame.display.flip()
                tetris.missionClearEventFlag = 1
                time.sleep(2)
            # Next mission Initialize
            tetris.minPath = 999
            tetris.missionColor = 4 #random.randint(1, 6)
            tetris.startPathX = blocklib.stageLevel[tetris.stageLevel][0]
            tetris.startPathY = blocklib.stageLevel[tetris.stageLevel][1]
            tetris.endPathX = blocklib.stageLevel[tetris.stageLevel][2]
            tetris.endPathY = blocklib.stageLevel[tetris.stageLevel][3]
            tetris.missionStartImg = tetris._image_load(tetris.metroImgs[tetris.missionColor - 1] + ".png")
            tetris.missionEndImg = tetris._image_load(tetris.metroImgs[(tetris.missionColor - 1) + 6] +".png")
            tetris.Map.clear()
            tetris.gameInit()

    # 최단거리 탐색(DFS)
    tempPath = []
    def dfsSerch(x, y, cnt) :
        # 최단거리 업데이트
        if tetris.Map[y][x] == tetris.missionColor :
            tetris.tempPath.append([y, x]) # 경로 추가
            if x == tetris.endPathX - 1 and y == tetris.endPathY - 1 :
                if cnt < tetris.minPath :
                    tetris.minPath = cnt
                    tetris.minPathLocation.clear()
                    tetris.minPathLocation = list(tetris.tempPath) # list 복사
            tempMap = tetris.Map[y][x]
            tetris.Map[y][x] = 0
            checkMapped = [x < tetris.mapRangeX - 3, y < tetris.mapRangeY - 1, y > 0, x > 0]
            gotoMapped = [(x + 1, y), (x, y + 1), (x, y - 1), (x - 1, y)]
            for i, _map in enumerate(checkMapped) :
                if _map :
                    tetris.dfsSerch(gotoMapped[i][0], gotoMapped[i][1], cnt + 1)

            tetris.tempPath.pop() # 이미 체크한 경로 삭제
            tetris.Map[y][x] = tempMap

    @staticmethod
    def drawText(x, y, text, size) :
        # text 만들기
        fontObj = pygame.font.Font('tetrisResource/font/BMYEONSUNG.ttf', size)
        textSurfaceObj = fontObj.render(text, True, tetris.BLACK)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x, y)
        tetris.screen.blit(textSurfaceObj, textRectObj)

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
    @staticmethod
    def drawMap() :
        # draw map.
        for i, yMap in enumerate(tetris.Map) :
            tempX = 300
            tempY = 20 * i
            for j, xMap  in enumerate(yMap) :
                tempColor = 0
                # 지하철 노선에 따른 색깔
                if 0 < xMap <= 6:
                    tempColor = tetris.colors[xMap]
                if 30 > xMap >= 1 :
                    pygame.draw.rect(tetris.screen, tempColor, pygame.Rect(tempX, tempY, 20, 20))
                tempX += 20

    # 게임과 관계 없는 화면에 배경을 그려주는 함수
    def insertImgPosition(x, y, image) :
        _indx = lambda xy : xy * 20
        Mapped = [(_indx(x) + 200 , _indx(y) - 20), (_indx(x) + 260 , _indx(y) + 20), (_indx(x) + 300 , _indx(y) - 20)]
        positionMapped = [x == 0, 30 > x > 0, x == 31]
        for i, m in enumerate(positionMapped) :
            if m :
                tetris.screen.blit(image, (Mapped[i][0], Mapped[i][1]))

    @staticmethod
    def drawBackbround() :
        tempN = 0
        for i in range(0, 2) :
            tempW = [280, 900]
            tempN = 0
            for j in range(0, tetris.mapRangeY) :
                tetris.screen.blit(tetris.block, (tempW[i], tempN))
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
        tetris.insertImgPosition(tetris.startPathX, tetris.startPathY, tetris.missionStartImg)
        tetris.insertImgPosition(tetris.endPathX, tetris.endPathY, tetris.missionEndImg)

    moveLeftCnt = 0
    moveRightCnt = 0
    oldval = [False, False, False, False, False] # 이전 키 입력
    # key값 에 따른 움직임 함수
    def movePlay() :
        if tetris.keys[2] and tetris.blockX > 300 and tetris.checkMoveL:
            tetris.moveLeftCnt += 1
            if tetris.moveLeftCnt == 10000 :
                tetris.blockX -= 20
                tetris.moveLeftCnt = 0
        elif tetris.keys[3] and tetris.blockX < 900 and tetris.checkMoveR:
            tetris.moveRightCnt += 1
            if tetris.moveRightCnt == 10000 :
                tetris.blockX += 20
                tetris.moveRightCnt = 0
        elif tetris.oldval[0] != tetris.keys[0] : # 이전 입력과 현재입력이 다를때(중복실행 방지)
            tetris.oldval = tetris.keys
            tetris.changeBlockShape = (tetris.changeBlockShape + 1) % 4
        elif tetris.oldval[1] != tetris.keys[1] :  # 이전 입력과 현재입력이 다를때(중복실행 방지)
            tetris.oldval = tetris.keys
            tetris.blockTimer1 = 1
            tetris.fastDownFlag = 1
        elif tetris.keys[4] :
            tetris.missionClearEvent()

    # key 입력 이벤트 처리 함수
    @staticmethod
    def keyeEventProcess() :
        # loop through the events
        for event in pygame.event.get():
            # key가 눌렸을때
            if event.type == pygame.KEYDOWN:
                tetris.keys= [event.key == K_UP and tetris.blockX < 840, event.key == K_DOWN,
                              event.key == K_LEFT, event.key == K_RIGHT, event.key == K_SPACE]
                pygame.mixer.Sound.play(tetris.btnSound)
            # key가 떨어졌을때
            if event.type == pygame.KEYUP:
                for i in range(0, 5) :
                    tetris.keys[i] = False
            # if it is quit the game
            if event.type == pygame.QUIT:
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
        for i in range(3, 0, -1) :
            yBlock = tetris.nowBlockShape[(tetris.changeBlockShape * 4) + i]
            # map에 블럭이 내려올때 바로 아래단에 블럭이 차있는지 확인 or 바닥에 닿았을 경우
            for j, tBlock in enumerate(yBlock) :
                if ((tBlock == 1 and tetris.Map[int(tetris.blockY / 20) + i + 1][int((tetris.blockX - 300) / 20) + j] >= 1)
                        or (tetris.blockY + 60 == ((tetris.mapRangeY - 1) * 20) - 20)) :
                    # 미션 실패(더 이상 내려올 곳이 없을때)
                    if tetris.blockY == 0 :
                        tetris.screen.blit(tetris.missionFailImg, (315, 250))
                        tetris.showPlayTime()
                        tetris.drawText(598, 345, str(tetris.stageLevel + 1), 30)
                        pygame.display.flip()
                        if tetris.stageLevel > 0 :
                            self.sendDataToServer = 1
                        self.gameSequence = 0
                        time.sleep(1)
                    tetris.copyBlockToMap()
                    tetris.blockX = 580
                    tetris.blockY = 0
                # 블럭이 좌, 우로 이동 가능한지 체크
                if tBlock == 1 and tetris.Map[int(tetris.blockY / 20) + i][int((tetris.blockX - 300) / 20) + j - 1] >= 1 :
                    tetris.checkMoveL = 0
                if tBlock == 1 and tetris.Map[int(tetris.blockY / 20) + i][int((tetris.blockX - 300) / 20) + j + 1] >= 1 :
                    tetris.checkMoveR = 0
        # 블럭 아래로 한칸씩 내리기
        if tetris.blockY < ((tetris.mapRangeY - 1) * 20) - 80 :
            if tetris.fastDownFlag == 0 :
                tetris.blockY += 1
            else :
                tetris.blockY -= (tetris.blockY % 10) # 20의 배수에서 checkFillBlock()을 실행하기 때문에
                tetris.blockY += 10

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
                        tetris.Map[0][k] = 0
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
                exit(0)
        return result

    # 버튼 선택 효과 보여주는 함수 들
    def _buildStartImage(x,y,z):
        if x:
            tetris.screen.blit(tetris.smallStartImg, (455, 380))
        for _img, _pos in [(tetris.smallStartImg, (455, 380)), (tetris.smallEndImg, (715, 380)),(tetris.smallDescriptionImg, (586, 380))]:
            tetris.screen.blit(_img, _pos)

    def _play_btn_sound(flag):
        if not flag:
            pygame.mixer.Sound.play(tetris.btnSound)
        return True

    btnSoundflag = False
    @staticmethod
    def effectMenueBtn() :
        pos = pygame.mouse.get_pos()
        x_inx =[ 522 >= pos[0] >= 455 , 643 >= pos[0] >= 586,  772 >= pos[0] >= 715 ]
        b_mapped = zip(x_inx , [(tetris.bigStartImg, (445, 340)), (tetris.bigDescriptionImg, (576, 340)), (tetris.bigEndImg, (705, 340) )])
        s_mapped = [(tetris.smallStartImg, (455, 380)), (tetris.smallEndImg, (715, 380)), (tetris.smallDescriptionImg, (586, 380))]

        for k in s_mapped :
            tetris.screen.blit(k[0], k[1])

        if 588 >= pos[1] >= 380 :
            if True in x_inx :
                tetris.btnSoundflag = tetris._play_btn_sound(tetris.btnSoundflag)
            else:
                tetris.btnSoundflag = False
            for j, k in b_mapped:
                if j :
                    tetris.screen.blit(k[0], k[1])
        else:
            tetris.btnSoundflag = False

    # description 페이지 관련 메소드(사용자 정보 입력 등)
    gameID = ['d','e','f','a','u','l','t']
    def inputInform(self) :
        tmpChar  = ''
        tetris.drawText(390, 635, ''.join(tetris.gameID), 27)
        for event in pygame.event.get():
            # 키보드 눌렀을때
            if event.type == pygame.KEYDOWN:
                inputKey = [K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m,
                            K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z]
                if len(tetris.gameID) < 25 :
                    for i, inputChar in enumerate(inputKey) :
                        if event.key == inputChar :
                            tmpChar = ord('a') + i  # 아스키값
                            tetris.gameID.append(chr(tmpChar))  # 아스키값을 char값으로 변환
                    if event.key == K_SPACE :
                        tetris.gameID.append(' ')
                if event.key == K_BACKSPACE and len(tetris.gameID) > 0 :
                    tetris.gameID.pop()
            # 마우스 클릭
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (1065 >= pos[0] >= 865) and (165 >= pos[1] >= 90) :
                    self.gameSequence = 0
            # 게임 끝내기
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

    #게임 데이터 서버로 전송
    @staticmethod
    def sendGameData() :
        tName = ''.join(tetris.gameID)
        tgameScore = tetris.resultScore
        tgameTime = str(datetime.datetime.now())
        tIntroduction = '게임시간 : ' + tgameTime + tetris.gameClearMessage
        data = {"secret_key" : '시크릿키', "name" : tName, "introduction" : tIntroduction,
                "gamescore" : tgameScore, "gamelevel" : tetris.stageLevel ,"gametime" : 0, "emailladdress" : 'default'}
        res = requests.post(tetris.url, data = data)
        tetris.resultScore = 0
        tetris.stageLevel = 0

    @staticmethod
    def viewTimer() :
        print(str(datetime.datetime.now()))
        timer = threading.Timer(1, tetris.viewTimer)

    # 스테이지 별로 맵 바꿔주는 함수(리팩토링 예정)
    def stageChange(level) :
        for i in range(0, tetris.mapRangeY) :
            tetris.Map[i][30] = 88
        if level == 0 :
            for i in range(0, 27) :
                tetris.Map[39][i] = 4
                tetris.Map[38][i] = 3
                tetris.Map[35][i] = 2
                tetris.Map[34][i] = 1
            for i in range(2,29) :
                tetris.Map[37][i] = 6
                tetris.Map[36][i] = 5
                tetris.Map[33][i] = 4
                tetris.Map[32][i] = 3
        elif level == 1 :
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
        elif level == 2 :
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
        elif level == 3 :
            for i in range(20, 40) :
                if i % 2 == 0 :
                    for j in range(1, 29) :
                        tetris.Map[i][j] = random.randint(1, 6)
                else :
                    for j in range(0, 28) :
                        tetris.Map[i][j] = random.randint(1, 6)
        '''elif level == 0 :
            for i in range(1, 18) :
                tetris.Map[27][i] = 4
            for i in range(27, 40) :
                tetris.Map[i][14] = 4
                tetris.Map[i][17] = 4
            tetris.Map[39][16] = 4
            tetris.Map[39][15] = 4'''
