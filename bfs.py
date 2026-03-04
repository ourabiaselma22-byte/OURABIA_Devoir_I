# bfs.py

from __future__ import annotations  # permet d'utiliser les annotations de type avancées

import time  # utilisé pour mesurer le temps d'exécution
from collections import deque  # structure de file FIFO utilisée par BFS
from typing import List, Optional, Set, Dict, Tuple

# Import des éléments nécessaires depuis le module maze
from maze import Maze, Coord, reconstruct_path

# Type de retour standard pour les algorithmes
# (path, visited, explored_count, dt_sec)
Result = Tuple[Optional[List[Coord]], Set[Coord], int, float]


def solve_bfs(maze: Maze) -> Result:
    """
    Implémente l'algorithme BFS (Breadth-First Search) pour trouver
    le plus court chemin entre S (start) et G (goal) dans le labyrinthe.

    Retourne :
    - path : chemin trouvé (liste de coordonnées) ou None
    - visited : ensemble des nœuds visités
    - explored : nombre de nœuds explorés
    - dt : temps d'exécution
    """

    # Récupération du point de départ et du point d'arrivée
    start, goal = maze.start, maze.goal

    # Début du chronométrage
    t0 = time.perf_counter()

    # File FIFO utilisée par BFS
    # On commence avec le nœud de départ
    q = deque([start])

    # Dictionnaire pour reconstruire le chemin final
    # parent[nœud] = nœud précédent
    parent: Dict[Coord, Optional[Coord]] = {start: None}

    # Ensemble des nœuds déjà visités
    # On marque directement start comme visité
    visited: Set[Coord] = {start}

    # Compteur du nombre de nœuds explorés
    explored = 0

    # Boucle principale de BFS
    while q:

        # On retire le premier élément de la file (FIFO)
        current = q.popleft()

        # On incrémente le compteur de nœuds explorés
        explored += 1

        # Si on atteint le but G
        if current == goal:

            # Reconstruction du chemin grâce au dictionnaire parent
            path = reconstruct_path(parent, start, goal)

            # Calcul du temps d'exécution
            dt = time.perf_counter() - t0

            # Retour des résultats
            return path if path else None, visited, explored, dt

        # Exploration des voisins accessibles
        for nxt in maze.neighbors_4(current):

            # Si le voisin n'a pas encore été visité
            if nxt not in visited:

                # On le marque comme visité
                visited.add(nxt)

                # On enregistre son parent
                parent[nxt] = current

                # On l'ajoute à la file pour exploration future
                q.append(nxt)

    # Si aucun chemin n'est trouvé
    dt = time.perf_counter() - t0
    return None, visited, explored, dt