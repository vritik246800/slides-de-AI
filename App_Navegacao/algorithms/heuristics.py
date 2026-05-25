"""
Funções heurísticas para algoritmos de busca informados.

Uma heurística é uma função h(n) que estima o custo de um estado n até o objetivo.
Boas heurísticas guiam a busca para o objetivo eficientemente sem causar subotimalidade.

Propriedades-chave de heurísticas:
  - Admissível: h(n) <= custo_verdadeiro(n, objetivo) para todos os estados n
    Garante que A* encontra soluções ótimas ao usar heurística admissível.
  - Consistente (monotônica): h(n) <= custo(n, n') + h(n') para todos os sucessores n' de n
    Garante que A* nunca precisa re-expandir um estado.

Distância Manhattan é tanto admissível quanto consistente para busca de caminho em grelha com
movimento ortogonal (4-direcional). É justa no sentido que apenas conta o
número mínimo de passos necessários em cada direção, nunca superestimando.

Enquanto heurísticas mais sofisticadas (como distância Euclidiana ou soluções de problema relaxado)
existem, Manhattan é simples, rápida de computar, e efetiva para problemas em grelha.
"""

from model.state import State


def manhattan(state: State, goal: State) -> float:
    """
    Calcula a distância Manhattan (distância L1) de um estado até o objetivo.

    Distância Manhattan é a soma das diferenças absolutas em posições de linha e coluna.
    Isto representa o número mínimo de movimentos necessários para alcançar o objetivo quando o movimento
    é restrito a direções ortogonais (cima, baixo, esquerda, direita), ignorando obstáculos.

    Fórmula: h(n) = |row_n - row_objetivo| + |col_n - col_objetivo|

    Por que Manhattan funciona como heurística:
    - Admissível: Nunca pode superestimar (cada passo move pelo menos 1 unidade Manhattan mais perto)
    - Consistente: Os valores heurísticos diminuem consistentemente ao longo de qualquer caminho ótimo
    - Justa: Não pode ser melhorada sem conhecimento específico do domínio de custos de terreno
    - Rápida: Computação O(1), útil para busca em tempo real

    Esta heurística é usada tanto por Busca Gulosa Melhor-Primeiro (para guiar para objetivo) quanto por A*
    (para guiar enquanto mantém otimalidade).

    Args:
        state: O estado atual (com atributos row e col).
        goal: O estado objetivo (com atributos row e col).

    Returns:
        Um float representando a distância Manhattan de estado até objetivo.
    """
    # |row_estado - row_objetivo| contabiliza distância vertical
    # |col_estado - col_objetivo| contabiliza distância horizontal
    # Soma é o número mínimo de movimentos ortogonais necessários
    return abs(state.row - goal.row) + abs(state.col - goal.col)
