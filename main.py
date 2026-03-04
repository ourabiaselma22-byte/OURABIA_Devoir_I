# main.py
from __future__ import annotations

from typing import Callable, List, Optional, Set, Tuple, Dict, Any

from maze import generate_maze, render_maze, path_to_string, Maze, Coord
from dfs import solve_dfs
from bfs import solve_bfs
from astar import solve_astar

Solver = Callable[[Maze], Tuple[Optional[List[Coord]], Set[Coord], int, float]]


def run_and_print(title: str, maze: Maze, solver: Solver) -> Dict[str, Any]:
    """
    Exécute un algorithme, affiche :
      - exploration (p)
      - solution (*)
      - chemin (S(...) -> ... -> G(...))
      - stats (noeuds, longueur, temps)
    Et retourne un dict de stats pour le tableau comparatif.
    """
    path, visited, explored, dt = solver(maze)
    start, goal = maze.start, maze.goal
    time_ms = dt * 1000.0

    print("\n" + "=" * 40)
    print(f"{title}")
    print("=" * 40)

    # 1) Exploration
    print("\n--- Exploration (p = cases parcourues) ---")
    print(render_maze(maze, visited=visited, mode="exploration"))

    # Si pas de chemin (ne devrait pas arriver car on garantit un chemin)
    if path is None:
        print("\n--- Solution (* = chemin trouvé) ---")
        print("Aucun chemin trouvé.")

        print("\n--- Chemin ---")
        print("Chemin : (aucun)")

        print("\n--- Statistiques ---")
        print(f"Nombre de noeuds explorés : {explored}")
        print(f"Longueur du chemin trouvé : 0")
        print(f"Temps d'exécution         : {time_ms:.3f} ms")

        return {"algo": title, "explored": explored, "length": 0, "time_ms": time_ms}

    # 2) Solution
    print("\n--- Solution (* = chemin trouvé) ---")
    print(render_maze(maze, path=path, mode="solution"))

    # 3) Chemin (format exigé)
    print("\n--- Chemin ---")
    print("Chemin :", path_to_string(path, start, goal))

    # 4) Stats
    print("\n--- Statistiques ---")
    print(f"Nombre de noeuds explorés : {explored}")
    print(f"Longueur du chemin trouvé : {len(path)}")
    print(f"Temps d'exécution         : {time_ms:.3f} ms")

    return {"algo": title, "explored": explored, "length": len(path), "time_ms": time_ms}


def print_comparison_table(results: List[Dict[str, Any]]) -> None:
    """
    Affiche un tableau comparatif ASCII :
      Algorithme | Noeuds explorés | Longueur du chemin | Temps (ms)
    """
    # (sécurité) filtrer les None au cas où
    results = [r for r in results if r is not None]

    headers = ["Algorithme", "Noeuds explorés", "Longueur du chemin", "Temps (ms)"]
    table_data = [
        [r["algo"], str(r["explored"]), str(r["length"]), f'{r["time_ms"]:.3f}']
        for r in results
    ]

    # Largeurs des colonnes
    col_widths = [len(h) for h in headers]
    for table_row in table_data:
        for idx, cell in enumerate(table_row):
            col_widths[idx] = max(col_widths[idx], len(cell))

    def sep(char: str = "-") -> str:
        return "+" + "+".join(char * (w + 2) for w in col_widths) + "+"

    def fmt_row(table_row: List[str]) -> str:
        return "| " + " | ".join(
            table_row[idx].ljust(col_widths[idx]) for idx in range(len(table_row))
        ) + " |"

    print("\n" + "=" * 40)
    print("TABLEAU COMPARATIF (DFS vs BFS vs A*)")
    print("=" * 40)
    print(sep("-"))
    print(fmt_row(headers))
    print(sep("="))
    for table_row in table_data:
        print(fmt_row(table_row))
        print(sep("-"))


def main() -> None:
    # Paramètres exigés : 16x16 + seed (reproductibilité)
    maze = generate_maze(size=16, seed=7, wall_prob=0.32)

    # Affichage du labyrinthe de base (optionnel mais utile)
    print("=== Labyrinthe (base) ===")
    print(render_maze(maze, mode="base"))

    # Exécuter les 3 algorithmes et collecter les stats
    results: List[Dict[str, Any]] = []
    results.append(run_and_print("DFS (Non-informé)", maze, solve_dfs))
    results.append(run_and_print("BFS (Non-informé, optimal)", maze, solve_bfs))
    results.append(run_and_print("A* (Informé, heuristique Manhattan)", maze, solve_astar))

    # Tableau comparatif final (exigence ajoutée)
    print_comparison_table(results)


if __name__ == "__main__":
    main()