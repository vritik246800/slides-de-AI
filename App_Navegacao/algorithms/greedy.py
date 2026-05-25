"""
Implementação de Busca Gulosa Melhor-Primeiro para busca de caminho.

Busca Gulosa Melhor-Primeiro é um algoritmo de busca informado que usa apenas a função
heurística h(n) para ordenar a fronteira. A cada passo, expande o estado que
parece mais próximo do objetivo de acordo com a heurística, independentemente do custo real
já gasto para alcançá-lo.

Esta abordagem torna a Busca Gulosa rápida—frequentemente mais rápida que A*—porque tende
a "ir direto" para o objetivo. Porém, isto pode levar a caminhos subótimos,
especialmente quando a heurística é enganosa ou quando custos de terreno variam significativamente.

Gulosa usa distância Manhattan h(n) = |row_estado - row_objetivo| + |col_estado - col_objetivo|.
Embora Manhattan seja admissível (nunca superestima), Gulosa ignora o custo real g(n)
gasto para alcançar cada estado, então não garante otimalidade de custo.

Desempenho: Tipicamente O(V log V) na prática, mas O(V*V) pior caso se heurística é pobre.
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


def greedy(problem: Problem) -> dict:
    """
    Executa Busca Gulosa Melhor-Primeiro para encontrar um caminho de início até objetivo.

    Busca Gulosa Melhor-Primeiro usa apenas a função heurística h(n) para priorizar a fronteira.
    Sempre expande o estado que parece mais próximo do objetivo, sem considerar
    o custo real g(n) gasto para alcançá-lo. Isto o torna eficiente mas potencialmente
    subótimo.

    Características principais:
    - Informado: Usa heurística h(n) = distância Manhattan para guiar busca
    - Rápido: Frequentemente explora menos nós que algoritmos desinformados ou otimizados em custo
    - Não é ótimo em custo: Pode encontrar solução mas não a de custo mínimo
    - Completo: Geralmente encontra solução se existe (depende de qualidade da heurística)

    Detalhe de implementação: O contador é usado como desempate na fila de prioridade
    para garantir comportamento FIFO quando dois estados têm valores heurísticos iguais (para estabilidade).

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
    goal = problem.goal
    counter = 0  # Desempate para estabilidade de heap (garante FIFO quando h são iguais)

    # Fila de prioridade: tuplas de (h_valor, contador, estado)
    # h_valor é a estimativa heurística; contador resolve empates
    frontier = [(manhattan(initial, goal), counter, initial)]
    parent = {initial: None}      # Mapeia cada estado para como foi alcançado
    cost_so_far = {initial: 0}    # Acumula custos de terreno para custo final do caminho
    visited = set()               # Rastreia estados expandidos para evitar re-expansão
    expanded = 0                  # Contagem de estados removidos da fronteira
    explored = []                 # Registra ordem de exploração para visualização

    # Loop principal de busca: continua até fronteira estar vazia
    while frontier:
        # Remove estado com menor h(n) da fila de prioridade
        # (Gulosa: ignora g(n), apenas considera h(n))
        _, _, state = heapq.heappop(frontier)

        # Pula se este estado já foi expandido (duplicado no heap)
        # Isto pode acontecer porque podemos adicionar o mesmo estado múltiplas vezes com custos diferentes
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
                "cost": cost_so_far[state],
                "time": time.perf_counter() - t0,
            }

        # Expande: gera todos os estados sucessores do estado atual
        for action in problem.actions(state):
            new_state = problem.result(state, action)
            # Apenas considera estados não visitados
            if new_state not in visited:
                new_cost = cost_so_far[state] + problem.step_cost(state, action)
                # Adiciona ou atualiza se encontrou caminho mais barato para este estado
                # (mesmo que Gulosa não use custo para priorização, rastreamos para comparação)
                if new_state not in cost_so_far or new_cost < cost_so_far[new_state]:
                    cost_so_far[new_state] = new_cost
                    parent[new_state] = state
                    counter += 1
                    # Adiciona à fronteira priorizado apenas por h(n) (ignorando g(n))
                    # Isto é o que torna "guloso": perseguindo o valor heurístico
                    heapq.heappush(frontier, (manhattan(new_state, goal), counter, new_state))

    # Nenhuma solução encontrada: fronteira esgotada sem alcançar objetivo
    return {
        "path": None,
        "explored": explored,
        "expanded": expanded,
        "cost": None,
        "time": time.perf_counter() - t0,
    }
