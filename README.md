# OURABIA_Devoir_I
Algorithmes de recherche dans un labyrinthe (DFS, BFS, Astar)
# Projet Labyrinthe — DFS, BFS, A*

## Description
Un labyrinthe est représenté par une matrice 2D :
- `#` : mur
- `.` : case libre
- `S` : départ (Start) à (1,1)
- `G` : arrivée (Goal) à (14,14) pour une grille 16x16

Déplacements autorisés : haut, bas, gauche, droite.

Le programme :
1. Génère un labyrinthe 16x16 avec murs aléatoires
2. Garantit qu'un chemin existe entre `S` et `G`
3. Résout le labyrinthe avec :
   - DFS
   - BFS
   - A*
4. Affiche pour chaque algorithme :
   - Exploration (cases visitées `p`)
   - Solution (chemin `*`)
   - Chemin (liste de coordonnées)
   - Statistiques : noeuds explorés, longueur du chemin, temps d'exécution

## Structure
- `maze.py` : génération + utilitaires + rendu
- `dfs.py` : algorithme DFS
- `bfs.py` : algorithme BFS
- `astar.py` : algorithme A*
- `main.py` : point d'entrée
- `requirements.txt`
- `README.md`

## Exécution
Avec Python 3.10+ (recommandé 3.11) :

```bash
python main.py
