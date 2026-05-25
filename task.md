# TASK.MD — Regras para Gerar Novos Slides

> Documento de referência de estilo e animação do `index.html`.
> Usar estas regras ao gerar qualquer novo slide — ignorar o conteúdo específico do projeto atual.

---

## 1. Design Tokens (CSS Variables)

```css
--bg:    #050505   /* fundo principal — quase preto */
--fg:    #F4F4E8   /* texto principal — cream */
--card:  #0F0F11   /* fundo de cards */
--panel: #111113   /* fundo de painéis secundários */
--con:   #12130F   /* fundo de blocos de código */
--lime:  #D1FF00   /* acento principal — lima */
--l04:   rgba(209,255,0,.04)  /* lime 4% — ghost words */
--l08:   rgba(209,255,0,.08)  /* lime 8% — hl background */
--l20:   rgba(209,255,0,.20)  /* lime 20% — hl border */
--flare: #ED4609   /* erro / perigo — laranja */
--blue:  #0099FF   /* strings de código / info */
--meta:  #9C9C9C   /* texto secundário / labels */
--b:     rgba(156,156,156,.15)  /* borda padrão */
--bs:    rgba(156,156,156,.45)  /* borda forte */
```

---

## 2. Tipografia

| Família | Variável | Uso |
|---|---|---|
| `Space Grotesk` | `--fd` | Títulos `.dt`, `.st`, `.ct` |
| `Inter` | `--fb` | Corpo de texto, `.lead`, `<p>` |
| `JetBrains Mono` | `--fm` | Código, labels, `.ey`, `.k2`, `.br` |

### Classes de texto

```
.ey   — eyebrow/label: mono 10px 600, uppercase, .22em spacing, lime
.dt   — display title: Space Grotesk clamp(36px,5.5vw,76px) 800, uppercase, -.04em, cream
         → .ac dentro de .dt = span com color: var(--lime)
.st   — section title: Space Grotesk 34px 800, uppercase, -.03em, cream
.lead — parágrafo lead: Inter 15px 400, 1.6 line-height, meta, max-width 580px
```

---

## 3. Estrutura de um Slide (`.step`)

```html
<div class="step" id="sN" data-x="X" data-y="Y" data-rz="DEG" data-s="SCALE">
  <!-- opcional: palavra fantasma -->
  <div class="bgw">PALAVRA</div>

  <!-- eyebrow obrigatório -->
  <div class="ey">[NUM] TÍTULO DO TEMA</div>

  <!-- título da secção -->
  <div class="st">Subtítulo do Slide</div>

  <!-- conteúdo: g2, g3, cb, tb, hl, fm2, pill, sl, bl, dr... -->
</div>
```

**Dimensões fixas:** `width: 1000px`, `min-height: 680px`, `padding: 44px 58px 60px`

**Grid de fundo:** automático via `.step::before` — linhas 50px × 50px em `--b`

**Opacidade:** `.step` = 0.15 por padrão; `.step.active` = 1.0

---

## 4. Posicionamento no Canvas 3D

O canvas usa coordenadas absolutas em pixels. Espaçamento da grelha padrão:

- **Horizontal:** 1200px entre colunas
- **Vertical:** 860px entre linhas

```
data-x="0"    data-x="1200"  data-x="2400"  data-x="3600"  data-x="4800"
data-y="0"    → linha 0
data-y="860"  → linha 1
data-y="1720" → linha 2
data-y="2580" → linha 3
```

**Rotação** (`data-rz`): valores pequenos criam dinamismo — ex: `2`, `-2`, `3`. A maioria fica em `0`.

**Escala** (`data-s`): normalmente `1`. Slide de encerramento pode usar `1.06` para destaque subtil.

---

## 5. Componentes de Layout

### Grid de colunas
```html
<div class="g2">…</div>   <!-- 2 colunas, gap 12px -->
<div class="g3">…</div>   <!-- 3 colunas, gap 10px -->
```

