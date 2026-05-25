"""
Módulo State: Representação imutável de posição na grade.

Este módulo define a classe State, que encapsula uma posição de grade 2D
(linha, coluna). Objetos State são usados em todo o sistema de busca de caminho como:
- Nós em fronteiras de algoritmos de busca (conjuntos abertos, conjuntos fechados)
- Chaves em dicionários e conjuntos (via __hash__ e __eq__)
- Representações de posições ao longo de caminhos solução
- Posições iniciais e de objetivo em definições de Problem

State é projetado para ser hasheável e comparável, permitindo busca eficiente
e deduplicação em implementações de algoritmos. É efetivamente imutável
(atributos não devem ser modificados após criação).
"""


class State:
    """Representa uma posição imutável na grade (linha, coluna).

    Um State encapsula um único ponto na grade 2D de busca de caminho. Cada State
    é identificado unicamente por suas coordenadas (linha, coluna).

    Características principais:
    - Hasheável: pode ser usado como chaves de dicionário e em conjuntos
    - Comparável: verificações de igualdade baseadas em coordenadas
    - Design imutável: atributos não devem ser modificados após criação
    - Conversível para tupla: pode ser convertido para tupla (linha, coluna) para serialização

    Usado por algoritmos de busca para representar nós em suas fronteiras (conjuntos abertos/fechados),
    tornando-se o bloco de construção fundamental do espaço de estado de busca de caminho.
    """

    def __init__(self, row: int, col: int):
        """Inicializa um State em posição da grade (linha, coluna).

        Args:
            row: Índice de linha na grade (0 = topo)
            col: Índice de coluna na grade (0 = esquerda)

        O objeto State é imutável por convenção — linha e coluna não devem
        ser modificadas após criação. A atribuição a self.row/col durante
        inicialização é a única mutação pretendida.
        """
        self.row = row
        self.col = col

    def __eq__(self, other):
        """Verifica igualdade com outro State.

        Args:
            other: Outro objeto para comparar

        Returns:
            True se outro é um State com mesma (linha, coluna), False caso contrário

        Permite que objetos State sejam usados em comparações (ex., state == objetivo)
        e em dicionários/conjuntos para deduplicação. Isto é crítico para
        algoritmos de busca que precisam verificar se um state foi visitado.

        Verificação de tipo previne travamentos se comparando State com objetos não-State.
        """
        if not isinstance(other, State):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        """Retorna hash deste State para uso em dicts e conjuntos.

        Returns:
            Hash inteiro baseado em tupla (linha, coluna)

        Permite que objetos State sejam usados como chaves de dicionário e em conjuntos,
        o qual é essencial para gerenciamento eficiente de fronteira em algoritmos de busca.
        O hash é baseado na tupla (linha, coluna), fazendo com que States com
        as mesmas coordenadas façam hash identicamente.

        Obrigatório junto com __eq__ para manter o invariante:
        "se a == b então hash(a) == hash(b)"
        """
        return hash((self.row, self.col))

    def __repr__(self):
        """Retorna uma representação em string deste State.

        Returns:
            String como "State(5, 3)"

        Usado para debug e logging. Fornece uma representação legível
        do state para inspeção em saída de console ou mensagens de erro.
        """
        return f"State({self.row}, {self.col})"

    def as_tuple(self):
        """Converte este State para uma tupla (linha, coluna).

        Returns:
            Tupla (self.row, self.col)

        Usado para serialização (ex., salvando/carregando mapas) e para passar
        posições de state para funções que esperam tuplas. Útil ao construir
        caminhos de solução para armazenamento ou renderização na UI, que podem
        trabalhar com tuplas em vez de objetos State.
        """
        return (self.row, self.col)
