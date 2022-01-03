#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on .....

@author: Chaimae ..., Kexin LI, Pauline ....
"""
import sys

#-------------------------
# fonctions hors le class
#-------------------------


def drawBoard(board):
    """
    This function prints out the board that it was passed. Returns None.
    """
    HLINE = '  +---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |'
    print('    0   1   2   3   4   5')
    print(HLINE)
    for x in range(6):
        # print(VLINE)
        print(x, end=' ')
        for y in range(6):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        # print(VLINE)
        print(HLINE)


def resetBoard():
    """
    Creates a brand new, blank board data structure.
    """
    board = []
    for i in range(6):
        board.append([' '] * 6)

    board[2][2] = 'X'
    board[2][3] = 'O'
    board[3][2] = 'O'
    board[3][3] = 'X'

    return board



def isOnBoard(x, y):
    """
    Returns True if the coordinates are located on the board.
    """
    return x >= 0 and x <= 5 and y >= 0 and y <= 5



def getBoardCopy(board):
    dupeBoard = resetBoard()
    for x in range(6):
        for y in range(6):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard


def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O ? X go first')
        tile = input().upper()
    if tile == 'X':
        turn = 'player'
        print('Player : X, Computer : O')
        print('Player go first')
        return ['X', 'O', turn]
    else:
        turn = 'computer'
        print('Player : O, Computer : X')
        print('Computer go first')
        return ['O', 'X', turn]



def is_game_over(board):
    '''
    C'est la condition de fin de partie et cela dépend de votre jeu. Retourne vrai ou faux
    The game ends when a player either cannot make a move, or the board is completely full.
    The player with the most tiles of their color wins.
    '''
    end = True  # the board is full
    # for i in range(6):
    #     for j in range(6):
    #         if self.state[i][j] != ' ':  # si il y a au moins une case vide
    #             end = False
    if len(get_legal_actions(board, 'X')) != 0 or len(get_legal_actions(board, 'O')) != 0:
        end = False
    return end



def is_game_over(board):
    '''
    C'est la condition de fin de partie et cela dépend de votre jeu. Retourne vrai ou faux
    The game ends when a player either cannot make a move, or the board is completely full.
    The player with the most tiles of their color wins.
    '''
    end = True  # the board is full
    for i in range(6):
        for j in range(6):
            if board[i][j] != ' ':  # si il y a au moins une case vide，end = False
                end = False
    return len(get_legal_actions(board, 'X')) == 0 or end or len(get_legal_actions(board, 'O')) == 0




def get_legal_actions(board, tile):
    '''
    Construit une liste de toutes les actions possibles à partir de l'état actuel. Retourne une liste.
    '''
    # if self.tour_joueur % 2 == 0:
    #     tile = 'X'
    # else:
    #     tile = 'O'
    possible_positions = []
    for x in range(6):
        for y in range(6):
            if isValidMove(board, tile, x, y) != False:
                possible_positions.append([x, y])

    return possible_positions



def isValidMove(board, tile, xstart, ystart):
    """
    Returns False if the player's move on space xstart, ystart is invalid.
    If it is a valid move, returns a list of spaces that would become the player's if they made a move here.

    """
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile  # temporarily set the tile on the board.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            while isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
            if isOnBoard(x, y) and board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' '  # restore the empty space
    if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip





def getPlayerMove(board, playerTile, showHints):
    # global showHints
    hintsBoard = getHintsBoard(board, playerTile)
    Digits1To6 = '0 1 2 3 4 5'.split()
    while True:
        print('Enter your move, \n or (1) type quit to end the game, \n or (2) hints to turn off/on hints, \n or (3) db to draw the present board')
        move = input().lower()
        if move == 'quit':
            print('Thanks for playing!')
            sys.exit(0)
        if move == 'hints':
            showHints = not showHints
            print('showHints : ', showHints)
            if showHints:
                drawBoard(hintsBoard)
            continue
        if move == 'db':
            if showHints:
                drawBoard(hintsBoard)
            else:
                drawBoard(board)
            continue
        if len(move) == 2 and move[0] in Digits1To6 and move[1] in Digits1To6:
            x = int(move[0])
            y = int(move[1])
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (0-5), then the y digit (0-5).')
            print('For example, 51 will be the top-right corner.')

    return [[x, y], showHints]


def move(board, tour_joueur, tile):
    '''
    Change l'état de votre plateau avec une nouvelle valeur. Pour un jeu de Tic Tac Toe normal, il peut
    s'agir d'un tableau 3 par 3 dont tous les éléments sont initialement à 0. 0 signifie que la position
    du plateau est vide. Si vous placez x sur la rangée 2, colonne 3, alors ce sera quelque chose comme
    plateau[2][3] = 1, où 1 représente ce x est placé.
    Renvoie le nouvel état après avoir effectué un déplacement.
    '''
    if tour_joueur % 2 == 0:
        print('tour_joueur == 0')

        # print('Joueur X a joué et placé son pion à la ligne', action[1], ' et à la colonne ', action[0])
    else:
        print('tour_joueur == 1')
        # tile = 'O'
        # print('Joueur O a joué et placé son pion à la ligne', action[1], ' et à la colonne ', action[0])

    # self.state = makeMove(self.state, tile, action[0], action[1])
    # tour_joueur += 1
    # drawBoard(self.states)
    # print(self.game_result())
    # return action


def flipTiles(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    # return True


# def makeMove(board, tile, xstart, ystart):
#     """
#     Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
#     Returns False if this is an invalid move, True if it is valid.
#     """
#     tilesToFlip = isValidMove(board, tile, xstart, ystart)
#     if tilesToFlip == False:
#         return False
#     board[xstart][ystart] = tile
#     for x, y in tilesToFlip:
#         board[x][y] = tile
#     return board




def getHintsBoard(board, tile):
    dupeBoard = getBoardCopy(board)

    for x, y in get_legal_actions(dupeBoard, tile):
        dupeBoard[x][y] = '.'

    return dupeBoard


def showPoints(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))

def showPoints_2ordi(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('Joueur %s have %s points. Joueur %s has %s points.' % (playerTile, scores[playerTile], computerTile, scores[computerTile]))


def getScoreOfBoard(board):
    """
    Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    """
    xscore = 0
    oscore = 0
    for x in range(6):
        for y in range(6):
            if board[x][y] == 'X':
                xscore += 1
            elif board[x][y] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}


def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def enterTileOrdre():
    tile = ''
    turn = 'player'
    while not (tile == 'X' or tile == 'O'):
        print('Do you want X or O go first ?')
        tile = input().upper()
    if tile == 'X':
        # turn = 'player'
        # print('Computer 1 : X, Computer 2 : O')
        print('X go first')
        return ['X', 'O', turn]
    else:
        # turn = 'computer'
        # print('Computer 1 : O, CComputer 2 : X')
        print('O go first')
        return ['O', 'X', turn]

