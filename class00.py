#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on .....

@author: Chaimae ..., Kexin LI, Pauline ....
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import time
# import State as Othello
from collections import defaultdict

# -----------------------------
# import fonctions hors class
# -----------------------------

from fonctions00 import drawBoard, resetBoard, isOnBoard, getBoardCopy, \
    enterPlayerTile, getPlayerMove, \
    getHintsBoard, showPoints, getScoreOfBoard, \
    is_game_over, get_legal_actions, isValidMove, move, flipTiles, \
    playAgain


class MonteCarloTreeSearchNode(object):
    def __init__(self, state, tile=None, parent=None, parent_action=None):
        self.state = state
        self.tile = tile
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        """
        Retourne la liste des actions non essayées d'un état donné. Pour le premier tour de notre jeu, il y a 81
        actions possibles. Pour le deuxième tour, il y en a 8 ou 9. Cela varie dans notre jeu.
        """
        # print('type:', type(self.state))
        # print('type:', type(self.state.states))
        # print('ok:', self.state)
        # print('ok2:', self.state.states)
        # print('AVANT, self._untried_actions', self._untried_actions)
        self._untried_actions = get_legal_actions(self.state, self.tile)
        # print('APRES, self._untried_actions', self._untried_actions)
        return self._untried_actions

    # def is_game_over(self):
    #     '''
    #     C'est la condition de fin de partie et cela dépend de votre jeu. Retourne vrai ou faux
    #     The game ends when a player either cannot make a move, or the board is completely full.
    #     The player with the most tiles of their color wins.
    #     '''
    #     end = True  # the board is full
    #     # for i in range(6):
    #     #     for j in range(6):
    #     #         if self.state[i][j] != ' ':  # si il y a au moins une case vide
    #     #             end = False
    #     if len(get_legal_actions(self.state, 'X')) != 0 or len(get_legal_actions(self.state, 'O')) != 0:
    #         end = False
    #     return end



    def q(self):
        """
        Retourne la différence entre les victoires et les défaites
        """
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        """
        Renvoie le nombre de fois que chaque nœud est visité.
        """
        return self._number_of_visits
    #
    # def expand(self, action):
    #     """
    #     A partir de l'état actuel, l'état suivant est généré en fonction de l'action qui est exécutée. Dans cette
    #     étape, tous les noeuds enfants possibles correspondant aux états générés sont ajoutés au tableau des
    #     enfants et le noeud enfant est renvoyé. Les états qui sont possibles à partir de l'état actuel sont tous
    #     générés et le child_node correspondant à cet état généré est renvoyé.
    #     """
    #     next_state = self.getChildState(action, self.tile)
    #     if self.tile == 'X':
    #         child_tile = 'O'
    #     else:
    #         child_tile = 'X'
    #     child_node = MonteCarloTreeSearchNode(next_state, tile = child_tile, parent=self, parent_action=action)
    #
    #     self.children.append(child_node)
    #     return child_node

    def expand(self):
        """
        A partir de l'état actuel, l'état suivant est généré en fonction de l'action qui est exécutée. Dans cette
        étape, tous les noeuds enfants possibles correspondant aux états générés sont ajoutés au tableau des
        enfants et le noeud enfant est renvoyé. Les états qui sont possibles à partir de l'état actuel sont tous
        générés et le child_node correspondant à cet état généré est renvoyé.
        """
        action = self._untried_actions.pop()  # .pop() enlève et renvoie le dernier élément de la liste
        # next_state = self.state.move(action)
        # child_node = MonteCarloTreeSearchNode(next_state, parent=self, parent_action=action)

        next_state = self.getChildState(action, self.tile)
        if self.tile == 'X':
            child_tile = 'O'
        else:
            child_tile = 'X'

        child_node = MonteCarloTreeSearchNode(next_state, tile=child_tile, parent=self, parent_action=action)
        self.children.append(child_node)

        return child_node




    def getChildState(self, action, tile):
        '''
        Change l'état de votre plateau avec une nouvelle valeur. Pour un jeu de Tic Tac Toe normal, il peut
        s'agir d'un tableau 3 par 3 dont tous les éléments sont initialement à 0. 0 signifie que la position
        du plateau est vide. Si vous placez x sur la rangée 2, colonne 3, alors ce sera quelque chose comme
        plateau[2][3] = 1, où 1 représente ce x est placé.
        Renvoie le nouvel état après avoir effectué un déplacement.
        '''
        # global tour_joueur
        # if tour_joueur % 2 == 0:
        #     tile = 'X'
        #     # print('Joueur X a joué et placé son pion à la ligne', action[1], ' et à la colonne ', action[0])
        # else:
        #     tile = 'O'
        #     # print('Joueur O a joué et placé son pion à la ligne', action[1], ' et à la colonne ', action[0])
        #


        # copier parent state

        child_state = getBoardCopy(self.state)

        flipTiles(child_state, tile, action[0], action[1])

        # drawBoard(child_state)
        # print(self.game_result())
        return child_state






    #
    def is_terminal_node(self):
        """
        Ceci est utilisé pour vérifier si le nœud actuel est terminal ou non. Le nœud terminal est atteint
        lorsque le jeu est terminé.
        """
        return is_game_over(self.state)
    #
    # def rollout(self):
    #     """
    #     À partir de l'état actuel, le jeu entier est simulé jusqu'à ce qu'il y ait un résultat pour le jeu. Le
    #     résultat du jeu est renvoyé. Par exemple, s'il s'agit d'une victoire, le résultat est égal à 1. Sinon, `
    #     il est égal à -1 s'il s'agit d'une défaite. Et 0 s'il y a égalité. Si l'ensemble du jeu est simulé de
    #     manière aléatoire, c'est-à-dire qu'à chaque tour, le coup est choisi de manière aléatoire parmi
    #     l'ensemble des coups possibles, on parle de jeu léger.
    #     """
    #
    #     while not is_game_over(self.state):  # tant que le jeu n'est pas terminé
    #         possible_moves = get_legal_actions(self.state, self.tile) # trouve moi tous les mouvements possibles
    #         action = self.rollout_policy(possible_moves)  # choisi l'action
    #         next_state = self.getChildState(action, self.tile)
    #         # current_rollout_state = self.move(action)  # déplace moi vers vers l'action choisie
    #         child_node = MonteCarloTreeSearchNode(next_state, tile=child_tile, parent=self, parent_action=action)
    #     return self.game_result()

    def rollout(self):
        """
        À partir de l'état actuel, le jeu entier est simulé jusqu'à ce qu'il y ait un résultat pour le jeu. Le
        résultat du jeu est renvoyé. Par exemple, s'il s'agit d'une victoire, le résultat est égal à 1. Sinon, `
        il est égal à -1 s'il s'agit d'une défaite. Et 0 s'il y a égalité. Si l'ensemble du jeu est simulé de
        manière aléatoire, c'est-à-dire qu'à chaque tour, le coup est choisi de manière aléatoire parmi
        l'ensemble des coups possibles, on parle de jeu léger.
        """
        current_rollout_state = getBoardCopy(self.state) # current_rollout_state = child_node.state

        current_tile = self.tile
        # if current_tile == 'X':
        #     tour_joueur = 0
        # else:
        #     tour_joueur = 1

        while not is_game_over(current_rollout_state):  # tant que le jeu n'est pas terminé, egale à tant que le node est pas terminal node
            possible_moves = get_legal_actions(current_rollout_state, current_tile) # trouve moi tous les mouvements possibles
            # print('A ' , current_tile, 'jouer')
            # action = possible_moves[random.randint(0, len(possible_moves))]
            if possible_moves !=[] :
                action = possible_moves[np.random.randint(len(possible_moves))]  # choisi l'action, pb: si possible_moves = [], erreur

                # current_rollout_state = current_rollout_state.move(action, tour_joueur)  # déplace moi vers vers l'action choisie
                flipTiles(current_rollout_state, current_tile, action[0], action[1])
                # drawBoard(current_rollout_state)

            if current_tile == 'X':
                 current_tile = 'O'
            else:
                 current_tile = 'X'

        resultats = getScoreOfBoard(current_rollout_state)

        return self.game_result(resultats)



    def rollout_policy(self, possible_moves):
        """
        Choisit aléatoirement un coup parmi les coups possibles. Il s'agit d'un exemple de jeu aléatoire.
        """
        return possible_moves[np.random.randint(len(possible_moves))]


    def game_result(self, resultats):
        '''
        Renvoie 1 ou 0 ou -1 selon votre état correspondant à une victoire, une égalité ou une perte.
        '''
        if self.tile =='O':
            computerTile = 'X'
        else:
            computerTile = 'O'

        if resultats[computerTile] > resultats[self.tile]:
            return 1
        elif resultats['X'] == resultats['O']:
            return 0
        else:
            return -1


    # def move(self, action, tour_joueur):
    #     '''
    #     Change l'état de votre plateau avec une nouvelle valeur. Pour un jeu de Tic Tac Toe normal, il peut
    #     s'agir d'un tableau 3 par 3 dont tous les éléments sont initialement à 0. 0 signifie que la position
    #     du plateau est vide. Si vous placez x sur la rangée 2, colonne 3, alors ce sera quelque chose comme
    #     plateau[2][3] = 1, où 1 représente ce x est placé.
    #     Renvoie le nouvel état après avoir effectué un déplacement.
    #     '''
    #     if tour_joueur % 2 == 0:
    #         tile = 'X'
    #         # print('Joueur X a joué et placé son pion à la ligne', action[1], ' et à la colonne ', action[0])
    #     else:
    #         tile = 'O'
    #         # print('Joueur O a joué et placé son pion à la ligne', action[1], ' et à la colonne ', action[0])
    #
    #     self.state = makeMove(self.state, tile, action[0], action[1])
    #
    #     tour_joueur += 1
    #     # drawBoard(self.states)
    #     # print(self.game_result())
    #     return self.state

        # copier parent state

        # child_state = getBoardCopy(self.state)
        #
        # flipTiles(child_state, tile, action[0], action[1])

        # tour_joueur += 1
        # drawBoard(self.states)
        # print(self.game_result())
        # return child_state




    def backpropagate(self, result):
        """
        Dans cette étape, toutes les statistiques des nœuds sont mises à jour. Jusqu'à ce que le nœud parent soit
        atteint, le nombre de visites pour chaque nœud est incrémenté de 1. Si le résultat est égal à 1, c'est-à-
        dire s'il s'agit d'un gain, alors le gain est incrémenté de 1. Sinon, si le résultat est une perte, alors
        la perte est incrémentée de 1.
        """
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)



    def is_fully_expanded(self):
        """
        Toutes les actions sont extraites de _untried_actions une par une. Lorsqu'il devient vide, c'est-à-dire
        lorsque sa taille est égale à zéro, il est entièrement développé.
        """
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        """
        Une fois complètement développée, cette fonction sélectionne le meilleur enfant dans le tableau des
        enfants. Le premier terme de la formule correspond à l'exploitation et le second terme à l'exploration.
        """
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]



    # def _tree_policy(self):
    #     """
    #     Sélectionne le nœud pour exécuter le déploiement.
    #     """
    #     simulation_no = 100
    #     current_node = self
    #     while not current_node.is_terminal_node():  # tant que le noeud actuel n'est pas terminal. Égale au current_node.is_game_over()
    #
    #         if not current_node.is_fully_expanded():
    #             action = current_node._untried_actions.pop()  # .pop() enlève et renvoie le dernier élément de la liste# si le noeud n'est pas entièrement développé
    #             return current_node.expand(action)  # je le développe # 但只得到下面一层的 children # return 结束 tree_policy
    #         # else:  # si c'est le noeud terminal
    #         #     current_node = current_node.best_child()  # je sélectionne le meilleur enfant
    #
    #         for c in current_node.children:
    #             for i in range(simulation_no):
    #                 current_node.children.rollout()
    #     return current_node

    def _tree_policy(self):
        """
        Sélectionne le nœud pour exécuter le déploiement.
        """
        current_node = self
        while not current_node.is_terminal_node():  # tant que le noeud actuel n'est pas terminal

            if not current_node.is_fully_expanded():  # si le noeud n'est pas entièrement développé
                return current_node.expand()  # je le développe # 结束 _tree_policy，return a chile_node()
            else:  # si c'est le noeud terminal
                current_node = current_node.best_child()  # je sélectionne le meilleur enfant
                return current_node







    def best_action(self):
        """
        Il s'agit de la fonction de meilleure action qui renvoie le nœud correspondant au meilleur déplacement
        possible. Les étapes d'expansion, de simulation et de rétropropagation sont réalisées par le code
        ci-dessus.
        """
        simulation_no = 1000


        for i in range(simulation_no):
            # print('simulation_no', simulation_no)
            v = self._tree_policy() # (当没有 full expanded 时) v 得到 self._tree_policy() 返回的一个 child_node
            reward = v.rollout() # renvoyer le resultat (1,0,-1)
            v.backpropagate(reward)

        return self.best_child(c_param=0.1) # return un child_node
















