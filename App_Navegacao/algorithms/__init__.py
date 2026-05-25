"""
Pacote de algoritmos de busca em caminho.

Este módulo contém três algoritmos de busca principais para busca de caminho em grelha:
  - BFS (Busca em Largura): Busca desinformada, garante contagem mínima de passos
  - Greedy Best-First: Usa apenas heurística h(n), rápido mas não otimizado em custo
  - A*: Usa f(n) = g(n) + h(n), otimizado em custo com heurística admissível

Todos os algoritmos aceitam um objeto Problem e retornam um dicionário padronizado com:
  - path: lista de tuplas (row, col) ou None se sem solução
  - explored: ordem de expansões de estados (para animação)
  - expanded: número total de nós expandidos
  - cost: custo acumulado do terreno ou None
  - time: tempo de execução em segundos
"""
