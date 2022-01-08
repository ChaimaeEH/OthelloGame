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
    























'''
Main Programm 2: (je ne l' ai pas encore vu en détail)
'''


def trace_jouer_en_hasards():
    """
    pour voir si commencer la partie impacte le résultat, 
    les deux joueurs choisissent jouent aléatoirement.
    Un fichier .csv et deux graphes du pourcentage de 
    victoires sont générés.
    """
    def jouer_en_hasards(firstPlayer):
        print('firstPlayer = ', firstPlayer)
        turn = firstPlayer
        initial_state = resetBoard()  # état initial du plateau avec les 2 premiers 'X' et 'O'
        computer1Tile, computer2Tile = ['X', 'O']  # a modifier après mais en gros c'est là qu'on decide que 'X' joue en premier et que computer1 est 'X' et computer2 est 'O'
        current_state = initial_state  # état de départ est l'état initial
        while not is_game_over(current_state):  # tant que le jeu n'est pas fini
            if turn == 'X':
                # root = MonteCarloTreeSearchNode(state=current_state, tile=computer1Tile)  # get toutes les actions possibles
                possible_moves = get_legal_actions(current_state, computer1Tile)
    
                if possible_moves != []:
                    action = possible_moves[np.random.randint(len(possible_moves))]
                    flipTiles(current_state, computer1Tile, action[0], action[1])
    
                if get_legal_actions(current_state, computer2Tile) != []:
                    turn = 'O'
    
            else:
                # root = MonteCarloTreeSearchNode(state=current_state, tile=computer2Tile)
                # selected_node = root.best_action(simulation_no2, c_param2)
                # current_state = getBoardCopy(selected_node.state)
                possible_moves = get_legal_actions(current_state, computer2Tile)
    
                if possible_moves != []:
                    action = possible_moves[np.random.randint(len(possible_moves))]
                    flipTiles(current_state, computer2Tile, action[0], action[1])
    
                if get_legal_actions(current_state, computer1Tile) != []:
                    turn = 'X'
        """
        Display the final score
        """
        drawBoard(current_state)
        showPoints_2ordi(current_state, computer1Tile, computer2Tile)
        print(getScoreOfBoard(current_state))
    
        return getScoreOfBoard(current_state)
    
    def jouer_en_hasards_tracer(firstPlayer,f):
    
        nb_partie = 5
        nb_gain_x = 0
        nb_gain_o = 0
        nb_gain_nul = 0
        X = []
        Y = []
        N = []
        for i in range(nb_partie):
            print('Plateau final pour la partie {}/{}'.format(i + 1, nb_partie))
            score = jouer_en_hasards(firstPlayer)
            if score['X'] > score['O']:
                nb_gain_x += 1
            elif score['O'] > score['X']:
                nb_gain_o += 1
            else:
                nb_gain_nul += 1
            X.append(nb_gain_x / (i + 1))
            Y.append(nb_gain_o / (i + 1))
            N.append(nb_gain_nul / (i + 1))
            f.write('{}, {}, {}, {}, {}'.format(firstPlayer, i+1, nb_gain_x, nb_gain_o, nb_gain_nul)) # enregister par lgne
            f.write('\n')
    
        plt.plot(list(range(1, nb_partie + 1)), X, label='X', color='pink')
        plt.plot(list(range(1, nb_partie + 1)), Y, label='O', color='purple')
        plt.plot(list(range(1, nb_partie + 1)), N, label='nul', color='red')
        plt.plot(list(range(1, nb_partie + 1)), [0.5] * nb_partie, color='black')  # la limite vers laquelle ça tend
        plt.ylabel('Pourcentage de gain de parties')
        plt.xlabel('Nombre de parties ')
        plt.title('Evolution du pourcentage de victoire en fonction du nombre de parties ({} commence)'.format(firstPlayer))
        plt.grid()  # ajouter une grille au graphique
        plt.legend()
        # plt.show()
        plt.savefig('{}.png'.format(firstPlayer), format='png', dpi=300)
        plt.close()
    
    
        return
    
    # jour_en_hasards('X')
    # jour_en_hasards('O')
    
    # f = open('test.csv','w', newline='\n') # si on veut generer a nouveau 
    f = open('test.csv','a', newline='\n') # si on veut enregistrer dans le meme fichier
    
    colonnes = 'firstPlayer, nb_partie, nb_gain_x, nb_gain_o, nb_gain_nul\n'
    f.write(colonnes)
    jouer_en_hasards_tracer('X',f)
    jouer_en_hasards_tracer('O',f)
    
    f.close()
    
    return



