# Contexto do Projeto — Navegação 2D com Inteligência Artificial

> Documento de contexto para elaboração do relatório académico.
> Cobre: objetivo do trabalho, fundamentos teóricos, implementação completa, interface gráfica e análise dos resultados.

---

## 1. Objetivo do Trabalho

Este é um Trabalho Prático (TP) da unidade curricular de **Inteligência Artificial**. O objetivo é implementar e comparar três algoritmos clássicos de busca num mapa em grelha 2D:

- **BFS** — Busca em Largura (não informada)
- **Greedy Best-First** — Busca Gulosa (informada)
- **A\*** — A-estrela (informada)

O programa permite ao utilizador desenhar o mapa (colocar obstáculos, terreno difícil, armadilhas e inimigos), definir um ponto de início e um objetivo, correr os algoritmos e observar visualmente o caminho encontrado e as métricas de desempenho.

---

## 2. Fundamentos Teóricos

### 2.1 O que é um Problema de Busca?

Um **problema de busca** é uma forma formal de descrever a navegação num espaço de possibilidades. Define-se com quatro elementos:

| Componente | Significado |
|---|---|
| **Estado inicial** | Onde o agente começa (posição de início) |
| **Objetivo** | Onde o agente quer chegar |
| **Ações** | Movimentos possíveis (cima, baixo, esquerda, direita) |
| **Custo de passo** | Custo de mover de uma célula para a seguinte |

O algoritmo de busca explora os estados a partir do início, expandindo os vizinhos de cada posição, até encontrar o objetivo.

### 2.2 Espaço de Estados

Neste projeto, o espaço de estados é uma **grelha 2D** de células. Cada célula é um estado. O algoritmo começa no estado inicial, gera os estados vizinhos (células adjacentes não bloqueadas) e repete até chegar ao objetivo ou esgotar todas as possibilidades.

### 2.3 Busca Não Informada vs. Busca Informada

| Tipo | Descrição | Exemplo |
|---|---|---|
| **Não informada** | Explora sem saber onde está o objetivo | BFS, DFS |
| **Informada** | Usa uma **heurística** (estimativa da distância ao objetivo) para guiar a busca | Greedy, A* |

Uma **heurística** é uma função `h(n)` que estima o custo de chegar do estado `n` ao objetivo, sem conhecer o caminho real.

---

## 3. Algoritmos Implementados

### 3.1 BFS — Busca em Largura

**Ideia:** Explora todos os nós a uma profundidade antes de avançar para a próxima. Garante encontrar o caminho com **menos passos** (menos células percorridas).

**Como funciona:**
1. Coloca o estado inicial numa fila (FIFO — primeiro a entrar, primeiro a sair).
2. Retira o primeiro estado da fila e expande os seus vizinhos.
3. Cada vizinho ainda não visitado é adicionado ao fim da fila.
4. Repete até chegar ao objetivo ou a fila ficar vazia.

**Propriedades:**
- **Completo:** Encontra sempre a solução se existir.
- **Ótimo em passos:** O caminho encontrado tem o menor número de células.
- **Não ótimo em custo:** Ignora os custos de terreno (uma célula difícil custa o mesmo que uma célula livre).
- **Memória:** Guarda todos os nós gerados — pode ser lento em mapas grandes.

**Estrutura de dados:** `collections.deque` (fila dupla eficiente)

**Fórmula de ordenação:** Nenhuma — FIFO puro.

**Ficheiro:** `algorithms/bfs.py`

---

### 3.2 Greedy Best-First — Busca Gulosa

**Ideia:** Sempre expande o nó que parece estar mais perto do objetivo segundo a heurística. É rápido, mas não garante o caminho de menor custo.

**Como funciona:**
1. Coloca o estado inicial numa fila de prioridade (heap), com prioridade `h(n)`.
2. Retira sempre o nó com menor `h(n)` (o "mais próximo" do objetivo).
3. Expande os seus vizinhos e insere-os na fila com as respetivas prioridades.
4. Repete até encontrar o objetivo ou a fila ficar vazia.

