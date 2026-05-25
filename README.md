# App_Navegacao — Navegação de Personagem em Grelha 2D

> Trabalho Prático — Unidade Curricular de **Inteligência Artificial**  
> Grupo 5 · Licenciatura em Engenharia Informática

---

## Visão Geral

**App_Navegacao** é uma aplicação interativa de navegação inteligente num mapa em grelha 2D. O programa implementa e compara três algoritmos clássicos de busca em espaço de estados — BFS, Greedy Best-First e A* — com uma interface gráfica completa desenvolvida em Pygame.

O utilizador pode desenhar o mapa (obstáculos, terrenos difíceis, armadilhas e inimigos), definir pontos de início e objetivo, executar os algoritmos e observar em tempo real o caminho encontrado e as métricas de desempenho de cada algoritmo.

---

## Equipa

| Número | Nome |
|---|---|
| 20190025 | Vritik Valabdas |
| 20190461 | Shuraim Hussene Ishakgi |
| 20240187 | Saymara Chambal |
| 20200039 | Martin Daud Ribeiro |
| 20230471 | Rahissa Mahomed Al Yashin |
| 20200612 | Shelton Arlindo |

---

## Funcionalidades

- **Três algoritmos de busca** implementados do zero em Python puro (BFS, Greedy, A*)
- **Interface gráfica Pygame** com edição de mapa em tempo real (clique e arrasto)
- **Animação célula a célula** da exploração e do caminho final com velocidade proporcional ao terreno
- **Modo "Executar Todos"** — corre os três algoritmos em simultâneo e compara as métricas lado a lado
- **Tab de Análise** com tabela de métricas e gráficos de barras horizontais (melhor valor destacado a verde)
- **Persistência de mapas** — guardar e carregar em formato JSON (`Ctrl+S` / `Ctrl+O`)
- **Estratégia Two-Pass** para mapas com inimigos — tenta primeiro evitá-los, senão passa por eles
- **Modo terminal** (`--test`) com 4 casos de teste automáticos e tabela ASCII de resultados
- Todos os ícones são vetoriais desenhados em Pygame — **sem ficheiros de imagem externos**

---

## Algoritmos Implementados

### BFS — Busca em Largura (Não Informada)

Explora todos os nós a uma profundidade antes de avançar. Usa uma fila FIFO (`collections.deque`).

- **Completo:** encontra sempre a solução se existir
- **Ótimo em passos:** garante o menor número de células percorridas
- **Não ótimo em custo:** ignora os custos de terreno
- **Ordenação:** `f(n) = FIFO puro`

### Greedy Best-First (Informada)

Sempre expande o nó com menor estimativa heurística `h(n)`. Usa uma fila de prioridade (`heapq`).

- **Rápido:** tende a explorar poucos nós
- **Não ótimo em custo:** pode escolher caminhos mais caros
- **Pode falhar em labirintos:** sensível a becos sem saída
- **Ordenação:** `f(n) = h(n)`

### A* — A-Estrela (Informada, Ótima)

Combina o custo real percorrido `g(n)` com a estimativa heurística `h(n)`. Ótimo e completo quando `h` é admissível.

- **Completo e ótimo em custo**
- **Eficiente:** guia-se pela heurística, expande menos nós que BFS
- **Degrada para Dijkstra** quando `h(n) = 0`
- **Ordenação:** `f(n) = g(n) + h(n)`

### Heurística de Manhattan

```
h(n) = |linha_n - linha_objetivo| + |coluna_n - coluna_objetivo|
```

Admissível (nunca sobrestima) porque o mapa usa apenas movimentos ortogonais. Garante a optimalidade do A*.

---

## Tipos de Terreno

| Tipo | Custo | Comportamento |
|---|---|---|
| Livre | 1 | Célula normal |
| Difícil | 3 | Penaliza moderadamente |
| Armadilha | 5 | Penaliza muito |
| Inimigo | 1 (algorítmico) | Fatal na animação (capturado) |
| Obstáculo | ∞ | Intransponível |

---

## Arquitetura do Projeto

```
App_Navegacao/
├── main.py                  # Ponto de entrada — modo GUI ou --test
│
├── model/                   # Dados puros — sem Pygame
│   ├── grid.py              # Grelha 2D, tipos de célula, custos
│   ├── state.py             # State(row, col) — hashável
│   └── problem.py           # Problem — interface dos algoritmos
│
├── algorithms/              # Funções stateless, mesma assinatura e saída
│   ├── bfs.py               # Busca em Largura
│   ├── greedy.py            # Busca Gulosa
│   ├── astar.py             # A*
│   └── heuristics.py        # manhattan(state, goal) → float
│
├── metrics/
│   └── tracker.py           # Registo e comparação de métricas
│
└── ui/                      # Interface gráfica Pygame
    ├── app.py               # Loop principal, eventos, animação
    ├── grid_view.py         # Renderização da grelha
    ├── controls.py          # Painel lateral e tabela de métricas
    └── icons.py             # Ícones vetoriais desenhados em runtime
```

### Princípios de Design

