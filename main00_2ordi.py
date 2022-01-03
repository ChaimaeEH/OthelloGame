#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on .....

@author: Chaimae ..., Kexin LI, Pauline ....
"""




#-------------------------
# import class
#-------------------------

from class00 import MonteCarloTreeSearchNode

# -------------------------
# import fonctions
# -------------------------
from fonctions00 import drawBoard, resetBoard, isOnBoard, getBoardCopy, \
    enterPlayerTile, getPlayerMove, enterTileOrdre,\
    getHintsBoard, showPoints, getScoreOfBoard, \
    is_game_over, get_legal_actions, isValidMove, move, flipTiles, \
    playAgain, showPoints_2ordi

import numpy as np


#-------------------------
# main fonction
#-------------------------


# def main():
#     # global showHints
#     print("===============")
#     print("  Bienvenue !")
#     print('===============')
#     while True:
#         initial_state = resetBoard()
#
#         playerTile, computerTile, turn = enterTileOrdre()
#
#         current_state = initial_state
#         drawBoard(current_state)
#         showPoints_2ordi(current_state, playerTile, computerTile)
#
#         while not is_game_over(current_state):
#             if turn == 'player':
#                 print('A X jouer')
#
#                 root = MonteCarloTreeSearchNode(state=current_state, tile=playerTile)
#
#                 selected_node = root.best_action()
#                 current_state = getBoardCopy(selected_node.state)
#
#                 input('Press Enter to see X\'s move.')
#                 drawBoard(current_state)
#                 showPoints_2ordi(current_state, playerTile, computerTile)
#
#                 if get_legal_actions(current_state, computerTile) != []:
#                     turn = 'computer'
#
#             else:
#                 print('A O jouer')
#
#                 root = MonteCarloTreeSearchNode(state=current_state, tile=computerTile)
#                 selected_node = root.best_action()
#                 current_state = getBoardCopy(selected_node.state)
#
#                 input('Press Enter to see O\'s move.')
#                 drawBoard(current_state)
#                 showPoints_2ordi(current_state, playerTile, computerTile)
#
#                 if get_legal_actions(current_state, playerTile) != []:
#                     turn = 'player'
#
#         """
#         Display the final score
#         """
#         print("===============")
#         print("Resultat")
#         print('===============')
#         drawBoard(current_state)
#         showPoints_2ordi(current_state, playerTile, computerTile)
#
#         if not playAgain():
#             break


def main():
    # global showHints
    print("===============")
    print("  Bienvenue !")
    print('===============')
    while True:
        initial_state = resetBoard()  # état initial du plateau avec les 2 premiers 'X' et 'O'
        computer1Tile, computer2Tile, turn = ['X', 'O',
                                              'X']  # a modifier après mais en gros c'est là qu'on decide que 'X' joue en premier et que computer1 est 'X' et computer2 est 'O'
        current_state = initial_state  # état de départ est l'état initial
        while not is_game_over(current_state):  # tant que le jeu n'est pas fini
            if turn == 'X':
                print('Computer 1 joue :')

                root = MonteCarloTreeSearchNode(state=current_state,
                                                tile=computer1Tile)  # get toutes les actions possibles
                print(root._untried_actions)
                selected_node = root.best_action()
                print(root.children)
                print([(c.q() / c.n()) + 0.1 * np.sqrt((2 * np.log(root.n()) / c.n())) for c in root.children])
                current_state = getBoardCopy(selected_node.state)
                if get_legal_actions(current_state, computer2Tile) != []:
                    turn = 'O'

                showPoints(current_state, computer1Tile, computer2Tile)  # afficher le score après chaque manche
                drawBoard(current_state)  # afficher le plateau à chaque manche


            else:
                print('Computer 2 joue :')
                root = MonteCarloTreeSearchNode(state=current_state, tile=computer2Tile)
                selected_node = root.best_action()
                current_state = getBoardCopy(selected_node.state)
                if get_legal_actions(current_state, computer1Tile) != []:
                    turn = 'X'

                showPoints(current_state, computer1Tile, computer2Tile)  # afficher le score après chaque manche
                drawBoard(current_state)  # afficher le plateau à chaque manche

        """
        Display the final score
        """
        print("===============")
        print("Resultat")
        print('===============')
        drawBoard(current_state)
        showPoints(current_state, computer1Tile, computer2Tile)

        if not playAgain():
            break


#-------------------------
# commencer jouer
#-------------------------

main()