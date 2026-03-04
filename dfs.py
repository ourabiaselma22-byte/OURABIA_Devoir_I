# dfs.py

from __future__ import annotations  # permet l'utilisation d'annotations de types avancées

import time  # utilisé pour mesurer le temps d'exécution de l'algorithme
from typing import List, Optional, Set, Dict, Tuple

# Import des éléments nécessaires depuis le module maze
from maze import Maze, Coord, reconstruct_path

# Type de retour standard pour tous les algorithmes
# (path, visited, explored_count, dt_sec)
Result = Tuple[Optional[List[Coord]], Set[Coord], int, float]


def solve_dfs(maze: Maze) -> Result:
    """
    Implémente l'algorithme DFS (Depth-First Search) pour trouver un chemin
    entre le point de départ S et l'objectif G dans le labyrinthe.

    Retourne :
    - path : liste des coordonnées du chemin trouvé ou None
    - visited : ensemble des nœuds explorés
    - explored : nombre de nœuds explorés
    - dt : temps d'exécution de l'algorithme
    """

    # Récupération du point de départ et du point d'arrivée
    start, goal = maze.start, maze.goal

    # Démarrage du chronomètre pour mesurer le temps d'exécution
    t0 = time.perf_counter()

    # Pile utilisée par DFS (structure LIFO : Last In First Out)
    stack: List[Coord] = [start]

    # Dictionnaire parent permettant de reconstruire le chemin final
    # parent[nœud] = nœud précédent
    parent: Dict[Coord, Optional[Coord]] = {start: None}

    # Ensemble des nœuds déjà visités
    visited: Set[Coord] = set()

    # Compteur du nombre de nœuds explorés
    explored = 0

    # Boucle principale de l'algorithme DFS
    while stack:

        # On retire le dernier élément ajouté dans la pile
        current = stack.pop()

        # Si ce nœud a déjà été visité, on l'ignore
        if current in visited:
            continue

        # On marque le nœud comme visité
        visited.add(current)

        # On incrémente le compteur de nœuds explorés
        explored += 1

        # Si on a atteint l'objectif G
        if current == goal:

            # Reconstruction du chemin grâce au dictionnaire parent
            path = reconstruct_path(parent, start, goal)

            # Calcul du temps d'exécution
            dt = time.perf_counter() - t0

            # Retour du résultat
            return path if path else None, visited, explored, dt

        # Récupération des voisins accessibles (haut, bas, gauche, droite)
        nbrs = maze.neighbors_4(current)

        # Pour conserver l'ordre logique d'exploration
        # on ajoute les voisins dans l'ordre inverse
        # car la pile (LIFO) inverse l'ordre d'exécution
        for nxt in reversed(nbrs):

            # Si le voisin n'a pas encore de parent enregistré
            if nxt not in parent:
                parent[nxt] = current  # on enregistre le parent

            # On ajoute le voisin dans la pile pour exploration future
            stack.append(nxt)

    # Si aucun chemin n'est trouvé (cas improbable ici car le générateur garantit un chemin)
    dt = time.perf_counter() - t0

    # On retourne None pour le chemin
    return None, visited, explored, dt