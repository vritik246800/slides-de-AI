"""
Pacote: metrics
================

Responsabilidade: Rastreamento, armazenamento e formatação de métricas de desempenho.

Este pacote é responsável por coletar, organizar e apresentar dados de desempenho
dos algoritmos de busca (BFS, Greedy Best-First, A*). Fornece a classe principal
Metrics que centraliza todas as operações de tracking de resultados.

Módulos:
  - tracker.py: Define a classe Metrics que gerencia o ciclo completo de métricas
                (registro, consulta, formatação para UI, geração de relatórios de depuração)

Exemplo de uso:
    from metrics.tracker import Metrics
    
    metrics = Metrics()
    metrics.record("BFS", algorithm_result_dict)
    metrics.record("A*", astar_result_dict)
    
    # Para UI (tabelas e gráficos):
    rows = metrics.to_rows()
    
    # Para terminal (depuração):
    print(metrics.summary())
"""
