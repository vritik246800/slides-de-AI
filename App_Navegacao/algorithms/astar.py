"""
Implementação de Busca A* para busca de caminho.

A* é um algoritmo de busca informado, otimizado em custo, que combina o custo real g(n)
com uma estimativa heurística h(n) para guiar a busca. Expande estados em ordem de
f(n) = g(n) + h(n), onde:
  - g(n): custo real de início até estado atual
  - h(n): custo estimado de estado atual até objetivo (heurística)
  - f(n): custo total estimado do caminho através do estado atual

Quando a heurística h(n) é admissível (nunca superestima o custo verdadeiro), A* é
garantido encontrar um caminho ótimo enquanto expande menos nós que algoritmos desinformados.

A* é considerado o "padrão ouro" para busca de caminho porque equilibra:
  - Completude: Sempre encontra solução se existe
  - Otimalidade: Encontra caminho de custo mínimo
  - Eficiência: Tipicamente explora muito menos nós que busca desinformada

Desempenho: O(V log V) com boa heurística; pior com heurísticas pobres.
Memória: O(V) para a fronteira e conjunto visitado.
"""

import heapq
import time

from model.problem import Problem
from model.state import State
from algorithms.heuristics import manhattan


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


def astar(problem: Problem) -> dict:
    """
    Executa Busca A* para encontrar um caminho de custo ótimo de início até objetivo.

    A* combina custo real g(n) com estimativa heurística h(n) para priorizar a
    fronteira usando f(n) = g(n) + h(n). Isto equilibra exploração (custo real) com
    orientação (heurística), levando a soluções ótimas com exploração eficiente.

    Características principais:
    - Informado: Usa heurística h(n) = distância Manhattan para guiar busca
    - Ótimo em custo: Encontra caminho de custo mínimo quando heurística é admissível
    - Completo: Sempre encontra solução se existe
    - Eficiente: Tipicamente expande muito menos nós que algoritmos desinformados

    Distância Manhattan é admissível para movimento em grelha com passos ortogonais
    porque nunca superestima o custo verdadeiro (custo mínimo por passo é 1, e
    Manhattan contabiliza todos os movimentos necessários sem atalhos).

    Detalhe de implementação: O contador é usado como desempate na fila de prioridade
    para garantir comportamento FIFO quando dois estados têm valores f(n) iguais.

    Args:
        problem: Uma instância de Problem definindo a grelha, início, objetivo e ações disponíveis.

    Returns:
        Um dicionário com chaves:
        - path: lista de tuplas (row, col) de início até objetivo, ou None se sem solução
        - explored: lista de tuplas (row, col) em ordem de expansão (para animação)
        - expanded: número de nós expandidos (estados removidos da fronteira)
        - cost: custo acumulado de terreno do caminho ótimo, ou None se sem solução
        - time: tempo de execução em segundos
    """
    # Registra tempo inicial para medição de desempenho
    t0 = time.perf_counter()

    # Inicializa busca com o estado inicial
    initial = problem.initial
    goal = problem.goal
    counter = 0  # Desempate para estabilidade de heap (garante FIFO quando f são iguais)

    # g_score: o custo real mais baixo encontrado até agora para alcançar cada estado
    # Inicializado com custo 0 para o estado inicial
    g_score = {initial: 0}

    # Fila de prioridade: tuplas de (f_valor, contador, estado)
    # f_valor = g(n) + h(n) é o custo estimado do caminho completo através deste estado
    frontier = [(manhattan(initial, goal), counter, initial)]
    parent = {initial: None}      # Mapeia cada estado para como foi alcançado
    visited = set()               # Rastreia estados expandidos para evitar re-expansão
    expanded = 0                  # Contagem de estados removidos da fronteira
    explored = []                 # Registra ordem de exploração para visualização

    # Loop principal de busca: continua até fronteira estar vazia
    while frontier:
        # Remove estado com menor f(n) = g(n) + h(n) da fila de prioridade
        # Isto equilibra custo real (g) com orientação heurística (h)
        f, _, state = heapq.heappop(frontier)

        # Pula se este estado já foi expandido (duplicado no heap)
        if state in visited:
            continue
        visited.add(state)
        expanded += 1
        explored.append((state.row, state.col))

        # Teste de objetivo: verifica se alcançou o alvo
        if problem.is_goal(state):
            return {
                "path": _reconstruct(parent, state),
                "explored": explored,
                "expanded": expanded,
                "cost": g_score[state],  # Retorna o custo real do caminho ótimo
                "time": time.perf_counter() - t0,
            }

        # Custo real atual para alcançar este estado
        g = g_score[state]

        # Expande: gera todos os estados sucessores do estado atual
        for action in problem.actions(state):
            new_state = problem.result(state, action)
            # Apenas considera estados não visitados
            if new_state not in visited:
                # Calcula custo real para alcançar novo_estado através do estado atual
                new_g = g + problem.step_cost(state, action)
                # Atualiza se é a primeira vez vendo este estado ou se encontrou caminho mais barato
                if new_state not in g_score or new_g < g_score[new_state]:
                    # Registra o custo menor
                    g_score[new_state] = new_g
                    parent[new_state] = state
                    counter += 1
                    # Adiciona à fronteira com prioridade f(n) = g(n) + h(n)
                    # g(n) = novo_g (custo real para alcançar novo_estado)
                    # h(n) = manhattan(novo_estado, objetivo) (custo estimado para alcançar objetivo)
                    # Juntos, f(n) guia busca para objetivo enquanto mantém otimalidade de custo
                    heapq.heappush(frontier, (new_g + manhattan(new_state, goal), counter, new_state))

    # Nenhuma solução encontrada: fronteira esgotada sem alcançar objetivo
    return {
        "path": None,
        "explored": explored,
        "expanded": expanded,
        "cost": None,
        "time": time.perf_counter() - t0,
    }
