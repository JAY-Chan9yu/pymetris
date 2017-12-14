import pygame
from pygame.locals import *
import math
import random
import blocklib
import tetris
import time

if __name__ == "__main__":
    gameSequence = 0        # game play 진행 순서

    pygame.init()
    game = tetris.tetris()

    '''# text 만들기
    fontObj = pygame.font.Font('tetrisResource/font/NanumGothicBold.ttf', 32)
    textSurfaceObj = fontObj.render('Hello Font!', True, game.GREEN)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (150, 150)
    game.screen.blit(textSurfaceObj, textRectObj)'''

    while 1 :
        # init view
        if gameSequence == 0 :
            pos = pygame.mouse.get_pos()
            game.screen.blit(game.initBackground, (0, 0))

            # 버튼 선택 효과
            if (pos[0] >= 465 and pos[0] <= 522) and ((pos[1] >= 380 and pos[1] <= 588)) :
                game.screen.blit(game.bigStartImg, (455, 340))
            else :
                game.screen.blit(game.smallStartImg, (465, 380))

            if (pos[0] >= 586 and pos[0] <= 643) and ((pos[1] >= 380 and pos[1] <= 588)) :
                game.screen.blit(game.bigDescriptionImg, (576, 340))
            else :
                game.screen.blit(game.smallDescriptionImg, (586, 380))

            if (pos[0] >= 715 and pos[0] <= 772) and ((pos[1] >= 380 and pos[1] <= 588)) :
                game.screen.blit(game.bigEndImg, (705, 340))
            else :
                game.screen.blit(game.smallEndImg, (715, 380))
            pygame.display.flip()

            pageButton = game.clickButton()
            if pageButton == 1 :
                gameSequence = 2
                game.gameInit()
            elif pageButton == 2 :
                # gameSequence = 1
                print('설명')
            elif pageButton == 3 :
                pygame.quit()
                exit(0)

        # View game description
        elif gameSequence == 1 :
            pass
        # Play gmae
        elif gameSequence == 2 :
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
                    # draw preview block
                    game.drawPreviewBlock()
                else :
                    time.sleep(3)
                    game.missionClearEventFlag = 0
                    #pass

                # update screen
                pygame.display.flip()

            # key event
            game.keyeEventProcess()
