#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/01/2022

@author: Chaimae EL HOUJJAJI, Kexin LI, Pauline TURK
"""

import numpy as np
from collections import defaultdict

# -----------------------------
# import fonctions hors class
# -----------------------------

from fonctions00 import getBoardCopy, getScoreOfBoard, \
    is_game_over, get_legal_actions, flipTiles


class MonteCarloTreeSearchNode(object):
    def __init__(self, state, tile=None, parent=None, parent_action=None):
        self.state = state
        self.tile = tile
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0               # gain
        self._results[-1] = 0              # perte
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return


    def untried_actions(self):
        """ 
        Returns:
            list: Actions légales non encore essayées pour une configuration
                  de jeu donnée pour le joueur dont c'est le tour.
        """
        self._untried_actions = get_legal_actions(self.state, self.tile)
        return self._untried_actions


    def q(self):
        """ Calcul de la différence entre les victoires et les défaites.

        Returns:
            float: différence entre les victoires et les défaites.
        """
        wins = self._results[1]
        loses = self._results[-1]   
        return wins - loses


    def n(self):
        """
        Returns:
            float: nombre de visites du noeud considéré.
        """
        return self._number_of_visits
    

    def expand(self):
        """À cette étape, un nouveau noeud enfant possible est généré et est ajouté au tableau des enfants. 
            Il constitue un nouveau noeud du tree search. 
            Ce nouveau noeud est associé au tour de l'autre joueur.

        Returns:
            list: le noeud enfant généré.
        """
        action = self._untried_actions.pop()  # .pop() enlève et renvoie le dernier élément de la liste
                                              # permet de ne générer qu'une seule fois chaque enfant
                                              # du noeud actuel.
        next_state = self.getChildState(action, self.tile)
        if self.tile == 'X':
            child_tile = 'O'
        else:
            child_tile = 'X'

        child_node = MonteCarloTreeSearchNode(next_state, tile=child_tile, parent=self, parent_action=action)
        self.children.append(child_node)

        return child_node


    def getChildState(self, action, tile):
        """Change l'état du plateau de jeu selon l'action envisagée.

        Args:
            action (list): couple des coordonnées de la case à jouer.          
            tile (str): vaut 'X' ou 'O' et définit à qui est le tour.

        Returns:
            list: le nouvel état après un coup.
        """
        child_state = getBoardCopy(self.state)
        flipTiles(child_state, tile, action[0], action[1])

        return child_state


    def is_terminal_node(self):
        """Teste si le noeud actuel est terminal ou non
           i.e si une partie est terminée ou non.

        Returns:
            bool: True si la partie est finie
                  False sinon.
        """
        return is_game_over(self.state)


    def rollout(self):
        """ À partir de l'état actuel, la partie est simulée jusqu'à la fin de partie. 
            Tous les coups sont choisis aléatoirement parmi l'ensemble des coups possibles, 
            on parle de jeu léger.

        Returns:
            [type]: Le résultat du jeu est renvoyé:
                    s'il s'agit d'une victoire, le résultat est égal à 1, 
                    s'il s'agit d'une défaite ,il est égal à -1 
                    sinon il vaut 0 en cas d'égalité. 
        """
        current_rollout_state = getBoardCopy(self.state) # current_rollout_state = child_node.state   
        current_tile = self.tile

        while not is_game_over(current_rollout_state):                               # tant que la partie simulée n'est pas terminée
            possible_moves = get_legal_actions(current_rollout_state, current_tile)  # liste des coups possibles
            if possible_moves !=[] :                                                 # si au moins un coup est possible
                action = possible_moves[np.random.randint(len(possible_moves))]      # tirer au hasard un coup possible
                flipTiles(current_rollout_state, current_tile, action[0], action[1]) # effectuer ce coup aléatoire
            
            # donner son tour à l'autre joueur dont le coup sera tiré au sort de la même façon
            if current_tile == 'X': 
                 current_tile = 'O'
            else:
                 current_tile = 'X'

        resultats = getScoreOfBoard(current_rollout_state)    # récupérer le nombre de 'X' et de 'O' en fin de partie
                                                              # pour pouvoir calculer le résultat du jeu est renvoyé
        return self.game_result(resultats)


    def game_result(self, resultats):
        """
        Args:
            resultats (int): résultat du jeu, c'est un dictionnaire avec le résultat de X et de O

        Returns:
            int: 1 ou 0 ou -1 selon que l'état correspondant à une victoire, une égalité ou une défaite.
        """
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



    def backpropagate(self, result):
        """Mise à jour des statistiques de chaque nœud de la branche contenant le noeud enfant considéré
           i.e remontée dans l'arbre du noeud enfant au noeud racine (qui n'a pas de parent) 
           --> récursivité de backpropagate().
           
           Pour chaque nœud de cette remontée dans l'arbre:
           - le nombre de visites est incrémenté de 1
           - si le résultat de la partie simulée est égal à 1, le compte des gains est incrémenté de 1
           - si le résultat de la partie simulée est égal à -1, le compte des défaites est incrémenté de 1

        Args:
            result (int): résultat de la partie simulée dans la rollout
        """
        self._number_of_visits += 1.     
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)


    def is_fully_expanded(self):
        """ Teste si le noeud considéré a été complètement développé
            i.e si tous ses enfants possibles ont été générés
            i.e toutes les actions possibles ont été utilisées pour générer un enfant.

        Returns:
            bool: True si le noeud est complètement développé
                  False sinon.
        """
        return len(self._untried_actions) == 0


    def best_child(self, c_param):
        """ Sélection du meilleur enfant (UCB le plus élevé) parmi tous les enfants possibles
        du noeud considéré. 
        Le premier terme de la formule de l'UCB correspond à l'exploitation et le second terme à l'exploration.

        Args:
            c_param (float):  paramètre d'exploration

        Returns:
            list: enfant d'UCB max
        """
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]


    def _tree_policy(self,c_param):
        """Selection du noeud enfant qui va subir le rollout.

        Args:
            c_param (float):  paramètre d'exploration

        Returns:
            list: - si le noeud actuel n'est pas complètement développé: nouvel enfant possbile qui est généré.
                  - sinon : le meilleur enfant parmi tous les enfants possibles.
        """ 
        current_node = self
        while not current_node.is_terminal_node():              # tant que le noeud actuel n'est pas terminal
            if not current_node.is_fully_expanded():            # si le noeud n'est pas entièrement développé
               return current_node.expand()                     # continuer à le développer en générant un nouvel
                                                                # enfant parmi les possibles
            else:                                               # s'il est complètement développé
                current_node = current_node.best_child(c_param) # sélection du meilleur enfant
                return current_node
            

    def best_action(self,simulation_no,c_param):
        """Permet de choisir la meilleure action i.e qui renvoie le nœud enfant correspondant au meilleur coup
        possible connu. 
        Les étapes d'expansion/sélection, de simulation et de rétropropagation sont réalisées par le code
        ci-dessus autant de fois que la valeur du paramètre simulation_no.

        Args:
            simulation_no (int): Nombre de fois où l'algorithme MCTS est appliqué au noeud considéré
                                 i.e revient au nombre de parties simulées avant de jouer le prochain coup
            c_param (float):  paramètre d'exploration

        Returns:
            list: noeud enfant correspondant au meileur coup à jouer selon le tree search connu
        """
        for i in range(simulation_no):
            v = self._tree_policy(c_param) # selection/expansion
            reward = v.rollout()           # simulation
            v.backpropagate(reward)        # rétropropagation

        return self.best_child(c_param=0.) # meilleur coup connu