**Propriedades:**
- **Rápido:** Tende a explorar poucos nós porque vai diretamente em direção ao objetivo.
- **Não ótimo:** Pode encontrar um caminho mais longo ou mais caro porque não considera o custo já percorrido.
- **Pode falhar em labirintos:** Pode ficar preso em becos sem saída se a heurística não o guiar bem.

**Fórmula de ordenação:** `f(n) = h(n)` (apenas a estimativa ao objetivo)

**Ficheiro:** `algorithms/greedy.py`

---

### 3.3 A\* — A-Estrela

**Ideia:** Combina o custo real já percorrido `g(n)` com a estimativa heurística `h(n)`. É o algoritmo de referência para navegação — **ótimo e completo** quando a heurística é admissível.

**Como funciona:**
1. Coloca o estado inicial numa fila de prioridade com `f(n) = g(n) + h(n)`.
2. Retira sempre o nó com menor `f(n)`.
3. Expande os vizinhos: para cada um, calcula `g_novo = g(atual) + custo_passo`. Se melhorar o custo conhecido, atualiza e insere na fila.
4. Repete até encontrar o objetivo.

**Propriedades:**
- **Completo:** Encontra sempre a solução se existir.
- **Ótimo em custo:** Garante o caminho de menor custo total (quando `h` é admissível).
- **Eficiente:** Melhor que BFS em mapas grandes porque guia-se pela heurística.

**Fórmula de ordenação:** `f(n) = g(n) + h(n)`

| Símbolo | Significado |
|---|---|
| `g(n)` | Custo real acumulado desde o início até ao nó `n` |
| `h(n)` | Estimativa heurística do custo de `n` ao objetivo |
| `f(n)` | Estimativa do custo total do caminho passando por `n` |

**Ficheiro:** `algorithms/astar.py`

---

### 3.4 Heurística de Manhattan

Todos os algoritmos informados (Greedy e A\*) usam a **distância de Manhattan** como heurística:

```
h(n) = |linha_n - linha_objetivo| + |coluna_n - coluna_objetivo|
```

Esta heurística conta o número mínimo de passos ortogonais (sem diagonais) entre dois pontos. É **admissível** porque nunca sobrestima o custo real (assume custo mínimo = 1 por passo), o que garante a optimalidade do A\*.

**Ficheiro:** `algorithms/heuristics.py`

---

## 4. Modelação Formal do Problema

### 4.1 Estado (`model/state.py`)

Um estado representa uma posição na grelha: `State(row, col)`.

- É **hashável** (pode ser usado como chave em dicionários e conjuntos).
- Dois estados são iguais se têm a mesma linha e coluna.
- Os algoritmos usam-no como chave no dicionário `parent` (para reconstruir o caminho) e no conjunto `visited` (para evitar revisitar posições).

### 4.2 Grelha (`model/grid.py`)

A grelha é uma matriz 2D de inteiros. Cada célula tem um tipo e um custo associado:

| Tipo | Constante | Valor inteiro | Custo de traversal | Notas |
|---|---|---|---|---|
| Livre | `FREE` | 0 | 1 | Normal |
| Obstáculo | `OBSTACLE` | 1 | ∞ | Intransponível |
| Armadilha | `TRAP` | 2 | 5 | Penaliza muito |
| Difícil | `DIFFICULT` | 3 | 3 | Penaliza moderadamente |
| Inimigo | `ENEMY` | 4 | 1 | Custo normal algoritmicamente; fatal na animação |

A grelha suporta redimensionamento dinâmico (entre 3×3 e 100×100), preservando as células existentes.

### 4.3 Problema (`model/problem.py`)

A classe `Problem` encapsula o problema de busca e fornece as operações que os algoritmos precisam:

