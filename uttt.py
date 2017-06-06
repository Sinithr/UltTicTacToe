#!/usr/bin/env python3.4

import random

area = 0 # 0 -> you can place symbol everywhere you want
         # 1-9 -> you can place only on area with this number

bigSymbols = [[" " for _ in range(3)] for _ in range(3)]
status = None

def main():
    global bigSymbols, status
    bigBoard = makeBigBoard()
    while status == None:
        showBigBoard(bigBoard)
        makeMove(bigBoard)
        enemyMove(bigBoard)
        if find3Symbols(bigSymbols, "x"):
            status = True
            print("You won! :)")
        elif find3Symbols(bigSymbols, "o"):
            status = False
            print("You lose! :(")

def find3Symbols(board, player):
    if board[0][0] == player and board[0][1] == player and board[0][2] == player:
        return True
    if board[1][0] == player and board[1][1] == player and board[1][2] == player:
        return True
    if board[2][0] == player and board[2][1] == player and board[2][2] == player:
        return True
    if board[0][0] == player and board[1][0] == player and board[2][0] == player:
        return True
    if board[0][1] == player and board[1][1] == player and board[2][1] == player:
        return True
    if board[0][2] == player and board[1][2] == player and board[2][2] == player:
        return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def enemyMove(bigBoard):
    global area, bigSymbols, status
    row = -1
    col = -1
    if area == 0:
        maximum = 0
        for i in range(3):
            for j in range(3):
                if bigSymbols[i][j] == " ":
                    if max(max(allChance(bigBoard[i][j], "o"))) > maximum:
                        row = i
                        col = j
    elif 1 <= area <= 3:
        row = 0
        col = area - 1
    elif 4 <= area <= 6:
        row = 1
        col = area - 4
    else:
        row = 2
        col = area - 7
    if row == -1 and col == -1:
        print("Nobody won. Draw.")
        status = False
        return
    chance = allChance(bigBoard[row][col], "o")
    maximum = max(max(chance))
    indexes = []
    for i in range(3):
        indexes.append([i for i,val in enumerate(chance[i]) if val == maximum])
    ys = [i for i,val in enumerate(indexes) if len(val) > 0]
    coords = [[ys[i], chance[ys[i]].index(maximum)] for i in range(len(ys))]
    random.shuffle(coords)
    x = coords[0][0]
    y = coords[0][1]
    moveString = "Enemy (board, area): ("
    moveString += str(col + 3*row + 1)
    moveString += ", "
    moveString += str(y + 3*x + 1)
    moveString += ")"
    print(moveString)
    bigBoard[row][col][x][y] = "o"
    if find3Symbols(bigBoard[row][col], "o"):
        bigSymbols[row][col] = "o"
    elif boardFull(bigBoard[row][col]):
        bigSymbols[row][col] = "F"
    if bigSymbols[x][y] != " ":
        area = 0
    else:
        area = y + 3*x + 1

def boardFull(board):
    for row in board:
        for pos in row:
            if pos == " ":
                return False
    return True

def smallChance(board, player):
    possibList = chanceToWin(board, player)
    for i in range(3):
        for j in range(3):
            if possibList[i][j] == 10:
                possibList[i][j] = 0
            else:
                possibList[i][j] /= 100
    return possibList

def bigChance(board, player):
    possibList = chanceToWin(board, player, big=True)
    for i in range(3):
        for j in range(3):
            if possibList[i][j] == 10:
                possibList[i][j] = 0
            else:
                possibList[i][j] /= 10
    return possibList

def allChance(board, player):
    global bigSymbols
    smallPossib = smallChance(board, player)
    bigPossib = bigChance(bigSymbols, player)
    for i in range(3):
        for j in range(3):
            if smallPossib[i][j] == 0:
                bigPossib[i][j] = 0
            else:
                bigPossib[i][j] += smallPossib[i][j]
    return bigPossib

