block1 = [[0, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 1, 0, 0]
          ]
block2 = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 1, 0, 0],
          [1, 1, 1, 0]
          ]
block3 = [[1, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 0, 0, 0]
          ]
block4 = [[0, 0, 0, 0],
          [0, 1, 0, 0],
          [1, 1, 0, 0],
          [1, 0, 0, 0]
          ]

# test
def randBlock(nextBlock) :
    if nextBlock == 0 :
        return block1
    elif nextBlock == 1 :
        return block2
    elif nextBlock == 2 :
        return block3
    elif nextBlock == 3 :
        return block4
