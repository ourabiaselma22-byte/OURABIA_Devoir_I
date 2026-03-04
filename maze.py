# maze.py
from __future__ import annotations  # permet d'utiliser des annotations de types "en avance" (Python 3.7+)

import random
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set, Dict

# -----------------------------
# Constantes de représentation
# -----------------------------
WALL = "#"    # mur (obstacle infranchissable)
FREE = "."    # case libre
START = "S"   # point de départ
GOAL = "G"    # point d'arrivée

# Une coordonnée est représentée par un tuple (ligne, colonne)
Coord = Tuple[int, int]  # (row, col)


# -----------------------------
# Classe Maze : encapsule la grille
# -----------------------------
@dataclass(frozen=True)
class Maze:
    """
    Représente un labyrinthe sous forme de grille (liste de listes de caractères).
    frozen=True => instance immuable (on évite de modifier la grille par erreur).
    """
    grid: List[List[str]]

    @property
    def size(self) -> int:
        """Retourne la taille N du labyrinthe (ici 16)."""
        return len(self.grid)

    @property
    def start(self) -> Coord:
        """
        Cherche et retourne la coordonnée de 'S' dans la grille.
        Important : on parcourt toute la grille jusqu'à trouver START.
        """
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == START:
                    return r, c
        # Si on ne trouve pas S, c'est une erreur de génération / chargement de la grille
        raise ValueError("Start 'S' introuvable.")

    @property
    def goal(self) -> Coord:
        """
        Cherche et retourne la coordonnée de 'G' dans la grille.
        """
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == GOAL:
                    return r, c
        raise ValueError("Goal 'G' introuvable.")

    def is_wall(self, node: Coord) -> bool:
        """Vérifie si la case (r,c) est un mur."""
        r, c = node
        return self.grid[r][c] == WALL

    def in_bounds(self, node: Coord) -> bool:
        """Vérifie si la coordonnée (r,c) est dans les limites de la grille."""
        r, c = node
        return 0 <= r < self.size and 0 <= c < self.size

    def neighbors_4(self, node: Coord) -> List[Coord]:
        """
        Retourne les voisins accessibles en 4 directions (haut, bas, gauche, droite),
        uniquement si la case n'est pas un mur '#'.
        Cette fonction est utilisée par DFS, BFS et A* pour garantir la même logique de déplacement.
        """
        r, c = node

        # Candidats : les 4 mouvements autorisés
        cand = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        res: List[Coord] = []
        for rr, cc in cand:
            # On vérifie : dans la grille + pas un mur
            if 0 <= rr < self.size and 0 <= cc < self.size and self.grid[rr][cc] != WALL:
                res.append((rr, cc))
        return res


# -----------------------------
# Génération du labyrinthe
# -----------------------------
def generate_maze(size: int = 16, seed: Optional[int] = None, wall_prob: float = 0.30) -> Maze:
    """
    Génère un labyrinthe size x size.
    Contraintes de l'énoncé :
    - bords extérieurs toujours des murs
    - S à (1,1)
    - G à (size-2, size-2) => (14,14) si size=16
    - murs placés aléatoirement à l'intérieur
    - un chemin doit exister entre S et G
    - seed permet la reproductibilité

    Stratégie :
    1) On rend tout l'intérieur libre (.)
    2) On construit un chemin garanti de S vers G (protégé)
    3) On met des murs aléatoires ailleurs sans casser le chemin protégé
    """
    if size < 4:
        raise ValueError("size doit être >= 4.")

    # Générateur aléatoire local (seed => même labyrinthe à chaque exécution si seed identique)
    rng = random.Random(seed)

    # 1) Initialisation : toute la grille en murs '#'
    # => les bords seront automatiquement des murs (car on ne les change pas)
    grid = [[WALL for _ in range(size)] for _ in range(size)]

    # 2) On rend l'intérieur libre (.)
    for r in range(1, size - 1):
        for c in range(1, size - 1):
            grid[r][c] = FREE

    # Coordonnées imposées par l'énoncé
    s: Coord = (1, 1)
    g: Coord = (size - 2, size - 2)

    # 3) Construction d'un chemin garanti S -> G
    # On ne bouge que vers le bas (D) et vers la droite (R),
    # ce qui garantit d'atteindre G sans sortir de la grille.
    down_moves = g[0] - s[0]
    right_moves = g[1] - s[1]
    moves = ["D"] * down_moves + ["R"] * right_moves

    # On mélange pour obtenir un chemin différent selon la seed
    rng.shuffle(moves)

    # "protected" contient toutes les cases du chemin garanti
    protected: Set[Coord] = {s}

    # On suit les mouvements mélangés pour construire le chemin
    r, c = s
    for m in moves:
        if m == "D":
            r += 1
        else:
            c += 1
        protected.add((r, c))

    # 4) Ajout des murs aléatoires à l'intérieur (hors chemin protégé)
    # wall_prob contrôle la densité des murs
    for rr in range(1, size - 1):
        for cc in range(1, size - 1):
            if (rr, cc) in protected:
                continue  # on ne touche pas au chemin garanti
            grid[rr][cc] = WALL if rng.random() < wall_prob else FREE

    # 5) Placement final de S et G
    grid[s[0]][s[1]] = START
    grid[g[0]][g[1]] = GOAL

    return Maze(grid=grid)