def chanceToWin(board, player, big=False):
    if player == "x":
        enemy = "o"
    elif player == "o":
        enemy = "x"
    else:
        return None
    possibList = Possibilities(board, player)
    possibList = minMax(possibList)
    enemyPossib = Possibilities(board, enemy)
    enemyPossib = minMax(enemyPossib)
    if big:
        for i in range(3):
            for j in range(3):
                enemyPossib[i][j] = 1. - enemyPossib[i][j]
    for i in range(3):
        for j in range(3):
            if possibList[i][j] != 0:
                possibList[i][j] += enemyPossib[i][j] 
    return possibList

def minMax(p):
    new_p = [[None for _ in range(3)] for _ in range(3)]
    new_p[0][0] = max(min(p[0][0],p[1][0],p[2][0]), min(p[0][0],p[1][1],p[2][2]), min(p[0][0],p[0][1],p[0][2]))
    new_p[0][2] = max(min(p[0][2],p[0][0],p[0][1]), min(p[0][2],p[1][1],p[2][0]), min(p[0][2],p[1][2],p[2][2]))
    new_p[2][0] = max(min(p[2][0],p[1][0],p[0][0]), min(p[2][0],p[1][1],p[0][2]), min(p[2][0],p[2][1],p[2][2]))
    new_p[2][2] = max(min(p[2][2],p[2][1],p[2][0]), min(p[2][2],p[1][1],p[0][0]), min(p[2][2],p[1][2],p[0][2]))
    new_p[0][1] = max(min(p[0][1],p[0][0],p[0][2]), min(p[0][1],p[1][1],p[2][1]))
    new_p[1][0] = max(min(p[1][0],p[0][0],p[2][0]), min(p[1][0],p[1][1],p[1][2]))
    new_p[1][2] = max(min(p[1][2],p[0][2],p[2][2]), min(p[1][2],p[1][1],p[1][0]))
    new_p[2][1] = max(min(p[2][1],p[2][0],p[2][2]), min(p[2][1],p[1][1],p[0][1]))
    new_p[1][1] = max(min(p[1][1],p[0][0],p[2][2]), min(p[1][1],p[0][2],p[2][0]), min(p[1][1],p[0][1],p[2][1]), min(p[1][1],p[1][0],p[1][2]))
    for i in range(3):
        for j in range(3):
            if p[i][j] == 0:
                new_p[i][j] = 0
            elif p[i][j] == 10:
                new_p[i][j] = 10
    return new_p