def trace_jouer_avec_simulation1():
    """
    ordi1 un joue avec simulation, ordi2 joue en hasards
    ordi1 est toujours X
    enregistrer un ficher csv et deux graphs
    :return:
    """
    def jouer_simulation1(firstPlayer, simulation_no1, c_param1):

        print('firstPlayer = ', firstPlayer)
        turn = firstPlayer
        initial_state = resetBoard()  # état initial du plateau avec les 2 premiers 'X' et 'O'
        computer1Tile, computer2Tile = ['X', 'O']  # a modifier après mais en gros c'est là qu'on decide que 'X' joue en premier et que computer1 est 'X' et computer2 est 'O'
        current_state = initial_state  # état de départ est l'état initial
        while not is_game_over(current_state):  # tant que le jeu n'est pas fini
            if turn == 'X':
                root = MonteCarloTreeSearchNode(state=current_state, tile=computer1Tile)  # get toutes les actions possibles
                selected_node = root.best_action(simulation_no1, c_param1)
                current_state = getBoardCopy(selected_node.state)

                if get_legal_actions(current_state, computer2Tile) != []:
                    turn = 'O'

            else:
                # root = MonteCarloTreeSearchNode(state=current_state, tile=computer2Tile)
                # selected_node = root.best_action(simulation_no2, c_param2)
                # current_state = getBoardCopy(selected_node.state)
                possible_moves = get_legal_actions(current_state, computer2Tile)

                if possible_moves != []:
                    action = possible_moves[np.random.randint(len(possible_moves))]
                    flipTiles(current_state, computer2Tile, action[0], action[1])

                if get_legal_actions(current_state, computer1Tile) != []:
                    turn = 'X'
        """
        Display the final score
        """
        drawBoard(current_state)
        showPoints_2ordi(current_state, computer1Tile, computer2Tile)
        print(getScoreOfBoard(current_state))

        return getScoreOfBoard(current_state)

    def jouer_simulation1_tracer(firstPlayer,f):
        nb_partie = 5
        simulation_no1 = 11
        c_param1 = 1.5
        for s in range(10, simulation_no1+1):
            for c in list(np.arange(0.1, c_param1, 0.5)):
                nb_gain_x = 0
                nb_gain_o = 0
                nb_gain_nul = 0
                X = []
                Y = []
                N = []
                for i in range(nb_partie):
                    print('Plateau final pour la partie {}/{}'.format(i + 1, nb_partie))
                    score = jouer_simulation1(firstPlayer, s, c)
                    if score['X'] > score['O']:
                        nb_gain_x += 1
                    elif score['O'] > score['X']:
                        nb_gain_o += 1
                    else:
                        nb_gain_nul += 1

                    X.append(nb_gain_x / (i + 1))
                    Y.append(nb_gain_o / (i + 1))
                    N.append(nb_gain_nul / (i + 1))
                    f.write('{}, {}, {}, {}, {}, {}, {}'.format(firstPlayer, s, c, i+1, nb_gain_x, nb_gain_o, nb_gain_nul)) # enregister par lgne
                    f.write('\n')
                    print('simulation_no1 : {}, c_param1 : {}, nb_partie : {}'.format(s,c,i+1))

            plt.plot(list(range(1, nb_partie + 1)), X, label='X_{}_{}'.format(s, c))
            plt.plot(list(range(1, nb_partie + 1)), Y, label='O')
            plt.plot(list(range(1, nb_partie + 1)), N, label='nul')
            plt.plot(list(range(1, nb_partie + 1)), [0.5] * nb_partie, color='black')  # la limite vers laquelle ça tend

        plt.ylabel('Pourcentage de gain de parties')
        plt.xlabel('Nombre de parties ')
        plt.title('Evolution du pourcentage de victoire en fonction du nombre de parties ({} commence)'.format(firstPlayer))
        plt.grid()  # ajouter une grille au graphique
        plt.legend()
        # plt.show()
        plt.savefig('{}.png'.format(firstPlayer), format='png', dpi=300)
        plt.close()


        return

    # jour_en_hasards('X')
    # jour_en_hasards('O')

    # f = open('test02.csv','w', newline='\n') # si on veut generer a nouveau
    f = open('test02.csv','a', newline='\n') # si on veut enregistrer dans le meme fichier

    colonnes = 'firstPlayer, simulation_no1, c_param1, nb_partie, nb_gain_x, nb_gain_o, nb_gain_nul\n'
    f.write(colonnes)
    jouer_simulation1_tracer('X', f)
    jouer_simulation1_tracer('O', f)

    f.close()

    return


#trace_jouer_avec_simulation1()