### Card
```html
<div class="card">
  <div class="ct">
    <span class="br">[BADGE]</span>
    TÍTULO DO CARD
  </div>
  <!-- conteúdo: .dr, <p>, .bl, etc. -->
</div>
```
- `.card` recebe tilt 3D magnético no hover (max 12°, glare)
- `.ct` — Space Grotesk 13px 800, uppercase
- `.br` — mono 9px, lime, `display:block`, .15em spacing

### Data Row (`.dr`)
```html
<div class="dr">
  <span class="k2">LABEL</span>
  <span class="v lm">valor lime</span>
</div>
```
- `.k2` — meta, mono, 9px, uppercase, .12em spacing
- `.v` — cream (padrão)
- `.v.lm` — lime
- `.v.fl` — flare/erro

### Pill
```html
<div class="pill">
  <div class="dot"></div>          <!-- lime -->
  <div class="dot b"></div>        <!-- blue -->
  <div class="dot f"></div>        <!-- flare -->
  <span style="font-family:var(--fm);font-size:10px;letter-spacing:.10em;text-transform:uppercase">LABEL</span>
</div>
```

### Highlight (`.hl`)
```html
<div class="hl">Texto com <strong>destaque</strong> em lime.</div>
```
- Fundo `--l08`, borda `--l20`, borda-esquerda 3px lima
- `strong` dentro = lime

### Fórmula (`.fm2`)
```html
<div class="fm2">f(n) = g(n) + h(n)</div>
```
- Fundo `--card`, borda-esquerda 3px lima, mono 14px 600, lime

### Bloco de código (`.cb`)
```html
<div class="cb"><span class="k">keyword</span> code <span class="cm"># comentário</span></div>
```
- `.k` = lime (keyword)
- `.cm` = meta (comentário)
- `.s` = blue (string)
- Fundo `--con`, mono 11px, `white-space:pre`

### Tabela (`.tb`)
```html
<table class="tb">
  <thead><tr><th>Col A</th><th>Col B</th></tr></thead>
  <tbody>
    <tr><td class="lm">valor lime</td><td>normal</td></tr>
    <tr><td class="fl">erro</td><td class="mt">meta</td></tr>
  </tbody>
</table>
```
- `th` — mono 9px, lime, uppercase, .15em spacing
- `.lm` / `.fl` / `.mt` nas células para lime / flare / meta

### Listas

**Numerada** (`.sl`):
```html
<ol class="sl">
  <li>Item um</li>
  <li>Item dois</li>
</ol>
```
→ contador `0N` em lime à esquerda

**Marcadores** (`.bl`):
```html
<ul class="bl">
  <li>Item</li>
</ul>
```
→ `//` em lime à esquerda

### Ghost background word (`.bgw`)
```html
<div class="bgw">PALAVRA</div>
```
- Posição: `bottom: 56px; right: 56px`
- Tamanho: `clamp(80px,14vw,200px)`, weight 800, uppercase
- Cor: `--l04` (lime 4% — quase invisível)
- `pointer-events:none`, `z-index:0`

---

## 6. Sistema de Animação (Canvas FX)

O `<canvas id="fx">` sobrepõe tudo em `z-index:500` e desenha via `requestAnimationFrame`.

### Modo Normal (slide activo)
- **Breathing glow:** radial gradient centrado no slide, pulsa com `sin(t * 1.3)`, amplitude `0.4 + 0.25 * sin` → `fillStyle rgba(209,255,0,pulse*0.05)`
- **Corner brackets:** 4 cantos em lime com `shadowBlur:14`, pulsam com o mesmo sin, alpha `pulse * 0.75`

### Modo Overview (`Tab`)
- **Ambient outline:** todos os slides com `strokeStyle rgba(209,255,0, 0.05+0.02*sin(t*.6+i*.45))`, `lineWidth 0.5`
- **Hover aura:** lerp `aura[i] += (target - aura[i]) * 0.075`
  - Radial gradient bloom centrado no slide
  - Glowing border com `shadowBlur: 22 * alpha`
  - Label `[01]` a lime acima do slide quando `alpha > 0.25`
  - Pulse: `0.65 + 0.35 * Math.sin(t * 2.8)`

