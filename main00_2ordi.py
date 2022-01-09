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
import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# import fonctions
# -------------------------

from fonctions00 import drawBoard, resetBoard, getBoardCopy, \
    enterPlayerTile, getPlayerMove, \
    getHintsBoard, showPoints, \
    is_game_over, get_legal_actions,flipTiles, \
    playAgain, showPoints_2ordi, getScoreOfBoard


#-------------------------------------
# main fonction : 2 ordinateurs
#-------------------------------------

def une_partie(simulation_no1, simulation_no2, c_param1, c_param2):
    """Faire jouer 2 ordinateurs l'un contre l'autre

    Args:
        simulation_no1 (int): nombre d'intérations de MCTS faite à chaque tour de l'ordinateur 1
        simulation_no2 ([int]): nombre d'intérations de MCTS faite à chaque tour de l'ordinateur 2
        c_param1 (float): paramètre d'exploration de l'ordinateur 1
        c_param2 (float): paramètre d'exploration de l'ordinateur 2

    Returns:
        dic: dictionnaire du score de chaque ordinateur en fin de partie
    """
                   
    initial_state = resetBoard()                         # initialisation du plateau avec les 2 premiers 'X' et 'O'
    
    computer1Tile, computer2Tile, turn = ['X', 'O', 'X'] # l'ordinateur 1 joue avec 'X'
                                                         # l'ordinateur 2 joue avec 'O'
                                                         # 'X' commence à jouer
                                                         
    current_state = initial_state                        # L'état de départ est l'état initial 
    
    while not is_game_over(current_state):               # Tant que la partie n'est pas finie
        if turn == 'X':                                                              # Si c'est le tour de l'ordinateur 1
            root = MonteCarloTreeSearchNode(state=current_state, tile=computer1Tile) # Générer son Tree search en sa configuration de jeu
            selected_node = root.best_action(simulation_no1, c_param1)                # Itérer le MCTS selone les paramètres choisis pour l'ordinateur 1
                                                                                     # et choix du meilleur coup connu selon l'arbre développé
            current_state = getBoardCopy(selected_node.state)
            if get_legal_actions(current_state, computer2Tile) != []:                # Si dans la nouvelle configuration de jeu l'ordinateur 2 peut jouer
                turn = 'O'                                                           # c'est son tour de jouer
                
        else:                                                                        # Meme logique si c'est le tour de l'ordinateur 2
            root = MonteCarloTreeSearchNode(state=current_state, tile=computer2Tile)
            selected_node = root.best_action(simulation_no2, c_param2)
            current_state = getBoardCopy(selected_node.state)
            if get_legal_actions(current_state, computer1Tile) != []:
                turn = 'X'
  
    drawBoard(current_state)                                       # Afficher l'état final du plateau 
    showPoints_2ordi(current_state, computer1Tile, computer2Tile)  # Afficher le score final de chaque ordinateur
    return getScoreOfBoard(current_state)
    
                    
def main(nb_partie, simulation_no1, simulation_no2, c_param1, c_param2):
    """Faire jouer 2 ordinateurs l'un contre l'autre un nombre de parties
       que l'on peut choisir.
       Et afficher le pourcentage de gains de chaque joueur en fonction
       du nombre de parties jouées.

    Args:
        nb_partie ([type]): [description]
        simulation_no1 (int): nombre d'intérations de MCTS faite à chaque tour de l'ordinateur 1
        simulation_no2 ([int]): nombre d'intérations de MCTS faite à chaque tour de l'ordinateur 2
        c_param1 (float): paramètre d'exploration de l'ordinateur 1
        c_param2 (float): paramètre d'exploration de l'ordinateur 2
    """
    nb_gain_x = 0
    nb_gain_y = 0
    X=[]
    Y=[]
    for i in range (nb_partie):
        print('Plateau final pour la partie {}/{}'.format(i+1,nb_partie))
        score = une_partie(simulation_no1,simulation_no2,c_param1,c_param2)
        if score['X'] > score['O']:
            nb_gain_x += 1
            X.append(nb_gain_x/(i+1))
            Y.append(nb_gain_y/(i+1))
        else :
            nb_gain_y += 1
            X.append(nb_gain_x/(i+1))
            Y.append(nb_gain_y/(i+1))
    plt.plot(list(range(1,nb_partie+1)),X, label = 'X', color = 'pink')
    plt.plot(list(range(1,nb_partie+1)),Y, label = 'Y', color = 'purple')
    plt.plot(list(range(1,nb_partie+1)),[0.5]*nb_partie, color = 'black') # la limite vers laquelle ça tend 
    plt.ylabel('Pourcentage de gain de parties')
    plt.xlabel('Nombre de parties ')
    plt.title('Evolution du pourcentage de victoires en fonction du nombre de parties')
    plt.grid() #ajouter une grille au graphique 
    plt.legend()
    plt.show()
    

'''
Main Programm 1:
'''
nb_partie = 5
simulation_no1 = 100
simulation_no2 = 1 
c_param1 = 0.5
c_param2 = 0.5
main(nb_partie,simulation_no1, simulation_no2, c_param1, c_param2)  