| Método | O que faz |
|---|---|
| `actions(state)` | Devolve os movimentos válidos (exclui limites, obstáculos e, opcionalmente, inimigos) |
| `result(state, action)` | Aplica a ação e devolve o novo estado |
| `step_cost(state, action)` | Devolve o custo de ir para a célula vizinha |
| `is_goal(state)` | Verifica se chegámos ao objetivo |

O parâmetro `avoid_enemies=True` controla se as células com inimigos são consideradas válidas. O programa tenta primeiro resolver evitando inimigos; se não encontrar caminho, tenta passando por eles.

---

## 5. Saída dos Algoritmos

Todos os algoritmos têm a mesma assinatura e retornam o mesmo formato de dicionário:

```python
def bfs(problem: Problem) -> dict:
    ...
    return {
        "path":     list[tuple[int,int]] | None,  # caminho de células, ou None se sem solução
        "explored": list[tuple[int,int]],          # ordem de expansão (para animação)
        "expanded": int,                           # número de nós expandidos
        "cost":     float | None,                  # custo total do terreno no caminho
        "time":     float,                         # tempo de execução em segundos
    }
```

O campo `"path"` é `None` quando não existe solução. O campo `"explored"` é usado para animar a progressão da busca no ecrã.

Após a execução, o `App` adiciona `"travel_time_s"` (tempo estimado de animação com base nos atrasos por célula).

---

## 6. Métricas e Comparação (`metrics/tracker.py`)

A classe `Metrics` regista os resultados de cada algoritmo e produz tabelas de comparação.

### Métricas recolhidas:

| Métrica | Significado |
|---|---|
| **Custo total** | Soma dos custos de terreno ao longo do caminho |
| **Nós expandidos** | Quantas células o algoritmo abriu/processou |
| **Passos do caminho** | Número de células no caminho (comprimento) |
| **Tempo de computação (ms)** | Tempo de execução do algoritmo |
| **Tempo de viagem (s)** | Estimativa de tempo de animação (varia com o terreno) |

Na tabela de comparação, o **melhor valor de cada coluna** é destacado a verde (lime). No modo terminal (`python main.py --test`), as métricas são impressas em formato de tabela ASCII.

---

## 7. Arquitetura do Programa

### 7.1 Estrutura de Ficheiros

```
projeto_ia/
├── main.py                  # Ponto de entrada; modo GUI ou modo --test
│
├── model/                   # Dados puros — sem Pygame
│   ├── grid.py              # Grelha 2D, tipos de célula, custos
│   ├── state.py             # State(row, col) — hashável
│   └── problem.py           # Problem — interface dos algoritmos
│
├── algorithms/              # Funções stateless; cada uma devolve o mesmo dict
│   ├── bfs.py               # Busca em Largura
│   ├── greedy.py            # Busca Gulosa (heurística h(n))
│   ├── astar.py             # A* (f(n) = g(n) + h(n))
│   └── heuristics.py        # manhattan(state, goal) → float
│
├── metrics/
│   └── tracker.py           # Metrics: registo e comparação de resultados
│
└── ui/                      # Interface gráfica Pygame
    ├── app.py               # App — loop principal, eventos, animação
    ├── grid_view.py         # GridView — renderiza a grelha
    ├── controls.py          # ControlsPanel — painel lateral e tabela
    └── icons.py             # Ícones vetoriais em Pygame (sem imagens externas)
```

### 7.2 Separação de responsabilidades

O projeto segue uma separação clara entre dados e apresentação:

- `model/` não importa Pygame em nenhum momento — é puro Python.
- `algorithms/` recebem um `Problem` e devolvem um `dict` — são independentes da UI.
- `ui/` usa o modelo e os algoritmos mas não conhece os seus detalhes internos.
- `metrics/` é agnóstico à UI — funciona tanto em modo terminal como em GUI.

---

## 8. Interface Gráfica

### 8.1 Modo de Execução

```bash
python main.py          # Abre a janela Pygame
python main.py --test   # Corre 4 cenários em terminal e imprime métricas
```

