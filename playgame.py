import pygame
from pygame.locals import *
import math
import random
import blocklib
import tetris
import time

if __name__ == "__main__":
    pygame.init()
    game = tetris.tetris()

    game.nextBlockShape = blocklib.randBlock(random.randint(0, 3))

    # 오른쪽 벽 채우기(오른쪽으로 더이상 이동 못하게)
    for i in range(0, game.mapRangeY) :
        game.Map[i][30] = 88
    for i in range(27, 40) :
        game.Map[i][14] = 4
    for i in range(27, 40) :
        game.Map[i][16] = 4
    for i in range(1, 15) :
        game.Map[27][i] = 4

    game.Map[39][15] = 4
    game.Map[39][16] = 4

    game.screen.blit(game.background, (0, 0))
    pygame.draw.rect(game.screen, game.BLACK, pygame.Rect(300, 0, 600, 800))
    pygame.display.flip()

    '''# text 만들기
    fontObj = pygame.font.Font('tetrisResource/font/NanumGothicBold.ttf', 32)
    textSurfaceObj = fontObj.render('Hello Font!', True, game.GREEN)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (150, 150)
    game.screen.blit(textSurfaceObj, textRectObj)'''

    while 1 :
        game.blockTimer -= 1
        if game.blockTimer <= 0 :
            game.blockTimer = game.blockTimer1

            game.updateMap()
            game.checkFillBlock()

            if game.missionClearEventFlag == 0 :
                # clean map
                pygame.draw.rect(game.screen, game.BLACK, pygame.Rect(300, 0, 600, 800))

                # draw background
                game.drawBackbround()
                # draw map
                game.drawMap()
                # draw now block
                game.drawBlock(0, game.nowBlockShape, game.blockColor, game.blockX, game.blockY)
                # draw next block
                game.drawBlock(0, game.nextBlockShape, game.nextColor, 940, 0)

                game.drawPreviewBlock()
            else :
                time.sleep(1)
                game.missionClearEventFlag = 0
                #pass

            # update screen
            pygame.display.flip()

        # key event
        game.keyeEventProcess()
