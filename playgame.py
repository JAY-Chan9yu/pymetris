import pygame
from pygame.locals import *
import math
import random
import blocklib
import tetris

if __name__ == "__main__":
    pygame.init()
    game = tetris.tetris()

    game.nextBlockShape = blocklib.randBlock(random.randint(0, 3))

    # 오른쪽 벽 채우기(오른쪽으로 더이상 이동 못하게)
    for i in range(0, game.mapRangeY) :
        game.Map[i][30] = 88

    while 1 :
        game.blockTimer -= 1

        if game.blockTimer <= 0 :
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

        # key event
        game.keyeEventProcess()