A dependência externa é apenas `pygame`. Instalar com: `pip install pygame`

### 8.2 Layout da Janela

A janela (1060×730 por omissão, redimensionável) divide-se em:

```
┌─────────────────────────────────────────────────────┐
│ Barra de menus (Ficheiro | Ajuda)                   │
│ Título: "Navegação de Personagem em Grelha 2D ..."  │
├──────────────┬──────────────────────────────────────┤
│ Grelha│Análise (tabs)            Painel de controlo │
│                                                     │
│  [Área da grelha 2D]        [Botões + Tabela]       │
│                                                     │
│ Separador arrastável ↕                              │
└─────────────────────────────────────────────────────┘
```

O separador vertical entre a grelha e o painel pode ser arrastado para redimensionar ambas as áreas.

### 8.3 Tab "Grelha"

Permite editar o mapa e correr os algoritmos.

**Modos de edição (painel lateral):**
- `Início (S)` — define o ponto de partida
- `Objetivo (G)` — define o ponto de chegada
- `Obstáculo` — célula intransponível
- `Difícil` — célula com custo 3
- `Armadilha` — célula com custo 5
- `Inimigo` — célula que mata o personagem na animação
- `Apagar` — restaura a célula para "Livre"

Clicar e arrastar aplica o modo em múltiplas células. Botão direito abre um menu de contexto.

**Botões de ação:**
- `Executar` — corre o algoritmo selecionado
- `Executar Todos` — corre BFS, Greedy e A* e compara na tabela
- `Animar Caminho` — anima o caminho célula a célula
- `Limpar Caminho` — remove o resultado sem alterar o mapa
- `Limpar Tudo` — repõe o mapa ao estado inicial

**Atalhos de teclado:**
- `Ctrl+S` — guardar mapa em JSON
- `Ctrl+O` — carregar mapa de JSON
- `Esc` — fechar menus / sair

### 8.4 Tab "Análise"

Vista de análise comparativa, com scroll. Mostra:
1. Tabela de métricas com todos os algoritmos (melhor valor destacado a verde).
2. Gráficos de barras horizontais para cada métrica (custo, nós, passos, tempo, tempo de viagem). A barra mais curta (melhor valor) é marcada com ★.

### 8.5 Animação

Quando se carrega em "Animar Caminho", a aplicação reproduz a busca em dois momentos:

1. **Células exploradas** (azul/cinzento) — aparecem rapidamente em lotes (16 ms por lote) mostrando a progressão da busca.
2. **Caminho final** (verde/amarelo) — aparece célula a célula com atrasos que dependem do terreno:
   - Livre: 100 ms por célula
   - Difícil: 350 ms por célula
   - Armadilha: 700 ms por célula

Se o caminho passar por uma célula com **Inimigo**, a animação para e o personagem é marcado como "capturado".

### 8.6 Guardar e Carregar Mapas

Os mapas são guardados em formato JSON com a estrutura:

```json
{
  "rows": 15,
  "cols": 18,
  "cells": [[0, 1, 0, ...], ...],
  "start": [2, 3],
  "goal":  [12, 15]
}
```

O diálogo de ficheiro abre numa janela tkinter separada (subprocess) para evitar conflitos com Pygame no macOS.

---

## 9. Lógica de Resolução com Inimigos (Two-Pass)

O programa usa uma estratégia em dois passos quando existem inimigos no mapa:

1. **Primeira tentativa:** resolve com `avoid_enemies=True` — os inimigos são tratados como obstáculos.
2. **Se não há solução:** resolve novamente com `avoid_enemies=False` — o algoritmo passa pelos inimigos.

Isto permite que a animação ainda mostre o personagem a chegar ao objetivo mesmo que o único caminho passe por inimigos, ativando o estado de "capturado" durante a animação.

---

## 10. Casos de Teste (Modo Terminal)

Executar `python main.py --test` corre automaticamente 4 cenários:

