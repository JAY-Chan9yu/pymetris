import pygame
from pygame.locals import *
import math
import random
import blocklib
import tetris
import time

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.music.load("tetrisResource/audio/bgm.mp3")
    pygame.mixer.music.play(-1)
    game = tetris.tetris()
    game.gameSequence = 0        # game play 진행 순서

    while 1 :
        # init viewgameSequence
        if game.gameSequence == 0 :
            game.screen.blit(game.initBackground, (0, 0))
            game.effectMenueBtn()
            pygame.display.flip()

            pageButton = game.clickButton()
            if pageButton == 1 :
                game.gameSequence = 2
                game.gameInit()
            elif pageButton == 2 :
                game.gameSequence = 1
            elif pageButton == 3 :
                pygame.quit()
                exit(0)

        # View game description
        elif game.gameSequence == 1 :
            pageButton = 0
            game.screen.blit(game.descriptionBackground, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if (pos[0] >= 865 and pos[0] <= 1065) and ((pos[1] >= 90 and pos[1] <= 165)) :
                        game.gameSequence = 0
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
        # Play gmae
        elif game.gameSequence == 2 :
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
                    game.missionClearEventFlag = 0
                # update screen
                pygame.display.flip()
            # key event
            game.keyeEventProcess()
