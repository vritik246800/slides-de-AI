"""
Módulo: metrics.tracker
========================

Responsabilidade: Coleta, armazenamento e formatação de métricas de desempenho dos algoritmos de busca.

Este módulo fornece a classe `Metrics` que atua como um registrador centralizado para os resultados
de execução de cada algoritmo (BFS, Greedy Best-First, A*). Captura informações críticas como:
  - Custo total da rota encontrada (soma dos custos de terreno)
  - Número de nós expandidos durante a busca
  - Número de passos na solução final
  - Tempo de execução do algoritmo
  - Tempo total de viagem (animação)
  - Se uma solução foi encontrada

Os dados são armazenados em formato padronizado (dict) para facilitar comparação entre algoritmos,
exportação para a UI (tabelas e gráficos), e geração de relatórios em texto para depuração.

Uso típico:
  1. Criar instância: metrics = Metrics()
  2. Registrar resultados: metrics.record("BFS", algorithm_result_dict)
  3. Obter dados formatados: metrics.to_rows()  # para UI
  4. Exibir resumo: print(metrics.summary())    # para terminal
"""


class Metrics:
    """
    Classe responsável pelo rastreamento e comparação de métricas dos algoritmos de busca.

    Atributos:
        results (dict): Dicionário que mapeia nomes de algoritmos para seus resultados.
                       Formato esperado de cada resultado:
                       {
                           "path": list[tuple] or None,    # Sequência de (row, col) da solução
                           "cost": float or None,           # Custo total do caminho (terreno)
                           "expanded": int,                 # Quantidade de nós expandidos
                           "time": float,                   # Tempo de execução em segundos
                           "travel_time_s": float (opt.)    # Tempo de animação em segundos
                       }
    """

    def __init__(self):
        """
        Inicializa a instância de Metrics com um dicionário vazio de resultados.

        Chamado uma vez por sessão da aplicação. Cada novo experimento deve chamar
        clear() se quiser resetar os dados anteriores.
        """
        self.results: dict = {}

    def record(self, algorithm_name: str, result: dict) -> None:
        """
        Registra o resultado de um algoritmo em execução.

        Argumentos:
            algorithm_name (str): Nome do algoritmo (ex: "BFS", "Greedy", "A*").
                                 Este nome é usado como chave no dicionário de resultados.
            result (dict): Dicionário contendo as métricas do algoritmo. Deve conter:
                          - "path": list ou None
                          - "cost": float ou None
                          - "expanded": int
                          - "time": float (em segundos)
                          - "travel_time_s": float (opcional)

        Comportamento:
            - Se o algoritmo já foi registrado, sobrescreve os dados anteriores.
            - Nenhuma validação é feita; assume-se que o chamador passou dados válidos.
        """
        self.results[algorithm_name] = result

    def clear(self) -> None:
        """
        Limpa todos os resultados registados.

        Útil entre execuções de testes para garantir que métricas antigas não
        interferem com novas análises. Reutiliza a aplicação para vários mapas/problemas.
        """
        self.results = {}

    def to_dict(self) -> dict:
        """
        Retorna uma cópia de todos os resultados registados em formato de dicionário.

        Retorna:
            dict: Cópia do dicionário interno de resultados.
                 Modificações nesta cópia não afetam o estado da instância Metrics.

        Uso típico:
            - Integração com ferramentas externas de análise
            - Depuração: inspecionar dados brutos de um algoritmo
        """
        return self.results.copy()

    def to_rows(self) -> list:
        """
        Converte os resultados registados em formato tabular para exibição na UI.

        Retorna:
            list[dict]: Lista de dicionários, um por algoritmo, com chaves:
                       - "algo": nome do algoritmo
                       - "found": bool, True se uma solução foi encontrada
                       - "cost": float ou None (custo total, ou None se sem solução)
                       - "expanded": int (número de nós expandidos)
                       - "steps": int ou None (comprimento do caminho, ou None se sem solução)
                       - "time_ms": float (tempo em milissegundos)
                       - "travel_time_s": float ou None (tempo de animação visual)

        Transformações aplicadas:
            1. Converte "time" de segundos para milissegundos (multiplica por 1000)
            2. Cria "steps" a partir do comprimento da lista "path"
            3. Define "found" como True/False baseado na existência de "path"
            4. Define atributos como None quando não há solução (path=None)

        Nota importante:
            Este método assume que o algoritmo executou via App._run() ou App._run_all(),
            que adicionam "travel_time_s" aos resultados. Se for chamado com dados
            que não têm "travel_time_s", retornará None para esse campo.
        """
        rows = []
        # Itera sobre cada algoritmo e seus resultados
        for algo, r in self.results.items():
            rows.append({
                # Nome do algoritmo (chave do dicionário)
                "algo":          algo,
                # Verifica se uma solução foi encontrada (path não é None e não vazio)
                "found":         bool(r["path"]),
                # Custo total: retorna o valor se existe solução, None caso contrário
                "cost":          r["cost"]          if r["path"] else None,
                # Número de nós expandidos durante a busca (sempre presente)
                "expanded":      r["expanded"],
                # Número de passos: comprimento do caminho se existe solução, None caso contrário
                "steps":         len(r["path"])     if r["path"] else None,
                # Tempo de execução convertido para milissegundos (mais legível que segundos)
                "time_ms":       r["time"] * 1000,
                # Tempo total de animação visual (soma dos atrasos de cada célula do caminho)
                # Usa .get() porque nem todos os resultados têm este campo
                "travel_time_s": r.get("travel_time_s"),
            })
        return rows

    def summary(self) -> str:
        """
        Gera um resumo textual formatado com todos os resultados para exibição em terminal.

        Retorna:
            str: String contendo uma tabela formatada ASCII com:
                 - Algoritmo: nome do algoritmo
                 - Custo: custo total da rota (ou "---" se sem solução)
                 - Nós: número de nós expandidos durante a busca
                 - Passos: comprimento do caminho (ou "---" se sem solução)
                 - Tempo: tempo de execução em milissegundos

        Formato:
            Usa uma tabela com bordas de "=" e "-", coluna de algoritmo com 12 caracteres,
            valores numéricos alinhados à direita para facilitar comparação visual.

        Caso especial:
            Se não há resultados registados, retorna a mensagem "Nenhum resultado registado."

        Uso típico:
            print(metrics.summary())  # Modo terminal ou depuração (--test)
        """
        # Tratamento de caso vazio: nenhum algoritmo foi executado
        if not self.results:
            return "Nenhum resultado registado."

        # Largura padrão das colunas em caracteres (usada para alinhamento)
        col_w = 12

        # Constrói a tabela linha por linha
        lines = [
            # Linha de topo com bordas
            "=" * 52,
            # Cabeçalho das colunas: algoritmo alinhado à esquerda, números à direita
            f"{'Algoritmo':<{col_w}} {'Custo':>6} {'Nós':>6} {'Passos':>7} {'Tempo':>10}",
            # Linha separadora
            "-" * 52,
        ]

        # Preenche a tabela com os dados de cada algoritmo
        for algo, r in self.results.items():
            if r["path"]:
                # Caso: solução encontrada — exibe valores reais
                lines.append(
                    # Algoritmo à esquerda (12 chars), custo/nós/passos/tempo alinhados à direita
                    f"{algo:<{col_w}} {r['cost']:>6} {r['expanded']:>6} "
                    f"{len(r['path']):>7} {r['time'] * 1000:>8.2f}ms"
                )
            else:
                # Caso: sem solução — exibe "---" para campos não aplicáveis (custo e passos)
                # Nós expandidos e tempo de busca continuam sendo exibidos (máquina tentou buscar)
                lines.append(
                    f"{algo:<{col_w}} {'---':>6} {r['expanded']:>6} "
                    f"{'---':>7} {r['time'] * 1000:>8.2f}ms"
                )

        # Fecha a tabela com linha de rodapé
        lines.append("=" * 52)

        # Retorna a tabela como string única, com linhas separadas por quebra de linha
        return "\n".join(lines)