- `model/` não importa Pygame — é Python puro e testável de forma independente
- `algorithms/` são **stateless** — recebem um `Problem`, devolvem sempre o mesmo formato de `dict`
- `ui/` usa o modelo e os algoritmos mas não conhece os seus detalhes internos
- `metrics/` é agnóstico à UI — funciona em modo terminal e em GUI

---

## Contrato dos Algoritmos

Todos os algoritmos têm a mesma assinatura e devolvem o mesmo dicionário — são intercambiáveis:

```python
def bfs(problem: Problem) -> dict:
    return {
        "path":     list[tuple] | None,  # caminho ou None se sem solução
        "explored": list[tuple],          # ordem de expansão (para animação)
        "expanded": int,                  # número de nós processados
        "cost":     float | None,         # custo total de terreno
        "time":     float,                # tempo de execução em segundos
    }
```

---

## Instalação e Execução

### Pré-requisitos

- Python 3.10 ou superior
- Pygame

### Instalar dependências

```bash
pip install pygame
```

### Executar

```bash
# Abre a interface gráfica Pygame
python main.py

# Corre os 4 casos de teste em modo terminal
python main.py --test
```

---

## Modos de Uso

### Interface Gráfica

1. Selecionar o modo de edição no painel lateral (Início, Objetivo, Obstáculo, etc.)
2. Clicar ou arrastar na grelha para editar o mapa
3. Selecionar o algoritmo no menu de seleção
4. Clicar **Executar** para correr um algoritmo ou **Executar Todos** para comparar os três
5. Clicar **Animar Caminho** para ver a animação célula a célula
6. Consultar a tab **Análise** para ver métricas e gráficos comparativos

### Atalhos de Teclado

| Atalho | Ação |
|---|---|
| `Ctrl+S` | Guardar mapa em JSON |
| `Ctrl+O` | Carregar mapa de JSON |
| `Esc` | Fechar menus / cancelar |

### Modo Terminal

```bash
python main.py --test
```

Corre automaticamente 4 cenários e imprime uma tabela ASCII de métricas por caso:

| Caso | Mapa | Descrição |
|---|---|---|
| 01 | 5×5 sem obstáculos, (0,0)→(4,4) | Caso base — todos encontram caminho |
| 02 | 10×10 com vários obstáculos, (0,0)→(9,9) | Capacidade de contornar obstáculos |
| 03 | 5×5 com coluna completamente bloqueada | Cenário sem solução — todos retornam `None` |
| 04 | 8×8 com terreno difícil e armadilha | Impacto dos custos de terreno nas métricas |

---

## Métricas Recolhidas

| Métrica | Significado |
|---|---|
| Custo total | Soma dos custos de terreno ao longo do caminho |
| Nós expandidos | Número de células processadas pelo algoritmo |
| Passos do caminho | Comprimento do caminho em número de células |
| Tempo de computação (ms) | Tempo de execução do algoritmo (`time.perf_counter`) |
| Tempo de viagem (s) | Estimativa de tempo de animação baseada nos atrasos por célula |

Na tabela de análise, o **melhor valor de cada coluna** é destacado a verde.

---

## Análise Comparativa

| Cenário | BFS | Greedy | A* |
|---|---|---|---|
| Mapa simples | Ótimo em passos | Rápido, poucas expansões | Ótimo em custo |
| Terreno variado | Ignora custos — caminho errado | Pode escolher caminho mais caro | Escolhe sempre o mais barato |
| Labirinto complexo | Explora muitas células | Pode falhar em becos | Eficiente e correto |
| Sem solução | Expande tudo; reporta `None` | Expande menos; reporta `None` | Expande menos que BFS; reporta `None` |

---

## Estratégia Two-Pass (Inimigos)

Quando existem inimigos no mapa, o programa usa uma estratégia em dois passos:

1. **Primeira tentativa** — resolve com `avoid_enemies=True`: inimigos tratados como obstáculos
2. **Se não há solução** — resolve novamente com `avoid_enemies=False`: algoritmo pode passar pelos inimigos

Na animação, se o caminho passar por uma célula com inimigo, a animação para e o personagem é marcado como **capturado**.

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| Pygame | Interface gráfica, renderização, eventos |
| `collections.deque` | Fila FIFO para BFS |
| `heapq` | Fila de prioridade para Greedy e A* |
| `json` | Serialização/deserialização de mapas |
| `tkinter` (subprocess) | Diálogo de ficheiro nativo no macOS |
| `time.perf_counter` | Medição precisa do tempo de execução |

Não há dependências de aprendizagem automática nem bibliotecas de IA externas — todos os algoritmos estão implementados manualmente em Python puro.

---

## Apresentação Interativa

Os slides da apresentação estão disponíveis em formato HTML interativo com navegação 3D.

**Repositório dos slides:** [github.com/vritik246800/slides-de-AI](https://github.com/vritik246800/slides-de-AI)

---

## Licença

Projeto académico — Unidade Curricular de Inteligência Artificial.  
Todos os direitos reservados ao Grupo 5.