# -----------------------------
# Reconstruction du chemin
# -----------------------------
def reconstruct_path(parent: Dict[Coord, Optional[Coord]], start: Coord, goal: Coord) -> List[Coord]:
    """
    Reconstruit le chemin en utilisant le dictionnaire parent :
      parent[nœud] = nœud précédent
    Principe :
      - on part de goal
      - on remonte jusqu'à start (via parent)
      - puis on inverse la liste obtenue

    Retour :
      - liste de Coord du chemin S -> ... -> G
      - si aucun chemin valide n'a été reconstruit, retourne []
    """
    path: List[Coord] = []
    cur: Optional[Coord] = goal

    # Remonter depuis goal jusqu'à None (parent[start] = None)
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)

    # On a construit le chemin à l'envers (G -> ... -> S), donc on inverse
    path.reverse()

    # Vérification : si le chemin ne commence pas par start, alors reconstruction invalide
    if not path or path[0] != start:
        return []
    return path


# -----------------------------
# Affichage du labyrinthe
# -----------------------------
def render_maze(
    maze: Maze,
    visited: Optional[Set[Coord]] = None,
    path: Optional[List[Coord]] = None,
    mode: str = "base"
) -> str:
    """
    Produit une représentation texte du labyrinthe.

    Modes :
      - "base"       : affiche la grille telle quelle
      - "exploration": marque les cases visitées avec 'p'
      - "solution"   : marque les cases du chemin final avec '*'

    Règle importante :
      - S et G ne sont jamais remplacés par p ou *
    """
    visited = visited or set()
    path_set = set(path) if path else set()

    out_lines: List[str] = []

    # On parcourt toute la grille pour construire l'affichage ligne par ligne
    for r in range(maze.size):
        row_chars: List[str] = []
        for c in range(maze.size):
            ch = maze.grid[r][c]

            # Les murs restent des murs
            if ch == WALL:
                row_chars.append(WALL)
                continue

            # Mode exploration : on marque 'p' les cases visitées (sauf S/G)
            if mode == "exploration":
                if (r, c) in visited and ch not in (START, GOAL):
                    row_chars.append("p")
                else:
                    row_chars.append(ch)

            # Mode solution : on marque '*' les cases du chemin (sauf S/G)
            elif mode == "solution":
                if (r, c) in path_set and ch not in (START, GOAL):
                    row_chars.append("*")
                else:
                    row_chars.append(ch)

            # Mode base : on affiche tel quel
            else:
                row_chars.append(ch)

        # Ajout de la ligne formatée (séparée par des espaces pour lisibilité)
        out_lines.append(" ".join(row_chars))

    # On retourne une seule chaîne de caractères multi-lignes
    return "\n".join(out_lines)


# -----------------------------
# Conversion du chemin en texte
# -----------------------------
def path_to_string(path: List[Coord], start: Coord, goal: Coord) -> str:
    """
    Convertit la liste de coordonnées en format demandé :
    Chemin : S(1, 1) -> (2, 1) -> ... -> G(14, 14)
    """
    parts: List[str] = []
    for (r, c) in path:
        if (r, c) == start:
            parts.append(f"S({r}, {c})")
        elif (r, c) == goal:
            parts.append(f"G({r}, {c})")
        else:
            parts.append(f"({r}, {c})")
    return " -> ".join(parts)


# -----------------------------
# Heuristique A* (Manhattan)
# -----------------------------
def manhattan(a: Coord, b: Coord) -> int:
    """
    Distance Manhattan entre a et b :
      |ax - bx| + |ay - by|
    Utilisée comme heuristique h(n) dans A* sur une grille 4-directionnelle.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])