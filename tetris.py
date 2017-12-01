# 1 - Import library
import pygame
from pygame.locals import *
import math
import random

# Initialize the game
pygame.init()
width, height = 1300, 800
screen=pygame.display.set_mode((width, height))

# data
map = [[0, 0, 0, 0, 0, 0, 0], # 7 * 8
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        ]

keys = [0, 0, 0, 0]

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255, 255, 255)

#블록데이터 구조 설정
b1 = { 'rect':pygame.Rect(300,80,50,100), 'color':RED}
b2 = { 'rect':pygame.Rect(200,200,20,20), 'color':GREEN}
b3 = { 'rect':pygame.Rect(100,150,60,60), 'color':BLUE}
blocks = [b1,b2,b3]

blockTimer = 10000
blockTimer1 = 0
blockX = 300
blockY = 0

while 1:
    blockTimer -= 1
    # update the screen
    if blockTimer == 0 :
        blockTimer = 100 - (blockTimer1 * 2)
        '''if blockTimer1 >= 35 :
            blockTimer1 = 35
        else :
            blockTimer1 += 5'''
        screen.fill(0)
        pygame.draw.rect(screen, b1['color'], pygame.Rect(blockX , blockY, 100, 100))
        pygame.display.flip()
        if blockY < 700 :
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
        blockX-=100
        keys[2] = 0
    elif keys[3] == 2 :
        blockX+=100
        keys[3] = 0
