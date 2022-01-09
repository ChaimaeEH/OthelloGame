# -------------------------
# import class
# -------------------------

from class00 import MonteCarloTreeSearchNode



# -------------------------
# import fonctions
# -------------------------
from fonctions00 import drawBoard, resetBoard, getBoardCopy, \
    enterPlayerTile, getPlayerMove, \
    getHintsBoard, showPoints, \
    is_game_over, get_legal_actions, flipTiles, \
    playAgain, showPoints_2ordi, getScoreOfBoard

import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd





def jouer_avec_simulation_1_enregistrer(nb_partie,
                                       simulation_no1, c_param1,
                                       simulation_no2 = 11, c_param2 = 1.5 ,
                                       simulation1_min=1, simulation1_pas=10,
                                       c_param1_min=0, c_param1_pas=0.5):
    """
       - L'ordinateur 1 joue avec un nombre de simulations que l'on fait varier,
         et pour différentes valeurs du paramètre d'exploration.
         Pour chaque couple (nombre de simulation, paramètre d'exploration),
       - L'ordinateur 1 joue contre l'ordinateur 2.
       - L'ordinateur 1 joue toujours avec 'X'.
       
       
       - L'ordinateur 2 a les mêmes possibilités que le 1, mais on choisi de lui donner des valeurs par défaut
         pour évaluer le comportement de l'ordinateur 1 lorsqu'on fait varier ses paramètres.
         Ainsi pour l'ordinateur 2 on donne par défaut :
         - un nombre de simulations de 11
         - un paramètre d'exploitation de 1.5 (proche de sqrt(2) qui est la valeur par défaut dans MCTS)
       

    Args:
        nb_partie (int): nombre de parties jouées entre l'ordinateur 1 et 2 pour chaque couple de paramètres testés.
        simulation_no1 (int): nombre de simulations avant chaque coup joué pour l'ordinateur 1.
        c_param1 (float): paramètre d'exploration pour l'ordinateur 1.
        
        simulation_no2 (int, optional): nombre de simulations avant chaque coup joué pour l'ordinateur 2. Defaults to 11.
        c_param2 (float, optional): paramètre d'exploration pour l'ordinateur 2. Defaults to 1.41.
        simulation1_min (int, optional): nombre minimal de simulations avant chaque coup joué pour l'ordinateur 1. Defaults to 1.
        simulation1_pas (int, optional): pas d'incrémentation du nombre de simulations pour l'ordinateur 1. Defaults to 10. 
        c_param1_min (float, optional): [description]. paramètre d'exploration minimpal pour l'ordinateur 1. Defaults to 0.
        c_param1_pas (float, optional): pas d'incrémentation paramètre d'exploration pour l'ordinateur 1. Defaults to 0.5.
    """  
    
    def jouer_simulation1(simulation_no1,c_param1):
        turn = 'X'                    # c'est 'X' qui joue le premier coup
        initial_state = resetBoard()  # état initial du plateau avec les 2 premiers 'X' et 'O'
        computer1Tile, computer2Tile = ['X', 'O']  
        current_state = initial_state  # état de départ est l'état initial
        while not is_game_over(current_state):  # tant que le jeu n'est pas fini
            if turn == 'X':
                root = MonteCarloTreeSearchNode(state=current_state, tile=computer1Tile)  
                selected_node = root.best_action(simulation_no1, c_param1)
                current_state = getBoardCopy(selected_node.state)

                if get_legal_actions(current_state, computer2Tile) != []:
                    turn = 'O'

            else:
                root = MonteCarloTreeSearchNode(state=current_state, tile=computer2Tile)
                selected_node = root.best_action(simulation_no2, c_param2)
                current_state = getBoardCopy(selected_node.state)

                if get_legal_actions(current_state, computer1Tile) != []:
                    turn = 'X'
     
        drawBoard(current_state)
        showPoints_2ordi(current_state, computer1Tile, computer2Tile)
        print(getScoreOfBoard(current_state))

        return getScoreOfBoard(current_state)

    def jouer_simulation1_tracer():
        for c in np.arange(c_param1_min, c_param1, c_param1_pas):
            X = []
            for s in range(simulation1_min, simulation_no1 + 1, simulation1_pas):
                nb_gain_x = 0
                nb_gain_o = 0
                nb_gain_nul = 0
                for i in range(nb_partie):
                    print('Plateau final pour la partie {}/{}'.format(i + 1, nb_partie))
                    score = jouer_simulation1(s, c)
                    if score['X'] > score['O']:
                        nb_gain_x += 1
                    elif score['O'] > score['X']:
                        nb_gain_o += 1
                    else:
                        nb_gain_nul += 1

                X.append(((nb_gain_x)/ (nb_partie-nb_gain_nul))*100) # enlever les parties nulles
                print('simulation_no1 : {}, c_param1 : {}'.format(s,c))

            plt.plot(list(range(simulation1_min, simulation_no1+1, simulation1_pas)), X, label='c_param_{}'.format(c))
      
        plt.ylabel('Parties gagnées en %')
        plt.xlabel('Nombre de simulations')
        plt.title('Evolution du pourcentage de victoires du joueur X en fonction\n du nombre de simulations et du paramètre d\'exploration ({} parties)'.format(nb_partie), 
                   fontdict={'weight': 'bold',
                             'size': 11})
        plt.grid()  
        plt.legend()
        plt.savefig('fun06_1 simulation_gains_X ({} parties).png'.format(nb_partie), format='png', dpi=300)
        plt.close()
       
    jouer_simulation1_tracer()
 




'''
Main Programm:
'''
nb_partie = 100
simulation_no1 = 101
c_param1 = 3

jouer_avec_simulation_1_enregistrer(nb_partie,
                                    simulation_no1, c_param1)
   
    
    
    
    