def Possibilities(board, player): # how many possibilities are to win on each place
    if player == "x":
        enemy = "o"
    elif player == "o":
        enemy = "x"
    else:
        return None
    possibList = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            if board[i][j] == enemy:
                possibList[i][j] = 0
                continue
            if board[i][j] == player:
                possibList[i][j] = 10
                continue
            if i == 1:
                if j == 1: # i=1, j=1
                    possibilities = 4
                    if board[0][0] == enemy or board[2][2] == enemy:
                        possibilities -= 1
                    if board[0][1] == enemy or board[2][1] == enemy:
                        possibilities -= 1
                    if board[0][2] == enemy or board[2][0] == enemy:
                        possibilities -= 1
                    if board[1][0] == enemy or board[1][2] == enemy:
                        possibilities -= 1
                else: 
                    possibilities = 2
                    if j == 0: # i=1, j=0
                        if board[0][0] == enemy or board[2][0] == enemy:
                            possibilities -= 1
                        if board[1][1] == enemy or board[1][2] == enemy:
                            possibilities -= 1
                    else: # i=1, j=2
                        if board[0][2] == enemy or board[2][2] == enemy:
                            possibilities -= 1
                        if board[1][0] == enemy or board[1][1] == enemy:
                            possibilities -= 1
            else: 
                if i == 0:
                    if j == 1: # i=0, j=1
                        possibilities = 2
                        if board[0][0] == enemy or board[0][2] == enemy:
                            possibilities -= 1
                        if board[1][1] == enemy or board[2][1] == enemy:
                            possibilities -= 1
                    else:
                        possibilities = 3
                        if j == 0: # i=0, j=0
                            if board[1][0] == enemy or board[2][0] == enemy:
                                possibilities -= 1
                            if board[1][1] == enemy or board[2][2] == enemy:
                                possibilities -= 1
                            if board[0][1] == enemy or board[0][2] == enemy:
                                possibilities -= 1
                        else: # i=0, j=2
                            if board[0][0] == enemy or board[0][1] == enemy:
                                possibilities -= 1
                            if board[2][0] == enemy or board[1][1] == enemy:
                                possibilities -= 1
                            if board[1][2] == enemy or board[2][2] == enemy:
                                possibilities -= 1
                else:
                    if j == 1: # i=2, j=1
                        possibilities = 2
                        if board[2][0] == enemy or board[2][2] == enemy:
                            possibilities -= 1
                        if board[0][1] == enemy or board[1][1] == enemy:
                            possibilities -= 1
                    else: 
                        possibilities = 3
                        if j == 0: # i=2, j=0
                            if board[0][0] == enemy or board[1][0] == enemy:
                                possibilities -= 1
                            if board[1][1] == enemy or board[0][2] == enemy:
                                possibilities -= 1
                            if board[2][1] == enemy or board[2][2] == enemy:
                                possibilities -= 1
                        else: # i=2 j=2
                            if board[2][0] == enemy or board[2][1] == enemy:
                                possibilities -= 1
                            if board[0][0] == enemy or board[1][1] == enemy:
                                possibilities -= 1
                            if board[0][2] == enemy or board[1][2] == enemy:
                                possibilities -= 1
            possibList[i][j] = possibilities
    return possibList

def makeMove(bigBoard):
    global area, bigSymbols
    if area == 0:
        print("Select board: ")
        while True:
            selected = input()
            if selected.isdigit():
                selected = int(selected)
                if 1 <= selected <= 9:
                    if 1 <= selected <= 3:
                        row = 0
                        col = selected - 1
                    elif 4 <= selected <= 6:
                        row = 1
                        col = selected - 4
                    else:
                        row = 2
                        col = selected - 7
                    if bigSymbols[row][col] == " ":
                        break;
        area = int(selected)

    print("Select area on board " + str(area) + ":") 
    while True:
        selected = input()
        if selected.isdigit():
            if 1 <= int(selected) <= 9:
                selected = int(selected)
                if 1 <= area <= 3:
                    row = 0
                    col = area - 1
                elif 4 <= area <= 6:
                    row = 1
                    col = area - 4
                else:
                    row = 2
                    col = area - 7
                if 1 <= selected <= 3:
                    row2 = 0
                    col2 = selected - 1
                elif 4 <= selected <= 6:
                    row2 = 1
                    col2 = selected - 4
                else:
                    row2 = 2
                    col2 = selected - 7
                if bigBoard[row][col][row2][col2] == " ":
                    bigBoard[row][col][row2][col2] = "x"
                    if find3Symbols(bigBoard[row][col], "x"):
                        bigSymbols[row][col] = "x"
                    elif boardFull(bigBoard[row][col]):
                        bigSymbols[row][col] = "F"
                    if bigSymbols[row2][col2] != " ":
                        area = 0
                    else:
                        area = selected
                    break;
                else:
                    print("This place isn't free. Try again: ")

def makeSmallBoard():
    return [[" " for _ in range(3)] for _ in range(3)]

def showSmallBoard(board):
    for row in board:
        print(row[0], row[1], row[2])

def makeBigBoard():
    return [[makeSmallBoard() for _ in range(3)] for _ in range(3)]

def showBigBoard(bigBoard):
    global bigSymbols
    print("+-----------------+")
    for i in range(3):
        for k in range(3):
            line = "| " 
            for j in range(3):
                line += bigBoard[i][j][k][0] + bigBoard[i][j][k][1] + bigBoard[i][j][k][2] + " | "
            print(line)
        print("+-----------------+")

if __name__ == "__main__":
    main()