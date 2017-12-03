# 1 - Import library
import pygame
from pygame.locals import *
import math
import random
import blocklib

pygame.init()
width, height = 1200, 700
screen=pygame.display.set_mode((width, height))

map = [[0] * 30 for row in range(30)] # 20 x 20  30 * 20 = 600 픽셀

keys = [0, 0, 0, 0] # key 값 판단하는 리스트

nextBlock = 0 # 다음 블럭

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
colors = [BLACK, RED, GREEN, BLUE, WHITE]

blockTimer = 100000
blockTimer1 = 0
blockX = 300
blockY = 0

# load images
block = pygame.image.load("tetrisResource/image/block.jpg")

def copyBlocToMap(block, X, Y) :
    global map
    global nextBlock

    for i in range(0, 4) :
        for j in range(0, 4) :
            if block[i][j] >= 1 :
                map[int((Y / 20) + i)][int(((X - 300) / 20) + j)] = block[i][j]
    #map[28][28] = 1#int(block[i][j])

    nextBlock = random.randint(0, 3)


if __name__ == "__main__":
    while 1:
        blockTimer -= 1
        #screen.fill(0)

        # block update
        if blockTimer == 0 :
            blockTimer = 100 - (blockTimer1 * 2)
            screen.fill(0)

            #update map
            for i in blocklib.block1[3] :
                if (i == 1 and map[int(blockY / 20)+1][int((blockX - 300) / 20)] == 1) \
                    or (blockY + 60 == 580) :
                    #tempa =1
                    copyBlocToMap(blocklib.block1, blockX, blockY)
                    blockX = 300
                    blockY = 0

            # draw map
            for i, yMap in enumerate(map) :
                tempX = 300
                tempY = 20 * i
                for j, xMap  in enumerate(yMap) :
                    tempColor = 0

                    # 지하철 노선에 따른 색깔
                    if xMap == 2:
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
                        pygame.draw.rect(screen, ORANGE, pygame.Rect(tempX, tempY, 20, 20))
                        tempX += 20

            # draw now block
            for i, yBlock in enumerate(blocklib.block1) :
                tempX = blockX
                tempY = blockY + (20 * i)
                for j, xBlock  in enumerate(yBlock) :
                    tempColor = 0
                    if xBlock == 1 :
                        tempColor = ORANGE
                    pygame.draw.rect(screen, tempColor, pygame.Rect(tempX, tempY, 20, 20))
                    tempX += 20

            # draw next block
            for i, yBlock in enumerate(blocklib.randBlock(nextBlock)) :
                tempX = 940
                tempY = 20 * i
                for j, xBlock  in enumerate(yBlock) :
                    tempColor = 0
                    if xBlock == 1 :
                        tempColor = ORANGE
                    pygame.draw.rect(screen, tempColor, pygame.Rect(tempX, tempY, 20, 20))
                    tempX += 20

            # draw background
            tempN = 0
            for i in range(0, 2) :
                tempW = 280
                if i == 1 :
                    tempW = 900
                    tempN = 0
                for j in range(0, 31) :
                    screen.blit(block, (tempW, tempN))
                    tempN += 20
            tempN = 280
            for i in range(0, 32) :
                screen.blit(block, (tempN, 600))
                tempN += 20

            # update screen
            pygame.display.flip()

            if blockY < 520  :
                blockY += 1 # 아래로 내려가기

        # loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.KEYDOWN: # key가 눌렸을때
                if event.key==K_UP:
                    keys[0]=1
                elif event.key==K_DOWN:
                    keys[1]=1
                elif event.key==K_LEFT and blockX > 300 :
                    keys[2]=1
                elif event.key==K_RIGHT and blockX < 900:
                    keys[3]=1

            if event.type==pygame.KEYUP: # key가 떨어졌을때
                if keys[0] == 1 and event.key==pygame.K_UP:
                    keys[0]=2
                elif keys[1] == 1 and event.key==pygame.K_DOWN:
                    keys[1]=2
                elif keys[2] == 1 and event.key==pygame.K_LEFT:
                    keys[2]=2
                elif keys[3] == 1 and event.key==pygame.K_RIGHT:
                    keys[3]=2

            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)

        # Move playe
        if keys[2] == 2 :
            blockX-=20
            keys[2] = 0
        elif keys[3] == 2 :
            blockX+=20
            keys[3] = 0
