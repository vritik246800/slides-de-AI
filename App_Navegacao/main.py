"""
Ponto de entrada do projeto.

Uso:
  python main.py          → abre a interface gráfica Pygame
  python main.py --test   → corre os 4 casos de teste em modo terminal
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from model.grid    import Grid, FREE, OBSTACLE, TRAP, DIFFICULT
from model.state   import State
from model.problem import Problem
from algorithms.bfs    import bfs
from algorithms.greedy import greedy
from algorithms.astar  import astar
from metrics.tracker   import Metrics


# ---------------------------------------------------------------------------
# Casos de teste (terminal)
# ---------------------------------------------------------------------------

def _run_case(title, grid, start, goal, metrics):
    sr, sc = start
    gr, gc = goal
    problem = Problem(grid, State(sr, sc), State(gr, gc))

    print(f"\n{'='*55}")
    print(f" {title}")
    print(f"{'='*55}")
    print(f" Mapa: {grid.rows}x{grid.cols}  |  Inicio: {start}  |  Objetivo: {goal}")
    print()

    metrics.clear()
    for name, fn in [("BFS", bfs), ("Greedy", greedy), ("A*", astar)]:
        metrics.record(name, fn(problem))

    print(metrics.summary())


def run_tests():
    metrics = Metrics()

    # Caso 1: 5x5 sem obstáculos
    g1 = Grid(5, 5)
    _run_case("Caso 1 — 5x5 sem obstaculos", g1, (0, 0), (4, 4), metrics)

    # Caso 2: 10x10 com obstáculos
    g2 = Grid(10, 10)
    for r, c in [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
                 (5, 4), (5, 5), (5, 6), (5, 7), (5, 8),
                 (7, 0), (7, 1), (7, 2)]:
        g2.set_cell(r, c, OBSTACLE)
    _run_case("Caso 2 — 10x10 com obstaculos", g2, (0, 0), (9, 9), metrics)

    # Caso 3: sem solução
    g3 = Grid(5, 5)
    for r in range(5):
        g3.set_cell(r, 2, OBSTACLE)
    _run_case("Caso 3 — sem solucao (coluna bloqueada)", g3, (2, 0), (2, 4), metrics)

    # Caso 4: custos variados
    g4 = Grid(8, 8)
    for r in range(8):
        for c in range(4):
            g4.set_cell(r, c, DIFFICULT)
    g4.set_cell(3, 2, TRAP)
    _run_case("Caso 4 — terrenos de custo variado", g4, (0, 0), (7, 7), metrics)

    print("\nTestes concluidos.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        from ui.app import App
        App().run()
