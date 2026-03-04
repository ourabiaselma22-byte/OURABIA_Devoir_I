# astar.py

from __future__ import annotations  # permet d'utiliser les annotations de type avancées

import time  # utilisé pour mesurer le temps d'exécution
import heapq  # implémentation de file de priorité (min-heap)
from typing import List, Optional, Set, Dict, Tuple

# Import des fonctions et types nécessaires depuis maze.py
from maze import Maze, Coord, reconstruct_path, manhattan

# Type de retour standard pour tous les algorithmes
# (path, visited, explored_count, dt_sec)
Result = Tuple[Optional[List[Coord]], Set[Coord], int, float]


def solve_astar(maze: Maze) -> Result:
    """
    Implémente l'algorithme A* (A-star) pour trouver le chemin optimal
    entre le point de départ S et le point d'arrivée G.

    Retourne :
    - path : chemin trouvé (liste de coordonnées) ou None
    - visited : ensemble des nœuds explorés
    - explored : nombre de nœuds explorés
    - dt : temps d'exécution
    """

    # Récupération du point de départ et du point d'arrivée
    start, goal = maze.start, maze.goal

    # Démarrage du chronomètre
    t0 = time.perf_counter()

    # g_score[n] = coût réel depuis le départ jusqu'au nœud n
    # Au départ, seul start a un coût connu = 0
    g_score: Dict[Coord, int] = {start: 0}

    # Dictionnaire pour reconstruire le chemin final
    parent: Dict[Coord, Optional[Coord]] = {start: None}

    # File de priorité (heap) contenant les nœuds à explorer
    # Chaque élément = (f_score, tie_breaker, node)
    open_heap: List[Tuple[int, int, Coord]] = []

    # variable utilisée pour départager les nœuds ayant le même f_score
    tie = 0

    # insertion du nœud start dans la file de priorité
    # f(start) = g(start) + h(start)
    # g(start) = 0
    # h(start) = distance Manhattan jusqu'au goal
    heapq.heappush(open_heap, (manhattan(start, goal), tie, start))

    # ensemble des nœuds déjà explorés
    visited: Set[Coord] = set()

    # compteur du nombre de nœuds explorés
    explored = 0

    # boucle principale de l'algorithme A*
    while open_heap:

        # extraction du nœud avec le plus petit f_score
        _, _, current = heapq.heappop(open_heap)

        # si déjà visité, on ignore
        if current in visited:
            continue

        # marquer le nœud comme visité
        visited.add(current)

        # incrément du compteur
        explored += 1

        # si on atteint l'objectif
        if current == goal:

            # reconstruction du chemin
            path = reconstruct_path(parent, start, goal)

            # calcul du temps d'exécution
            dt = time.perf_counter() - t0

            return path if path else None, visited, explored, dt

        # exploration des voisins accessibles
        for nxt in maze.neighbors_4(current):

            # coût pour atteindre le voisin depuis start
            tentative_g = g_score[current] + 1

            # si le voisin n'a jamais été vu
            # ou si on trouve un chemin plus court
            if nxt not in g_score or tentative_g < g_score[nxt]:

                # mise à jour du coût
                g_score[nxt] = tentative_g

                # mise à jour du parent pour reconstruire le chemin
                parent[nxt] = current

                # incrément pour éviter les conflits dans la heap
                tie += 1

                # calcul de la fonction d'évaluation A*
                # f(n) = g(n) + h(n)
                f = tentative_g + manhattan(nxt, goal)

                # insertion dans la file de priorité
                heapq.heappush(open_heap, (f, tie, nxt))

    # si aucun chemin n'a été trouvé
    dt = time.perf_counter() - t0
    return None, visited, explored, dt