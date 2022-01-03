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
    enterPlayerTile, getPlayerMove, \
    getHintsBoard, showPoints, getScoreOfBoard, \
    is_game_over, get_legal_actions, isValidMove, move, flipTiles, \
    playAgain


#-------------------------
# main fonction
#-------------------------


def main():
    # global showHints
    print("===============")
    print("  Bienvenue !")
    print('===============')
    while True:
        initial_state = resetBoard()
        playerTile, computerTile, turn = enterPlayerTile()
        showHints = False
        # print('turn= ', turn)
        # initialiserGame()
        # current_state = MonteCarloTreeSearchNode(state=initial_state)
        current_state = initial_state
        while not is_game_over(current_state):
            if turn == 'player':
                print('A player jouer')
                # current_state.tile = playerTile

                # dessiner le board et les points
                if showHints:
                    hintsBoard = getHintsBoard(current_state, playerTile)
                    drawBoard(hintsBoard)
                else:
                    drawBoard(current_state)
                showPoints(current_state, playerTile, computerTile)

                # demander l<action
                res = getPlayerMove(current_state, playerTile, showHints) # rerurn [x, y] saisi, avec showHints
                action = res[0]
                showHints =res[1]

                flipTiles(current_state, playerTile, action[0], action[1])

                drawBoard(current_state)

                if get_legal_actions(current_state, computerTile) != []:
                    turn = 'computer'

            else:
                print('A computer jouer')
                # current_state.tile = computerTile
                # selected_node = current_state.best_action()
                # drawBoard(current_state)
                # showPoints(current_state, playerTile, computerTile)
                # input('Press Enter to see the computer\'s move.')
                root = MonteCarloTreeSearchNode(state=current_state, tile=computerTile)
                selected_node = root.best_action()
                current_state = getBoardCopy(selected_node.state)
                # best_child = current_state.best_action()
                # action = move(current_state.state, tour_joueur, playerTile)
                if get_legal_actions(current_state, playerTile) != []:
                    turn = 'player'

        """
        Display the final score
        """
        print("===============")
        print("Resultat")
        print('===============')
        drawBoard(current_state)
        showPoints(current_state, playerTile, computerTile)

        if not playAgain():
            break

#-------------------------
# commencer jouer
#-------------------------

main()