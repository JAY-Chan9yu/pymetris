# 1 - Import library
import pygame
from pygame.locals import *
import math
import random
import blocklib

pygame.init()
width, height = 1200, 1000
mapRangeX, mapRangeY = 33, 41
screen=pygame.display.set_mode((width, height))

map = [[0] * mapRangeX for row in range(mapRangeY)] # 20 x 20  30 * 20 = 600 픽셀

keys = [0, 0, 0, 0, 0] # key 값 판단하는 리스트

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

missionClearEventFlag = 0 # mission clear 이벤틀 플래그
# 게임 스피드
blockTimer = 5000
blockTimer1 = 5000
changeBlockShape = 0 # 블럭의 모양을 변경하는 변수
nowBlockShape = blocklib.block1 # 현재 나오는 블럭의 모양
nextBlockShape = blocklib.block1 # 다음 블럭
blockColor = ORANGE # 블럭 색상
nextColor = BLUE # 다음 블럭 색상
checkMoveR = 0
checkMoveL = 0
blockX = 600 # 현재 나오는 블럭의 x,y 좌표
blockY = 0
missionColor = 3 # 미션 컬러
minPath = 999 # 최단경로

startPathX = 0
startPathY = 29
endPathX = 10
endPathY = 40
# load images
block = pygame.image.load("tetrisResource/image/block.jpg")

def copyBlocToMap(block, X, Y) :
    global map
    global nextColor
    global blockColor
    global blockTimer1
    global nowBlockShape
    global nextBlockShape

    for i in range(0, 4) :
        for j in range(0, 4) :
            # 지하철 노선에 따른 색깔
            tempColor = 0
            if blockColor == BLUE:
                tempColor = 1
            elif blockColor == GREEN:
                tempColor = 2
            elif blockColor == ORANGE :
                tempColor = 3
            elif blockColor == BLUE :
                tempColor = 4
            elif blockColor == PURPLE :
                tempColor = 5
            elif blockColor == BROWN :
                tempColor = 6

            if block[(changeBlockShape * 4) + i][j] >= 1 :
                map[int((Y / 20) + i)][int(((X - 300) / 20) + j)] = tempColor

    blockTimer1 = 5000
    blockColor = nextColor
    nowBlockShape = nextBlockShape
    nextBlockShape = blocklib.randBlock(random.randint(0, 3))
    nextColor = colors[random.randint(1, 6)]

def missionClearEvent() :
    dfsSerch(0, 30, 1)
    print("short path cnt : " + str(minPath))

# 최단거리 탐색
def dfsSerch(x, y, cnt) :
    global map
    global endPathX
    global endPathY
    global mapRangeX
    global mapRangeY
    global missionColor
    global minPath

    if x == (endPathX - 1) and y == (endPathY - 1) :
        if cnt < minPath :
            minPath = cnt
        return

    map[y][x] = 0

    print("x : " + str(x) + " y : " + str(y))
    if x > 0 and map[y][x - 1] == missionColor : # Left
        dfsSerch(x - 1, y, cnt + 1)
    if x < mapRangeX - 3 and map[y][x+1] == missionColor :
        dfsSerch(x + 1, y, cnt + 1)
    if y > 0 and map[y - 1][x] == missionColor :
        dfsSerch(x, y - 1, cnt + 1)
    if y < mapRangeY - 1 and map[y + 1][x] == missionColor : # Down
        dfsSerch(x, y + 1, cnt + 1)

    # 원상 복귀
    map[y][x] = missionColor