| Caso | Descrição | O que testa |
|---|---|---|
| 1 | 5×5 sem obstáculos, (0,0)→(4,4) | Caso base, todos os algoritmos encontram o caminho |
| 2 | 10×10 com vários obstáculos, (0,0)→(9,9) | Capacidade de contornar obstáculos |
| 3 | 5×5 com coluna completamente bloqueada | Cenário sem solução — todos devem retornar `None` |
| 4 | 8×8 com metade em terreno difícil e uma armadilha | Impacto dos custos de terreno nas métricas |

A saída é uma tabela ASCII por caso, com custo, nós expandidos, passos e tempo.

---

## 11. Análise Comparativa dos Algoritmos

### Comportamento esperado

| Cenário | BFS | Greedy | A* |
|---|---|---|---|
| Mapa simples sem obstáculos | Ótimo em passos; custo pode não ser mínimo | Rápido, poucas expansões | Ótimo em custo |
| Mapa com terrenos de custo variado | Ignora custos, caminho errado | Pode escolher caminho mais caro | Escolhe sempre o mais barato |
| Mapa com labirinto complexo | Explora muitas células | Pode falhar ou demorar | Eficiente e correto |
| Sem solução | Expande tudo, reporta sem solução | Expande menos, reporta sem solução | Expande menos que BFS, reporta sem solução |

### Tradeoffs principais

- **BFS vs A\*:** BFS garante o menor número de passos; A\* garante o menor custo. Quando todos os terrenos têm custo igual, os dois coincidem.
- **Greedy vs A\*:** Greedy é mais rápido (menos nós expandidos) mas não é ótimo. A\* é mais lento mas encontra sempre o caminho de menor custo.
- **Nós expandidos:** BFS expande mais nós que A\* na maioria dos casos porque não tem heurística para se guiar.

---

## 12. Tecnologias e Dependências

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| Pygame | Janela gráfica, renderização, eventos |
| `collections.deque` | Fila FIFO para BFS |
| `heapq` | Fila de prioridade para Greedy e A\* |
| `json` | Serialização dos mapas |
| `tkinter` (subprocess) | Diálogo de ficheiro no macOS |
| `time.perf_counter` | Medição precisa do tempo dos algoritmos |

Não há dependências de aprendizagem automática nem bibliotecas de IA externas — todos os algoritmos estão implementados manualmente.

---

## 13. Design Visual

O projeto usa a paleta **AIOX Dark Cockpit**:

| Papel | Cor | Hex |
|---|---|---|
| Fundo | Preto-quase | `#050505` |
| Superfície painéis | Quase-preto azulado | `#0F0F11` |
| Texto principal | Creme | `#F4F4E8` |
| Destaque / melhor valor | Lima | `#D1FF00` |
| Erro / capturado | Laranja-vermelho | `#ED4609` |
| Texto secundário | Cinzento | `#9C9C9C` |

Todos os ícones (guardar, abrir, apagar, ajuda, etc.) são desenhados vetorialmente em Pygame em tempo de execução — não há ficheiros de imagem externos.

---

## 14. Resumo para o Relatório

Para o relatório académico, os pontos mais relevantes a desenvolver são:

1. **Introdução:** objetivo do trabalho, algoritmos escolhidos e motivação.
2. **Fundamentação teórica:** o que é busca em espaço de estados, diferença entre busca informada e não informada, como funciona cada algoritmo (com pseudocódigo ou diagramas).
3. **Modelação do problema:** como o mapa foi modelado (grelha, estados, custos de terreno).
4. **Implementação:** arquitetura do programa, decisões de design (separação modelo/UI, contrato dos algoritmos, two-pass para inimigos).
5. **Resultados:** tabela de métricas dos 4 casos de teste, análise dos gráficos gerados pelo programa.
6. **Conclusão:** qual o melhor algoritmo para cada tipo de cenário e porquê.

Para obter os resultados: correr `python main.py --test` e guardar a saída; ou usar a GUI, clicar "Executar Todos" em cada cenário e consultar a tab "Análise".
