#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/01/2022

@author: Chaimae EL HOUJJAJI, Kexin LI, Pauline TURK
"""

import sys

#-------------------------
# fonctions hors le class
#-------------------------


def drawBoard(board):
    """Affiche le plateau de jeu dans son état actuel.

    Args:
        board (list): plateau de jeu actuel.
    """
    HLINE = '  +---+---+---+---+---+---+'
    print('    0   1   2   3   4   5')
    print(HLINE)
    for x in range(6):
        print(x, end=' ')
        for y in range(6):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(HLINE)


def resetBoard():
    """Réinitialisation du plateau de jeu.

    Returns:
        list: plateau de jeu réinitialisé.
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
    """Teste si les coordonnées d'une position
        existent sur le plateau de jeu.

    Args:
        x (int): absicsse
        y (int): ordonnée

    Returns:
        bool: True si la position est sur le plateau de jeu
              False sinon.
    """
    return x >= 0 and x <= 5 and y >= 0 and y <= 5


def getBoardCopy(board):
    """ Génère une copie du plateau de jeu actuel.

    Args:
        board (list): plateau de jeu actuel.

    Returns:
        list: copie du plateau de jeu actuel.
    """
    dupeBoard = resetBoard()
    for x in range(6):
        for y in range(6):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard


def enterPlayerTile():
    """Dans le cas d'une partie jouée entre un humain et l'ordinateur,
       permet à l'humain de choisir entre jouer avec 'X' et donc commencer
       et jouer avec 'O' et donc jouer en second.

    Returns:
        list: [symbole de l'humain, symbole de l'ordinateur, joueur qui va commencer la partie]
    """
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
    """ Conditions de fin de partie:
        plus aucun joueur ne peux jouer
        (en particulier si toutes les cases du plateau de jeu sont occupées)
    Args:
        board (list): plateau de jeu actuel.

    Returns:
        bool: True si la partie est finie
              False sinon.
    """
    end = True       # la partie est terminée
    if len(get_legal_actions(board, 'X')) != 0 or len(get_legal_actions(board, 'O')) != 0:
        end = False  # sauf si au moins un des 2 joueurs peut encore jouer
    return end


def get_legal_actions(board, tile):
    """Construit une liste de toutes les actions possibles à partir de la configuration de
    jeu actuelle pour le joueur dont c'est le tour.

    Args:
        board (list): plateau de jeu actuel.
        tile (str): vaut 'X' ou 'O' et définit à qui est le tour.

    Returns:
        list: liste de toutes les actions possibles à partir de la configuration de
              jeu actuelle pour le joueur dont c'est le tour.
    """
    possible_positions = []
    for x in range(6):
        for y in range(6):
            if isValidMove(board, tile, x, y) != False:
                possible_positions.append([x, y])

    return possible_positions



def isValidMove(board, tile, xstart, ystart):
    """Interdit un coup invalide:
       - qui n'est pas sur le plateau
       - ou qui concerne une case déjà occupée
       - ou qui ne va permettre de récupérer aucune case de l'adversaire

       Et si le coup est valide, renvoie les cases qui seront récupérées
       par le joueur à l'issue de ce coup.

    Args:
        board (list): plateau de jeu actuel.
        tile (str): vaut 'X' ou 'O' et définit à qui est le tour.
        xstart (int): abscisse souhaitée
        ystart (int): ordonnée souhaitée

    Returns:
        bool: False si le mouvement est invalide
        sinon
        list: liste des positions gagnées si ce coup est joué
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
    if len(tilesToFlip) == 0:    # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip





def getPlayerMove(board, playerTile, showHints):
    """Dans le cas d'une partie jouée entre un humain et l'ordinateur,
       permet de récupérer le coup demandé par l'humain.
       Par exemple, s'il veut prendre la case de la ligne 4, colonne 2,
       il devra enter: 42
       ATTENTION: la numérotation des lignes et colonnes commence à 0.

       D'autres options sont disponibles:
       - quiter le jeu en entrant: quit
       - demander à voir ses coups possibles en entrant: hints
       - réafficher l'état du plateau de jeu en entrant: db

    Args:
        board (list): plateau de jeu actuel.
        playerTile (str): vaut 'X' ou 'O' et correspond au symbole de l'humain.
        showHints (bool): indique si les coups possibles doivent etre affichés ou non

    Returns:
        list: coup choisi par le joueur ou une des autres options possibles
    """
    hintsBoard = getHintsBoard(board, playerTile)
    Digits1To6 = '0 1 2 3 4 5'.split()
    while True:
        print('\nEnter your move (ex. for ligne 4, column 2, type: 42)\
              \n- to end the game, type: quit\
              \n- to turn off/on hints, type: hints\
              \n- to draw the present board, type: db')
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
            print('For example, 05 will be the top-right corner.')

    return [[x, y], showHints]


def flipTiles(board, tile, xstart, ystart):
    """Si un coup est validé, la case choisie devient du symbole du joueur qui vient de jouer.
       Il en est de meme pour toutes les cases remportées
       Sinon la fonction renvoie false.

    Args:
        board (list): plateau de jeu actuel.
        tile (str): vaut 'X' ou 'O' et définit à qui est le tour.
        xstart (int): abscisse souhaitée
        ystart (int): ordonnée souhaitée

    Returns:
        bool: False si un coup est invalides
    """
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile


def getHintsBoard(board, tile):
    """Indique par un point toutes les cases qui peuvent
       etre jouées au joueur dont c'est le tour.
       
    Args:
        board (list): plateau de jeu actuel.
        tile (str): vaut 'X' ou 'O' et définit à qui est le tour.

    Returns:
        list: plateau avec des points dans les cases des coups valides
    """
    dupeBoard = getBoardCopy(board)

    for x, y in get_legal_actions(dupeBoard, tile):
        dupeBoard[x][y] = '.'

    return dupeBoard


def showPoints(board, playerTile, computerTile):
    """Affiche le score de l'humain et de l'ordinateur.

    Args:
        board (list): plateau de jeu actuel.
        playerTile (str): vaut 'X' ou 'O' et correspond au symbole de l'humain.
        computerTile (str): vaut 'X' ou 'O' et correspond au symbole de l'ordinateur.
    """
    scores = getScoreOfBoard(board)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))


def showPoints_2ordi(board, playerTile, computerTile):
    """Affiche le score de chaque ordinateur.

    Args:
        board (list): plateau de jeu actuel.
        playerTile (str): vaut 'X' ou 'O' et correspond au symbole du premier ordinateur.
        computerTile (str): vaut 'X' ou 'O' et correspond au symbole du second ordinateur.
    """
    scores = getScoreOfBoard(board)
    print('Computer %s has %s points. Computer %s has %s points.' % (playerTile, scores[playerTile], computerTile, scores[computerTile]))


def getScoreOfBoard(board):
    """Calcul le score de chaque joueur en comptant le nombre de
       cases occupées par chacun.

    Args:
        board ([type]): [description]

    Returns:
        dic: dictionnaire du score de chaque joueur avec pour clef: 'X' et 'O'
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
    """Récupère la réponse de l'utilisateur à la question s'il souhaite
       rejouer une nouvelle partie ou pas.
    Returns:
        bool: True si sa réponse commence par un 'y' ou 'Y'
              False sinon
    """
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

