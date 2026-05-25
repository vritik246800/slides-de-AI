"""
Pacote Model: Estruturas de dados centrais para busca de caminho.

O pacote model encapsula todas as estruturas de dados puras e definições de
problemas para o sistema de busca de caminho, independente da UI e algoritmos:

Módulos:
- grid.py: Grade 2D com tipos de terreno e custos de movimento
- state.py: Representação imutável de posição na grade (linha, coluna)
- problem.py: Definição formal do problema com ações, custos e teste de objetivo

Essas classes formam a base que os algoritmos de busca (BFS, Guloso, A*)
constroem. Eles definem o espaço de estados, regras de transição, custos e
condições de objetivo para o problema de busca de caminho em uma grade 2D
com terreno variável.

Princípio de design: A camada model é independente da UI (Pygame) e dos
algoritmos. Grid, State e Problem definem apenas o domínio do problema;
como resolvemos e visualizamos é deixado para outras camadas.
"""
