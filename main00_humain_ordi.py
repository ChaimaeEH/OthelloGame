#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/01/2022

@author: Chaimae EL HOUJJAJI, Kexin LI, Pauline TURK
"""




#-------------------------
# import class
#-------------------------

from class00 import MonteCarloTreeSearchNode

# -------------------------
# import fonctions
# -------------------------
from fonctions00 import drawBoard, resetBoard, getBoardCopy, \
    enterPlayerTile, getPlayerMove, \
    getHintsBoard, showPoints, \
    is_game_over, get_legal_actions, flipTiles, \
    playAgain


#-------------------------
# main fonction
#-------------------------


def main(simulation_no, c_param):                      
    print("===============")
    print("  Welcome !")
    print('===============')
    while True:
        initial_state = resetBoard()
        playerTile, computerTile, turn = enterPlayerTile()
        showHints = False

        current_state = initial_state
        while not is_game_over(current_state):
            if turn == 'player':
                print('It\'s your turn')

                # dessiner le plateau et les points
                if showHints:
                    hintsBoard = getHintsBoard(current_state, playerTile)
                    drawBoard(hintsBoard)
                else:
                    drawBoard(current_state)
                showPoints(current_state, playerTile, computerTile)

                # demander l'action au joueur
                res = getPlayerMove(current_state, playerTile, showHints) # return [x, y] saisi, avec showHints
                action = res[0]
                showHints =res[1]

                flipTiles(current_state, playerTile, action[0], action[1])

                drawBoard(current_state)

                if get_legal_actions(current_state, computerTile) != []:
                    turn = 'computer'

            else:
                print('It\'s the computer\'s turn')
                root = MonteCarloTreeSearchNode(state=current_state, tile=computerTile)
                selected_node = root.best_action(simulation_no, c_param)                                            
                current_state = getBoardCopy(selected_node.state)
                if get_legal_actions(current_state, playerTile) != []:
                    turn = 'player'
        
        #afficher le résultat
        print("===============")
        print("Result")
        print('===============')
        drawBoard(current_state)
        showPoints(current_state, playerTile, computerTile)

        if not playAgain():
            break

#-------------------------
# Jouer une partie
#-------------------------
simulation_no = 10
c_param = 0.5
main(simulation_no, c_param)
