import pygame
from pygame.locals import *
import math
import random
import blocklib
import tetris

if __name__ == "__main__":
    pygame.init()
    game = tetris.tetris

    game.nextBlockShape = blocklib.randBlock(random.randint(0, 3))
    print("TEST")
    # 오른쪽 벽 채우기(오른쪽으로 더이상 이동 못하게)
    for i in range(0, game.mapRangeY) :
        game.Map[i][30] = 88
    for i in range(30, 40) :
        game.Map[i][9] = 3
    for i in range(1, 9) :
        game.Map[30][i] = 3
        #map[39][i] = 1
    for i in range(1, 30) :
        game.Map[38][i] = 2
    for i in range(1, 30) :
        game.Map[39][i] = 2

    while 1 :
        game.blockTimer -= 1
        if game.blockTimer == 0 :
            game.blockTimer = game.blockTimer1
            game.screen.fill(0)

            game.updateMap()
            game.checkFillBlock()

            # draw map
            game.drawMap()
            # draw now block
            game.drawBlock(game.nowBlockShape, game.blockColor, game.blockX, game.blockY)
            # draw next block
            game.drawBlock(game.nextBlockShape, game.nextColor, 940, 0)
            # draw background
            game.drawBackbround()

            # update screen
            pygame.display.flip()

            # 블럭 아래로 한칸씩 내리기
            if game.blockY < ((game.mapRangeY - 1) * 20) - 80 :
                game.blockY += 1

        # key event
        game.keyeEventProcess()