if __name__ == "__main__":
    nextBlockShape = blocklib.randBlock(random.randint(0, 3))
    # 오른쪽 벽 채우기(오른쪽으로 더이상 이동 못하게)
    for i in range(0, mapRangeY) :
        map[i][30] = 88
    for i in range(30, 40) :
        map[i][9] = 3
    for i in range(1, 9) :
        map[30][i] = 3
        #map[39][i] = 1

    while 1:
        blockTimer -= 1
        #screen.fill(0)

        # block update
        if blockTimer == 0 :
            blockTimer = blockTimer1
            screen.fill(0)

            # update map
            checkMoveL = checkMoveR = 1
            for i in range(3, 0, -1) :
                yBlock = nowBlockShape[(changeBlockShape * 4) + i]
                # map에 블럭이 내려올때 바로 아래단에 블럭이 차있는지 확인 or 바닥에 닿았을 경우
                for j, tBlock in enumerate(yBlock) :
                    if ((tBlock == 1 and map[int(blockY / 20) + i + 1][int((blockX - 300) / 20) + j] >= 1)
                            or (blockY + 60 == ((mapRangeY - 1) * 20) - 20)) :
                        copyBlocToMap(nowBlockShape, blockX, blockY)
                        blockX = 300
                        blockY = 0
                    if (tBlock == 1 and map[int(blockY / 20) + i][int((blockX - 300) / 20) + j - 1] >= 1) :
                        checkMoveL = 0
                    if (tBlock == 1 and map[int(blockY / 20) + i][int((blockX - 300) / 20) + j + 1] >= 1) :
                        checkMoveR = 0

            # checkFillBlock
            for i in range(mapRangeY - 2, 0, -1) :
                yMap = map[i]
                checkLine = 0
                for xMap in yMap : # 라인 체크
                    if xMap >= 1 :
                        checkLine += 1
                if checkLine >= 31 : # 라인이 한줄 꽉찰경우
                    for t in range(mapRangeY - 2, 1, -1) :
                        for k in range(0, 31) :
                            map[t][k] = map[t - 1][k]
                    for k in range(0, 31) :
                        map[0][k] = 0
                checkLine = 0

            # draw map.
            for i, yMap in enumerate(map) :
                tempX = 300
                tempY = 20 * i
                for j, xMap  in enumerate(yMap) :
                    tempColor = 0

                    # 지하철 노선에 따른 색깔
                    if xMap == 1:
                        tempColor = BLUE
                    elif xMap == 2:
                        tempColor = GREEN
                    elif xMap == 3 :
                        tempColor = ORANGE
                    elif xMap == 4 :
                        tempColor = BLUE
                    elif xMap == 5 :
                        tempColor = PURPLE
                    elif xMap == 6 :
                        tempColor = BROWN

                    if xMap >= 1 :
                        #pygame.draw.rect(screen, colors[random.randint(0,4)], pygame.Rect(tempX, tempY, 20, 20))
                        pygame.draw.rect(screen, tempColor, pygame.Rect(tempX, tempY, 20, 20))
                    tempX += 20

            # draw now block
            for i in range(0, 4) :
                tBlock = nowBlockShape
                yBlock = tBlock[(changeBlockShape * 4) + i]
                tempX = blockX
                tempY = blockY + (20 * i)
                for j, xBlock  in enumerate(yBlock) :
                    if xBlock >= 1 :
                        pygame.draw.rect(screen, blockColor, pygame.Rect(tempX, tempY, 20, 20))
                    tempX += 20

            # draw next block
            for i in range(0, 4) :
                tBlock = nextBlockShape
                yBlock = tBlock[(changeBlockShape * 4) + i]
                tempX = 940
                tempY = 20 * i
                for j, xBlock in enumerate(yBlock) :
                    if xBlock >= 1 :
                        pygame.draw.rect(screen, nextColor, pygame.Rect(tempX, tempY, 20, 20))
                    tempX += 20

            # draw background
            tempN = 0
            for i in range(0, 2) :
                tempW = 280
                if i == 1 :
                    tempW = 900
                    tempN = 0
                for j in range(0, mapRangeY) :
                    screen.blit(block, (tempW, tempN))
                    tempN += 20
            tempN = 280
            for i in range(0, mapRangeX - 2) :
                screen.blit(block, (tempN, (mapRangeY - 1) * 20))
                tempN += 20
            pygame.draw.rect(screen, ORANGE, pygame.Rect((startPathX * 20) + 280, (startPathY * 20), 20, 20))
            pygame.draw.rect(screen, ORANGE, pygame.Rect((endPathX * 20) + 280, (endPathY * 20), 20, 20))


            # update screen
            pygame.display.flip()

            if blockY < ((mapRangeY - 1) * 20) - 80 :
                blockY += 1 # 아래로 내려가기

        # loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.KEYDOWN: # key가 눌렸을때
                if event.key == K_UP:
                    keys[0] = 1
                elif event.key == K_DOWN:
                    keys[1] = 1
                elif event.key == K_LEFT and blockX > 300 and checkMoveL == 1:
                    keys[2] = 1
                elif event.key == K_RIGHT and blockX < 900 and checkMoveR == 1:
                    keys[3] = 1
                elif event.key == K_SPACE :
                    keys[4] = 1

            if event.type==pygame.KEYUP: # key가 떨어졌을때
                if keys[0] == 1 and event.key == K_UP:
                    keys[0] = 2
                elif keys[1] == 1 and event.key == K_DOWN:
                    keys[1] = 2
                elif keys[2] == 1 and event.key == K_LEFT:
                    keys[2] = 2
                elif keys[3] == 1 and event.key == K_RIGHT:
                    keys[3] = 2
                elif keys[4] == 1 and event.key == K_SPACE :
                    keys[4] = 2

            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)

        # Move playe
        if keys[2] == 2 :
            blockX -= 20
            keys[2] = 0
        elif keys[3] == 2 :
            blockX += 20
            keys[3] = 0
        elif keys[0] == 2 :
            changeBlockShape += 1
            if changeBlockShape >= 4 :
                changeBlockShape = 0
            keys[0] = 0
        elif keys[1] == 2 :
            blockTimer1 = 5
            keys[1] = 0
        elif keys[4] == 2 :
            missionClearEventFlag = 1
            missionClearEvent()
            keys[4] = 0
