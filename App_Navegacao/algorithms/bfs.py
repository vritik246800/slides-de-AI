"""
Implementação de Busca em Largura (BFS) para busca de caminho.

BFS é um algoritmo de busca desinformado que explora estados nível a nível,
garantindo o caminho com o número mínimo de passos. Porém, não considera
custos de terreno (DIFÍCIL, ARMADILHA) ao computar o caminho, tornando-o
ótimo apenas para contagem de passos, não para custo total.

BFS usa uma fila FIFO (deque) para manter a fronteira. Cada estado é expandido
apenas uma vez, na ordem em que é descoberto. Esta exploração nível a nível
garante que quando o objetivo é encontrado, foi alcançado via o caminho mais curto
em termos de passos.

Desempenho: O(V + E) onde V = número de estados, E = número de arestas.
Memória: O(V) para a fronteira e dicionário de pais.
"""

from collections import deque
import time

from model.problem import Problem
from model.state import State


def _reconstruct(parent: dict, goal: State) -> list:
    """
    Reconstrói o caminho do início até o objetivo rastreando links de pais.

    Args:
        parent: Dicionário mapeando cada estado para seu estado pai na árvore de busca.
                O estado inicial mapeia para None.
        goal: O estado objetivo de onde rastrear.

    Returns:
        Uma lista de tuplas (row, col) representando o caminho de início até objetivo,
        em ordem de início (índice 0) até objetivo (índice -1).
    """
    path = []
    node = goal
    while node is not None:
        path.append((node.row, node.col))
        node = parent[node]
    return list(reversed(path))


def bfs(problem: Problem) -> dict:
    """
    Executa Busca em Largura para encontrar um caminho de início até objetivo.

    BFS processa estados em ordem FIFO (usando uma deque), expandindo todos os estados em
    profundidade d antes de expandir estados em profundidade d+1. Isto garante encontrar o caminho
    com o número mínimo de passos (embora não necessariamente custo mínimo).

    Características principais:
    - Desinformado: Não usa heurística para guiar a busca
    - Ótimo para contagem de passos: Encontra caminho com menos movimentos
    - Completo: Sempre encontra uma solução se existe
    - Não prefere caminhos de menor custo (ignora custos de DIFÍCIL, ARMADILHA)

    Args:
        problem: Uma instância de Problem definindo a grelha, início, objetivo e ações disponíveis.

    Returns:
        Um dicionário com chaves:
        - path: lista de tuplas (row, col) de início até objetivo, ou None se sem solução
        - explored: lista de tuplas (row, col) em ordem de expansão (para animação)
        - expanded: número de nós expandidos (estados removidos da fronteira)
        - cost: custo acumulado de terreno do caminho, ou None se sem solução
        - time: tempo de execução em segundos
    """
    # Registra tempo inicial para medição de desempenho
    t0 = time.perf_counter()

    # Inicializa busca com o estado inicial
    initial = problem.initial
    frontier = deque([initial])  # Fila FIFO para exploração em largura desinformada
    parent = {initial: None}      # Mapeia cada estado para como foi alcançado
    cost_so_far = {initial: 0}    # Acumula custos de terreno (para log, não decisão)
    expanded = 0                  # Contagem de estados removidos da fronteira
    explored = []                 # Registra ordem de exploração para visualização

    # Loop principal de busca: continua até fronteira estar vazia
    while frontier:
        # Remove o próximo estado da frente da fila (comportamento FIFO)
        state = frontier.popleft()
        expanded += 1
        explored.append((state.row, state.col))

        # Teste de objetivo: verifica se alcançou o alvo
        if problem.is_goal(state):
            return {
                "path": _reconstruct(parent, state),
                "explored": explored,
                "expanded": expanded,
                "cost": cost_so_far[state],
                "time": time.perf_counter() - t0,
            }

        # Expande: gera todos os estados sucessores do estado atual
        for action in problem.actions(state):
            new_state = problem.result(state, action)
            # Apenas adiciona estados não visitados à fronteira (evita ciclos e caminhos redundantes)
            if new_state not in parent:
                parent[new_state] = state
                # Rastreia custo de terreno mesmo que BFS não otimize para isso
                cost_so_far[new_state] = cost_so_far[state] + problem.step_cost(state, action)
                frontier.append(new_state)

    # Nenhuma solução encontrada: fronteira esgotada sem alcançar objetivo
    return {
        "path": None,
        "explored": explored,
        "expanded": expanded,
        "cost": None,
        "time": time.perf_counter() - t0,
    }