### Tilt 3D — Cards e Tabelas
```
LERP = 0.13
MAX cards (.card) = 12°
MAX tables (.tb standalone) = 6°
```
- `mouseenter` → `borderColor rgba(209,255,0,.28)`, `boxShadow 0 0 0 1px rgba(209,255,0,.10), 0 10px 32px rgba(0,0,0,.55)`
- Glare: `radial-gradient` segue rato, `rgba(209,255,0,.09)`
- `transform: perspective(700px) rotateX(rx) rotateY(ry)`

### Tilt 3D — Steps (modo overview)
```
LERP = 0.11
MAX = 10°
```
- Wrapper interno `perspective:800px` → não altera `getBoundingClientRect()` do step
- Glare: `rgba(209,255,0,.06)`
- `outline 1px solid rgba(209,255,0,.22)` no hover

---

## 7. Navegação e HUD

### HUD (fixo no rodapé)
```
height: 52px, background rgba(5,5,5,.92), backdrop-filter blur(10px)
border-top: 1px solid --b
font: JetBrains Mono 10px 600, uppercase, .15em spacing, meta
```
- Contador `[01 / 15]` — número activo em lima (`#hcur`)
- Barra de progresso `#pf` — lime, `transition width .5s ease`
- Dicas de teclado com `<kbd>` estilizados

### Teclado
| Tecla | Acção |
|---|---|
| `→` `↓` `Space` `PgDn` | Avançar |
| `←` `↑` `PgUp` | Recuar |
| `Home` | Primeiro slide |
| `End` | Último slide |
| `Tab` | Entrar/sair Overview |
| `Esc` `O` | Toggle Overview |

### Touch
- Swipe horizontal > 50px → navegar

---

## 8. Transições de Câmara

```js
transition: 'transform 850ms cubic-bezier(.33,0,.67,1)'
```

**Ir para slide:**
```js
cvs.style.transform =
  `perspective(1500px) scale(sc) rotateZ(${-rz}deg) translate3d(${-x}px,${-y}px,0)`
```
(A câmara contra-roda o `data-rz` do slide activo)

**Overview:**
```js
const sc = Math.min(
  window.innerWidth         / 6600,
  (window.innerHeight - 52) / 4200
)
cvs.style.transform = `perspective(1500px) scale(${sc}) translate3d(-2400px,-1300px,0)`
```

---

## 9. Regras para Adicionar um Novo Slide

1. **ID sequencial:** `id="sN"` onde N = número seguinte
2. **Posição:** escolher coordenadas livres na grelha (incrementos de 1200x / 860y)
3. **Rotação:** opcional, usar valores pequenos (`-3` a `3`) para variedade
4. **Estrutura mínima obrigatória:**
   - `.ey` com número de secção e tema
   - `.st` ou `.dt` com título
5. **Conteúdo:** escolher entre `g2`, `g3`, `cb`, `tb`, `hl`, `fm2`, `sl`, `bl`, `dr` conforme o tipo de informação
6. **Actualizar `TOTAL`** na variável JS e o texto `[htot]` no HUD
7. **Nunca alterar** os scripts de animação nem as variáveis CSS — apenas adicionar slides no HTML

---

## 10. Padrões de Slide por Tipo

| Tipo | Layout sugerido | Componentes |
|---|---|---|
| Capa | coluna única + `.bgw` | `.dt` com `.ac`, `.lead`, pills `.cm2` |
| Conceito | `.g2` | card esquerda + `.hl` ou `.fm2` direita |
| Algoritmo / Código | `.g2` | `.cb` esquerda + card propriedades direita |
| Comparação | `.tb` full-width + `.g3` | tabela + 3 `.hl` |
| Arquitectura | `.g2` | `.cb` árvore esquerda + cards direita |
| Lista de passos | `.g2` | `.sl` esquerda + card direita |
| Encerramento | `.g3` + `.bgw` | 6 cards 2×3 |
