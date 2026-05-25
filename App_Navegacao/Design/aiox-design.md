---
version: "2.2"
name: "AIOX"
description: "Brutalist-technical dark cockpit system. Neon lime signature, warm cream typography on near-black canvas, TASA Orbiter Display headlines, Geist body, Geist Mono HUD overlays, hairline borders, zero-radius hero, surface-tier elevation. Brazilian-Portuguese AI orchestration system positioned as the antidote to AI-that-replaces-you."
defaultMode: "dark"
supportsDark: true
archetype: "Brutalist-Technical · Dark Cockpit · Neon Signature"
chips:
  - "Lime #D1FF00"
  - "TASA Orbiter Display"
  - "Radius 0px"
  - "HUD bracket overlays"

consumer_contract:
  standalone: true
  goal: "Generate AIOX-style interfaces from this file alone."
  priority_order:
    - "Use semantic tokens first: colors, dark, typography, spacing, rounded, shadows, motion."
    - "Apply component recipes exactly before inventing variants."
    - "Use prose sections for judgment when a token is ambiguous."
    - "Respect Do's and Don'ts over generic framework defaults."
  mode_rule: "Dark mode is the primary product context — most screens are dark. Light mode is reserved for docs/blog and light-tenant overlays. The same lime signature and component library applies in both modes; only the semantic token bindings flip."
  font_rule: "Use TASA Orbiter Display for hero / display moments; Geist for body and UI; Geist Mono for HUD labels, eyebrows, and bracket annotations. Without TASA Orbiter, fall back to Geist Bold — display loses identity but never blocks shipment."
  asset_rule: "Brand requires the AIOX logo (white on dark, black on light, color, negative variants). Do not require photographic imagery — grid, dot, circuit, hazard patterns only."
  accessibility_rule: "Ship WCAG AA contrast, visible lime focus rings, keyboard-operable controls, no body text below 14px, and respect reduced-motion preferences."

colors:
  # Semantic UI color slots (DARK MODE default — the product context)
  primary: "#D1FF00"             # neon lime — signature, focus ring, glow, CTA
  primary-foreground: "#050505"  # near-black fg on lime
  secondary: "#1D1F19"           # ink — body text on light
  secondary-foreground: "#F4F4E8"
  tertiary: "#3D3D3D"            # charcoal — structural neutral
  neutral: "#9C9C9C"             # fg-meta — metadata, HUD labels
  background: "#050505"          # near-black canvas (dark mode default)
  foreground: "#F4F4E8"          # warm cream type on dark
  surface: "#050505"
  surface-foreground: "#F4F4E8"
  card: "#0F0F11"                # elevated dark surface
  card-foreground: "#F4F4E8"
  popover: "#1A1A1C"
  popover-foreground: "#F4F4E8"
  muted: "#1A1A1C"
  muted-foreground: "#9C9C9C"
  accent: "rgba(209, 255, 0, 0.10)"  # lime-10 alpha — subtle backdrop
  accent-foreground: "#D1FF00"
  destructive: "#ED4609"         # flare — warm orange-red, NOT medical red
  destructive-foreground: "#FFFFED"
  border: "rgba(156, 156, 156, 0.15)"   # 1px hairline — primary separator
  border-strong: "rgba(156, 156, 156, 0.45)"
  border-subtle: "rgba(156, 156, 156, 0.10)"
  input: "rgba(156, 156, 156, 0.15)"
  ring: "rgba(209, 255, 0, 0.50)"  # lime focus ring at 50% alpha
  success: "#22C55E"
  warning: "#F59E0B"
  info: "#0099FF"
  chart-1: "#D1FF00"
  chart-2: "#0099FF"
  chart-3: "#ED4609"
  chart-4: "#DDD1BB"
  chart-5: "#9C9C9C"

  # Surface ladder (dark cockpit tiers)
  surface-container-low: "#0A0A0C"     # sunk surface
  surface-container: "#111113"          # default panel
  surface-container-high: "#151518"     # hover surface
  surface-container-highest: "#1C1E19"  # alt panel (lime-tinted)
  surface-bright: "#D1FF00"             # lime editorial panel
  surface-dim: "#000000"                # void anchor
  surface-inverse: "#F4F4E8"            # cream — closing inverse section
  surface-inverse-foreground: "#050505"
  surface-console: "#12130F"            # terminal panel (lime-tinted, h=118)
  surface-overlay: "#1A1A1C"            # popover / dialog
  surface-deep: "#0A0A0C"
  surface-panel: "#111113"
  surface-dark: "#0F0F11"
  surface-alt: "#1C1E19"
  surface-hover: "#151518"
  surface-hover-strong: "#181635"       # pressed (violet-lime mix — brandbook signature)

  # Brand swatch aliases
  lime: "#D1FF00"
  lime-deep: "#A8CC00"
  void: "#000000"
  ink: "#1D1F19"
  ink-soft: "#3D3D3D"
  ink-muted: "#5E5D59"
  cream: "#F4F4E8"
  cream-alt: "#F5F4E7"
  cream-ui: "#F5F5ED"
  warm-white: "#FFFFED"
  fg-meta: "#9C9C9C"
  fg-muted: "#BCBCBC"
  fg-muted-legacy: "#686868"

  # Neutral ramp (5 grayscale stops)
  gray-charcoal: "#3D3D3D"
  gray-dim: "#696969"
  gray-muted: "#999999"
  gray-silver: "#BDBDBD"
  gray-light: "#C2C2C2"

  # Secondary accents — sparing
  blue: "#0099FF"                # informational / data viz
  flare: "#ED4609"               # warm orange-red — destructive
  border-tint-lime: "#333804"    # lime-tinted accent border

  # Status ramp (badge / dot — Tailwind 400 level)
  status-success: "#4ADE80"
  status-warning: "#FBBF24"
  status-error: "#F87171"
  status-info: "#60A5FA"

  # Gold alt-theme (alternate accent system — never on same surface as lime)
  gold: "#DDD1BB"
  gold-dark: "#A89768"
  gold-wash: "#F1E9D6"

  # Lime alpha scale (15 pre-computed levels — the depth mechanism)
  lime-2: "rgba(209, 255, 0, 0.02)"
  lime-3: "rgba(209, 255, 0, 0.03)"
  lime-4: "rgba(209, 255, 0, 0.04)"
  lime-5: "rgba(209, 255, 0, 0.05)"
  lime-6: "rgba(209, 255, 0, 0.06)"
  lime-8: "rgba(209, 255, 0, 0.08)"
  lime-10: "rgba(209, 255, 0, 0.10)"
  lime-12: "rgba(209, 255, 0, 0.12)"
  lime-15: "rgba(209, 255, 0, 0.15)"
  lime-20: "rgba(209, 255, 0, 0.20)"
  lime-25: "rgba(209, 255, 0, 0.25)"
  lime-40: "rgba(209, 255, 0, 0.40)"
  lime-50: "rgba(209, 255, 0, 0.50)"
  lime-75: "rgba(209, 255, 0, 0.75)"
  lime-90: "rgba(209, 255, 0, 0.90)"

  # Lime glow (THE non-border elevation idiom)
  lime-glow: "rgba(209, 255, 0, 0.25)"
  lime-glow-soft: "rgba(209, 255, 0, 0.10)"

dark:
  # The "dark" key documents dark-mode bindings explicitly. AIOX defaults to dark,
  # so this section confirms the canonical product context.
  background: "#050505"
  foreground: "#F4F4E8"
  card: "#0F0F11"
  card-foreground: "#F4F4E8"
  popover: "#1A1A1C"
  popover-foreground: "#F4F4E8"
  primary: "#D1FF00"
  primary-foreground: "#050505"
  secondary: "#111113"
  secondary-foreground: "#F4F4E8"
  muted: "#1A1A1C"
  muted-foreground: "#9C9C9C"
  accent: "rgba(209, 255, 0, 0.10)"
  accent-foreground: "#D1FF00"
  destructive: "#ED4609"
  destructive-foreground: "#FFFFED"
  border: "rgba(156, 156, 156, 0.15)"
  input: "rgba(156, 156, 156, 0.15)"
  ring: "rgba(209, 255, 0, 0.50)"
  surface: "#050505"
  surface-foreground: "#F4F4E8"
  surface-container-low: "#0A0A0C"
  surface-container: "#111113"
  surface-container-high: "#151518"
  surface-container-highest: "#1C1E19"
  surface-bright: "#D1FF00"
  surface-dim: "#000000"
  surface-inverse: "#F4F4E8"
  surface-inverse-foreground: "#050505"
  elevation-raised: "none"
  elevation-floating: "none"
  elevation-overlay: "0 16px 40px rgba(0, 0, 0, 0.40)"
  elevation-modal: "0 24px 64px rgba(0, 0, 0, 0.55)"
  elevation-glow: "0 0 24px rgba(209, 255, 0, 0.25)"
  ink: "#F4F4E8"
  ink-soft: "#BCBCBC"
  ink-muted: "#9C9C9C"

# Light mode (overlay context — docs/blog/light-tenant)
light:
  background: "#F5F4E7"
  foreground: "#1D1F19"
  card: "#FFFFFF"
  card-foreground: "#1D1F19"
  primary: "#D1FF00"
  primary-foreground: "#1D1F19"
  secondary: "#F5F4E7"
  secondary-foreground: "#1D1F19"
  muted: "#F1E9D6"
  muted-foreground: "#686868"
  accent: "rgba(209, 255, 0, 0.15)"
  accent-foreground: "#3D3D3D"
  destructive: "#ED4609"
  destructive-foreground: "#FFFFED"
  border: "rgba(156, 156, 156, 0.24)"
  input: "rgba(0, 0, 0, 0.06)"
  ring: "rgba(209, 255, 0, 0.50)"
  surface: "#F5F4E7"
  surface-inverse: "#050505"
  surface-inverse-foreground: "#F4F4E8"

fonts:
  display: "'TASA Orbiter Display', 'Geist', system-ui, sans-serif"
  body: "'Geist', system-ui, sans-serif"
  eyebrow: "'Geist Mono', 'Roboto Mono', ui-monospace, monospace"
  mono: "'Geist Mono', 'Roboto Mono', ui-monospace, monospace"
  sans: "'Geist', system-ui, sans-serif"
  serif: "'Geist', system-ui, sans-serif"

typography:
  # Hero — TASA Orbiter Display, ALL CAPS, negative tracking
  hero:
    fontFamily: "TASA Orbiter Display, Geist, sans-serif"
    fontSize: 104px
    fontWeight: 800
    lineHeight: 1.0
    letterSpacing: "-0.05em"
    textTransform: "uppercase"
  display:
    fontFamily: "TASA Orbiter Display, Geist, sans-serif"
    fontSize: 64px
    fontWeight: 800
    lineHeight: 1.0
    letterSpacing: "-0.05em"
    textTransform: "uppercase"
  display-2:
    fontFamily: "TASA Orbiter Display, Geist, sans-serif"
    fontSize: 40px
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.03em"
    textTransform: "uppercase"

  # Headings (TASA Orbiter for h1-h4, Geist for h5)
  heading:
    fontFamily: "TASA Orbiter Display, Geist, sans-serif"
    fontSize: 40px
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.03em"
    textTransform: "uppercase"
  title:
    fontFamily: "TASA Orbiter Display, Geist, sans-serif"
    fontSize: 32px
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  subtitle:
    fontFamily: "TASA Orbiter Display, Geist, sans-serif"
    fontSize: 24px
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  h4:
    fontFamily: "TASA Orbiter Display, Geist, sans-serif"
    fontSize: 20px
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  h5:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.01em"

  # Body (Geist sans)
  body-lg:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "0em"
  body:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: "0em"
  body-sm:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"

  # Meta / HUD (Geist Mono — structural labels, bracket overlays)
  caption:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0em"
  label:
    fontFamily: "Geist Mono, monospace"
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.15em"
    textTransform: "uppercase"
  eyebrow:
    fontFamily: "Geist Mono, monospace"
    fontSize: 10px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.20em"
    textTransform: "uppercase"
  bracket:
    fontFamily: "Geist Mono, monospace"
    fontSize: 10px
    fontWeight: 500
    lineHeight: 1.0
    letterSpacing: "0.12em"
    textTransform: "uppercase"
  mono:
    fontFamily: "Geist Mono, Roboto Mono, monospace"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
  micro:
    fontFamily: "Geist Mono, monospace"
    fontSize: 9px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0.14em"
    textTransform: "uppercase"

spacing:
  "0": "0px"
  "1": "4px"
  "2": "8px"
  "3": "12px"
  "4": "16px"
  "5": "20px"
  "6": "24px"
  "8": "32px"
  "10": "40px"
  "12": "48px"
  "14": "56px"
  "16": "64px"
  "20": "80px"
  "24": "96px"
  "32": "128px"
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  section: "96px"
  section-lg: "128px"
  site-margin: "max(1.5rem, calc((100% - 1400px) / 2 + 1.5rem))"
  site-gutter: "24px"
  container-max: "1400px"
  reading-column: "640px"
  inline-media: "880px"

rounded:
  none: "0px"        # brutalist default — hero, display, panels
  sm: "0px"          # inputs, small controls
  md: "0px"          # medium panels, dialogs, dropdowns
  lg: "0px"          # cards
  xl: "0px"          # featured cards
  "2xl": "0px"       # hero CTAs, device mockup frames
  full: "0px"        # AIOX keeps even badges/avatars squared
  button: "0px"
  card: "0px"
  input: "0px"

shadows:
  none: "none"
  hairline: "0 0 0 1px rgba(156, 156, 156, 0.15)"
  hairline-strong: "0 0 0 1px rgba(156, 156, 156, 0.45)"
  glow: "0 0 24px rgba(209, 255, 0, 0.25)"
  glow-soft: "0 0 16px rgba(209, 255, 0, 0.10)"
  glow-strong: "0 0 32px rgba(209, 255, 0, 0.40)"
  overlay: "0 16px 40px rgba(0, 0, 0, 0.40)"
  modal: "0 24px 64px rgba(0, 0, 0, 0.55)"
  inner: "inset 0 1px 0 rgba(244, 244, 232, 0.04)"

motion:
  duration-instant: "0ms"
  duration-ultra-fast: "50ms"
  duration-faster: "100ms"
  duration-fast: "150ms"
  duration-normal: "200ms"
  duration-gentle: "350ms"
  duration-slow: "500ms"
  duration-slower: "700ms"
  duration-ultra-slow: "1000ms"
  ease-linear: "linear"
  ease-in: "cubic-bezier(0.4, 0, 1, 1)"
  ease-out: "cubic-bezier(0, 0, 0.2, 1)"
  ease-in-out: "cubic-bezier(0.4, 0, 0.2, 1)"
  ease-easy-ease: "cubic-bezier(0.33, 0, 0.67, 1)"
  ease-accelerate-mid: "cubic-bezier(0.7, 0, 1, 0.5)"
  ease-decelerate-mid: "cubic-bezier(0.1, 0.9, 0.2, 1)"
  press: "none"
  hover-opacity: "1"
  cursor-blink-duration: "1000ms"
  ticker-scroll-duration: "30000ms"

elevation:
  flat: "none"
  raised: "none"          # AIOX is brutalist — no shadow on raised by default
  floating: "none"        # surface tier shift instead of float shadow
  overlay: "0 16px 40px rgba(0, 0, 0, 0.40)"
  modal: "0 24px 64px rgba(0, 0, 0, 0.55)"
  glow: "0 0 24px rgba(209, 255, 0, 0.25)"  # the only non-border elevation idiom

components:
  button-primary:
    backgroundColor: "#D1FF00"
    textColor: "#050505"
    borderColor: "#D1FF00"
    typography: "Geist Mono 12px/1.3 600 +0.10em UPPERCASE"
    rounded: "0px"
    padding: "12px 20px"
    height: "44px"
    shadow: "none"
  button-primary-hover:
    backgroundColor: "#D1FF00"
    textColor: "#050505"
    borderColor: "#D1FF00"
    shadow: "0 0 24px rgba(209, 255, 0, 0.25)"
  button-primary-disabled:
    backgroundColor: "#3D3D3D"
    textColor: "#686868"
    borderColor: "#3D3D3D"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "#F4F4E8"
    borderColor: "rgba(156, 156, 156, 0.45)"
    typography: "Geist Mono 12px/1.3 600 +0.10em UPPERCASE"
    rounded: "0px"
    padding: "11px 19px"
    height: "44px"
  button-secondary-hover:
    backgroundColor: "rgba(209, 255, 0, 0.10)"
    textColor: "#D1FF00"
    borderColor: "#D1FF00"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "#F4F4E8"
    borderColor: "transparent"
    typography: "Geist Mono 12px/1.3 600 +0.10em UPPERCASE"
    rounded: "0px"
    padding: "8px 16px"
  button-destructive:
    backgroundColor: "#ED4609"
    textColor: "#FFFFED"
    borderColor: "#ED4609"
    typography: "Geist Mono 12px/1.3 600 +0.10em UPPERCASE"
    rounded: "0px"
    padding: "12px 20px"
  cta-button:
    backgroundColor: "#D1FF00"
    textColor: "#050505"
    borderColor: "#D1FF00"
    typography: "Geist Mono 14px/1.3 700 +0.10em UPPERCASE"
    rounded: "0px"
    padding: "16px 24px"
    height: "52px"
    shadow: "0 0 24px rgba(209, 255, 0, 0.25)"
  site-cta:
    backgroundColor: "#D1FF00"
    textColor: "#050505"
    borderColor: "#D1FF00"
    typography: "Geist Mono 14px/1.3 700 +0.10em UPPERCASE"
    rounded: "0px"
    padding: "20px 32px"
    height: "60px"
    shadow: "0 0 24px rgba(209, 255, 0, 0.25)"
  card:
    backgroundColor: "#0F0F11"
    textColor: "#F4F4E8"
    borderColor: "rgba(156, 156, 156, 0.15)"
    rounded: "0px"
    padding: "24px"
    shadow: "none"
  card-hover:
    backgroundColor: "#151518"
    textColor: "#F4F4E8"
    borderColor: "rgba(156, 156, 156, 0.24)"
    rounded: "0px"
    shadow: "none"
  input-text:
    backgroundColor: "#0F0F11"
    textColor: "#F4F4E8"
    borderColor: "rgba(156, 156, 156, 0.15)"
    typography: "Geist 16px/1.65 400"
    rounded: "0px"
    padding: "12px 14px"
  input-text-focus:
    backgroundColor: "#0F0F11"
    textColor: "#F4F4E8"
    borderColor: "#D1FF00"
    shadow: "0 0 0 3px rgba(209, 255, 0, 0.25)"
  input-text-invalid:
    backgroundColor: "#0F0F11"
    textColor: "#ED4609"
    borderColor: "#ED4609"
  badge-default:
    backgroundColor: "#111113"
    textColor: "#F4F4E8"
    borderColor: "rgba(156, 156, 156, 0.15)"
    typography: "Geist Mono 10px/1.0 500 +0.12em UPPERCASE"
    rounded: "0px"
    padding: "4px 8px"
  badge-lime:
    backgroundColor: "#D1FF00"
    textColor: "#050505"
    borderColor: "#D1FF00"
    typography: "Geist Mono 10px/1.0 500 +0.12em UPPERCASE"
    rounded: "0px"
    padding: "4px 8px"
  nav-header:
    backgroundColor: "rgba(5, 5, 5, 0.85)"
    textColor: "#F4F4E8"
    borderColor: "rgba(156, 156, 156, 0.15)"
    typography: "Geist Mono 12px/1.3 500 +0.10em UPPERCASE"
    height: "72px"
    backdropFilter: "blur(10px)"
  inverse-section:
    backgroundColor: "#F4F4E8"
    textColor: "#1D1F19"
    rounded: "0px"
    padding: "96px 64px"
  brutalist-hero:
    backgroundColor: "#050505"
    textColor: "#F4F4E8"
    typography: "TASA Orbiter Display 104px/1.0 800 -0.05em UPPERCASE"
    rounded: "0px"
    padding: "128px 64px 96px"
  hud-eyebrow:
    backgroundColor: "transparent"
    textColor: "#D1FF00"
    typography: "Geist Mono 10px/1.2 600 +0.20em UPPERCASE"
    rounded: "0px"
    padding: "0px"
  ontology-explorer:
    backgroundColor: "#12130F"      # surface-console
    textColor: "#F4F4E8"
    borderColor: "rgba(156, 156, 156, 0.15)"
    typography: "Geist Mono 14px/1.5 400"
    rounded: "0px"
    padding: "16px"
  animated-tab-nav:
    backgroundColor: "#111113"
    textColor: "#F4F4E8"
    borderColor: "rgba(156, 156, 156, 0.15)"
    typography: "Geist Mono 12px/1.3 600 +0.15em UPPERCASE"
    rounded: "0px"
    padding: "8px"
    backdropFilter: "blur(10px)"

preview_tokens:
  button_primary_bg: "#D1FF00"
  button_primary_text: "#050505"
  button_primary_border: "#D1FF00"
  button_secondary_bg: "transparent"
  button_secondary_text: "#F4F4E8"
  button_secondary_border: "rgba(156, 156, 156, 0.45)"
  button_tertiary_text: "#F4F4E8"
  surface_bg: "#050505"
  card_bg: "#0F0F11"
  text: "#F4F4E8"
  text_muted: "#9C9C9C"
  border: "rgba(156, 156, 156, 0.15)"
  accent: "#D1FF00"
  button_radius: "0px"
  card_radius: "0px"
  input_radius: "0px"

brand_primitives:
  # Typographic case — UPPERCASE on display, labels, eyebrow; sentence elsewhere
  case-eyebrow: "uppercase"
  case-btn: "uppercase"
  case-marquee: "uppercase"
  case-nav-brand: "uppercase"
  case-section-heading: "uppercase"
  case-display: "uppercase"
  # Motion — no press scale, no decorative motion, calm transitions
  motion-press: "none"
  motion-hover-opacity: "1"
  # Button geometry — flat with optional lime glow on hover
  btn-height: "44px"
  btn-padx: "20px"
  btn-pady: "12px"
  btn-shadow: "none"
  btn-shadow-hover: "0 0 24px rgba(209, 255, 0, 0.25)"
  btn-active-bg: "#D1FF00"
  btn-border-width: "1px"
  btn-secondary-border-width: "1px"
  nav-cta-height: "44px"
  nav-cta-padx: "20px"
  # Card geometry — flat surface tier shift on hover
  card-pad: "24px"
  card-pad-sm: "16px"
  card-shadow: "none"
  card-shadow-hover: "none"
  card-hover-bg: "#151518"
  # Hairline — alpha-based, the primary separator mechanism
  hairline-width: "1px"
  hairline-style: "solid"
  hairline-color: "rgba(156, 156, 156, 0.15)"
  hairline-color-strong: "rgba(156, 156, 156, 0.45)"
  hairline-card: "1"
  hairline-input: "1px"
  hairline-table: "1px"
  # Layout — architectural grid, quartered viewport
  nav-height: "72px"
  nav-padx: "32px"
  section-padx: "64px"
  section-pady: "96px"
  surface-pad: "96px"
  surface-min-h: "480px"
  container-max: "1400px"
  reading-column: "640px"
  inline-media: "880px"
  spacing: "0.25rem"
  # HUD signature — bracket prefix + mono eyebrow
  hud-bracket-color: "#D1FF00"
  hud-eyebrow-tracking: "0.20em"
  hud-bracket-tracking: "0.12em"
  # Glassmorphism — reserved for sticky nav and rectangular tab nav only
  glass-blur: "10px"
  glass-blur-soft: "5px"
  # Modal overlay dim
  modal-overlay: "rgba(61, 61, 61, 0.5)"

aliases:
  "--block-1": "--surface-bright"
  "--block-2": "--surface-container-low"
  "--block-3": "--surface-container"
  "--block-4": "--surface-container-high"
  "--block-5": "--surface-container-highest"
  "--block-6": "--surface-dim"
  "--block-7": "--surface-inverse"
  "--block-7-foreground": "--surface-inverse-foreground"
  "--text-h1": "--text-heading"
  "--text-h2": "--text-title"
  "--text-h3": "--text-subtitle"
  "--text-card-title": "--text-title"
  "--text-lead": "--text-body-lg"
  "--text-nav": "--text-label"
  "--text-btn": "--text-label"
  "--text-btn-sm": "--text-caption"
  "--text-eyebrow": "--text-eyebrow"
  "--text-meta": "--text-caption"
  "--font-weight-display": "800"
  "--font-weight-heading": "800"
  "--font-weight-body": "400"
  "--font-weight-lead": "400"
  "--font-weight-nav": "500"
  "--font-weight-brand": "800"
  "--font-weight-btn": "600"
  "--font-weight-emphasis": "600"
  "--font-weight-eyebrow": "600"
  "--tracking-display": "-0.05em"
  "--tracking-h1": "-0.03em"
  "--tracking-h2": "-0.03em"
  "--tracking-h3": "-0.02em"
  "--tracking-lead": "0em"
  "--tracking-body": "0em"
  "--tracking-btn": "0.10em"
  "--tracking-eyebrow": "0.20em"
  "--tracking-label": "0.15em"
  "--tracking-bracket": "0.12em"
  "--leading-display": "1.0"
  "--leading-heading": "1.05"
  "--leading-body": "1.65"
  "--leading-lead": "1.6"
  "--leading-tight": "1.2"
  "--shadow-1": "--elevation-flat"
  "--shadow-2": "--elevation-flat"
  "--shadow-3": "--elevation-glow"
  "--shadow-4": "--elevation-overlay"
  "--duration-base": "--duration-normal"
  "--radius-pill": "--radius-none"
  "--radius-hero": "--radius-none"

# Z-layer governance — canonical stack, never use arbitrary z-index
layers:
  base: 0
  elevated: 1
  sticky: 10
  nav: 100
  dropdown: 200
  overlay: 300
  modal: 400
  toast: 500

showcase:
  kicker: "[00] AI ORCHESTRATION SYSTEM"
  headline: "A IA é só a seta. O X é seu."
  lead: "AIOX é o sistema operacional para quem opera com IA — não para quem é operado por ela. Manifesto-grade. Anti-hype. Pro-operator. Construído por Alan Nicolás como o oposto explícito de 'IA que substitui você'."
  primary_cta: "Entrar no AIOX"
  secondary_cta: "Ler o manifesto"
  tertiary_cta: "Docs do operador →"
assets:
  logo:
    kind: "svg-inline"
    mime: "image/svg+xml"
    notes: "AIOX wordmark — TASA Orbiter Display lockup, brutalist-technical character"
  favicon:
    url: "https://brand.aioxsquad.ai/icon.svg?aiox"
    mime: "image/svg+xml"
    notes: "AIOX X-mark on flare (#ED4609) circle — shared brand domain"

fidelity_notes:
  shadows_detected: false
  fonts_proprietary:
    - "TASA Orbiter Display"
  icons_not_captured: false
  photography_not_captured: true
  alpha_lost: []
  intentional_gaps:
    - "Photographic imagery is intentionally absent — grid, dot, circuit, hazard patterns only"
    - "Elevation shadows are intentionally absent on cards — surface tier shift + hairline border carry depth"
    - "Pure white (#FFFFFF) is intentionally absent for foreground type — cream (#F4F4E8) carries the warmth"
    - "Pure red (#EF4444) is intentionally avoided as destructive — flare (#ED4609) replaces medical red"
    - "Emoji is intentionally absent — the brand is brutalist-technical and reserves all character for typography and HUD overlays"
---

## 1. Visual Theme & Atmosphere

AIOX reads as **dark cockpit with neon signature** — a brutalist-technical operating system, not a generic AI SaaS. The surface is closer to a terminal HUD than a marketing landing page: near-black canvas (`#050505`), warm cream type (`#F4F4E8` — paper-under-lamp, slightly analog), and a single electric accent (neon lime `#D1FF00`) reserved for focus rings, primary actions, and the AIOX logo accent.

The fundamental brand decision: **one accent, one canvas, one type color — everything else is structural**. Lime is the signature, never decorative. Borders carry separation, not shadows. Surface tiers carry depth, not elevation. The system wears its own wiring as ornament — bracket prefixes (`[00]`, `[AIOX]`, `[ESC]`), blinking cursors, mono-typed CSS variable refs surfaced as decoration, unicode structural dividers (`·`, `/`, `_`).

The brand line — *"A IA é só a seta. O X é seu."* — is the tone in one sentence: declarative, second-person, direct, technical. PT-BR by default; addresses the reader as `você`, never passive voice. Manifesto-grade rhetoric. Anti-hype. Pro-operator.

Dark mode is the *primary* product context. Most screens are dark. Light mode (`.brandbook-root` scoped variant or top-level `.light`) is reserved for docs/blog and light-tenant overlays. Both modes share the same lime signature and the same component library — only the semantic token bindings flip.

## 2. Color Palette & Roles

**Lime** `#D1FF00` — the signature. Neon lime from OKLCH `0.934 0.2264 121.95` — a single chroma point that cannot be substituted. Reserved for focus rings, primary CTAs, glow halos, the AIOX logo accent, and the *only* non-neutral fill in most compositions. Never used decoratively. Never tiled. Never gradient-filled. The lime carries depth through its **15-step pre-computed alpha scale** (2%, 3%, 4%, 5%, 6%, 8%, 10%, 12%, 15%, 20%, 25%, 40%, 50%, 75%, 90%) — the system never darkens or lightens the base hex.

**Cream** `#F4F4E8` (rgb 244/244/232) — warm cream on dark, the canonical paper color. Default foreground type on near-black. Slightly off-white on purpose: the warmth prevents clinical reading. **Warm-white** `#FFFFED` is the brand lockup ceiling. **Cream-alt** `#F5F4E7` and **cream-ui** `#F5F5ED` are the lighter UI cream variants.

**Ink** `#1D1F19` — near-black body type on light surfaces. OKLCH `0.235 0.0116 122.3` — a greenish-warm ink, not pure black, that pairs with cream without reading clinical.

**Surface tier ladder (dark cockpit):** `void` `#000000` (overlay anchor only) → `surface-deep` `#0A0A0C` (sunk surface) → `dark` `#050505` (canvas) → `surface-panel` `#111113` (default panel) → `surface-dark` `#0F0F11` (elevated card) → `surface-hover` `#151518` (hover) → `surface-overlay` `#1A1A1C` (popover/dialog) → `surface-console` `#12130F` (terminal panel, faint lime tint, OKLCH h=118) → `surface-alt` `#1C1E19` (alt panel, lime-tinted) → `surface-hover-strong` `#181635` (pressed — violet-lime mix, brandbook signature). Components gain weight by surface shift, never by shadow.

**Foreground ramp on dark:** `cream` `#F4F4E8` (default) → `fg-meta` `#9C9C9C` (metadata) → `fg-muted` `#BCBCBC` (muted) → `fg-muted-legacy` `#686868`.

**Borders are alpha-based, not solid:** `--border` is `rgba(156, 156, 156, 0.15)` (1px hairline). `--border-strong` brightens to `0.45` for emphasis. `--border-subtle` softens to `0.10`. Hairline borders are *the* primary separator mechanism — adapt naturally to every surface tier.

**Secondary accents — sparing.** **Blue** `#0099FF` for informational and data viz; never mixed with lime on the same surface element. **Flare** `#ED4609` — warm orange-red. Destructive states and critical alerts. Replaces "medical red" — the brand posture is too technical for pure red, flare carries more editorial weight.

**Semantic feedback (two tiers).** Tier 1 button-ready: `success` `#22C55E`, `warning` `#F59E0B`, `error` `#EF4444`. Tier 2 status-ready (lighter, badge/dot scale): `status-success` `#4ADE80`, `status-warning` `#FBBF24`, `status-error` `#F87171`, `status-info` `#60A5FA`.

**Gold alt-theme.** A single parallel theme exists: `gold` `#DDD1BB` replaces lime in alternate-tenant contexts (`gold-dark` `#A89768`, `gold-wash` `#F1E9D6`). Never render lime and gold on the same surface — they are alternate themes, not siblings.

## 3. Typography Rules

**Three faces, strict roles, no exceptions.**

**TASA Orbiter Display** (`--font-bb-display`) — self-hosted OTF, variable weight 700–900. Used ALL CAPS with `-0.05em` tracking for hero, section titles, and the word *AIOX* itself. A single display moment per page. Never mixed with display variants within the same section. Without the OTF, display falls back to Geist Bold and loses identity (do not block shipment, but document the substitution).

**Geist 300–900** (`--font-bb-sans`) — body, UI, labels, forms. Reads as precise and slightly technical. Pairs cleanly with the display face without competing. Weight hierarchy: 400 body, 500 meta/nav, 600 h5/labels, 800 bold emphasis. Variable font.

**Geist Mono 400–500** (`--font-bb-mono`) — HUD overlays, nav tickers, bracket annotations, timestamps, code, CSS variable refs surfaced as decoration. Roboto Mono is the OSS fallback. Mono is the *primary* structural label face, not a code-block afterthought.

**Scale.** Hero fluid clamp `clamp(3rem, 8vw, 6.5rem)` maxing at 104px. Display-1 fixed at 64px. Display-2 clamp `clamp(2rem, 4vw, 2.5rem)` maxing at 40px. Line-height 1–1.05, tight negative tracking `-0.05em` to `-0.03em`. Headings: h1 40px · h2 32px · h3 24px · h4 20px (TASA Orbiter 800). h5 shifts to Geist 600 at 18px — the register changes from editorial display to UI heading. Body: `body-lg` 18px/1.6 (marketing prose); `body` 16px/1.65 (default); `body-sm` 14px/1.5 (dense UI). Meta/HUD (Geist Mono): `caption` 12px/1.4 Geist sans; `label` 12px/1.3 mono +0.15em; `eyebrow` 10px/1.2 mono +0.20em; `bracket` 10px/1 mono +0.12em; `micro` 9px/1.2 mono +0.14em; `mono` 14px/1.5 mono (code blocks).

**Case discipline.** Display ALL CAPS with -0.05em tracking. Headings UPPERCASE. Body sentence case. Nav/labels UPPERCASE mono. Inline emphasis in `[BRACKETS]`. Never mix cases on the same surface without intent. Eyebrows always pair with bracket prefixes in the HUD register: `[00] MANIFESTO // CORE BELIEF`, `[AIOX] — SINGLE SOURCE OF TRUTH`, `[ULT] LATEST OPERATION`.

Never use more than two type weights on a single screen. Never stack two display-sized headings on the same vertical axis.

## 4. Components

**Buttons.** The primary button is **lime fill on dark canvas** (`#D1FF00` background, `#050505` text), 0px radius, 44px height. No shadow by default. On hover, gains a lime glow halo: `0 0 24px rgba(209, 255, 0, 0.25)` — the *only* non-border elevation idiom. Secondary: transparent background, cream text, hairline border (`rgba(156, 156, 156, 0.45)`). On hover, fills with `--lime-10` and shifts text to lime. Ghost: text only, no border, zero radius. Destructive uses flare (`#ED4609`) — never red. Site CTA is hero-scale: 60px height, 0px radius, generous mono label.

**Cards.** Dark surface (`#0F0F11`), 0px radius, 24px padding, 1px hairline border (`rgba(156, 156, 156, 0.15)`). **No shadow.** On hover, background shifts to `#151518` (surface-hover) and border brightens to `rgba(156, 156, 156, 0.24)`. The flat-with-tier-shift pattern is the brand's signature interaction — depth through surface, not shadow.

**Inputs.** Surface-dark background, 0px radius, 1px alpha hairline border. Lime focus ring at 50% alpha + 3px offset. Invalid state swaps text and border to flare (never red). Disabled at 0.5 opacity.

**Navigation.** 72px height, near-black background with `backdrop-filter: blur(10px)` (`--glass-blur`), hairline bottom border. Nav links in Geist Mono 500 +0.10em UPPERCASE at 12px. CTA button uses the same lime primary pattern at 44px height and 0px radius. Navigation states use hard rectangular slabs, never pills.

**HUD components — the brand's content idioms.** `mono-label`: lime text in Geist Mono 12px +0.15em UPPERCASE. `section-label` (eyebrow with bracket prefix): `[00] MANIFESTO` rendered in lime Geist Mono 10px +0.20em UPPERCASE. `bracket` annotation: 10px +0.12em UPPERCASE inline marker. These are *content components*, not utility styles — they carry the HUD register.

**Surfaces & cards.** `article-card`, `author-card`, `job-listing-card`, `team-card`, `office-card`, `device-mockup-frame`. All flat, 1px hairline border, no shadow. Border brightens on hover. Block-accent variants use a 3px left border in semantic color (lime/blue/flare).

**Data & feedback.** Badges use bracket typography (Geist Mono 10px +0.12em UPPERCASE). Alerts use flat strip with left 3px border (no full-bleed fill). Progress: lime fill on surface-panel track. Skeleton: surface-hover background with subtle pulse. Charts: surface-dark background, lime/blue/flare data series.

**Product-specific.** `ontology-explorer` (node-graph UI on `surface-console` `#12130F`), `org-chart-node` (team hierarchy), `pricing-benefit` and `post-benefit` (feature row).

## 5. Layout Principles

**Architectural grid. Editorial spreads. Quartered viewports.**

Max content width **1400px**, with a `--bb-gutter` formula — `max(1.5rem, calc((100% - 1400px) / 2 + 1.5rem))` — that provides automatic edge padding. **Reading column** caps at 640px. **Inline media** at 880px.

**Grid systems:** 4-column for hero/editorial/manifesto spreads; 12-column fluid for dashboards; 8-column for condensed operational UI. **Quartered viewport** — the signature AIOX background technique. Four vertical border lines divide the viewport into quarters as structural decoration. Never interrupted by content; content sits *above* the grid. **Oversized word** — the brand word *AIOX* set at 20% opacity sits behind hero content at display-1 scale. Reserved for landing and manifesto sections.

**Spacing scale** — 4/8px rhythm: 0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 80, 96, 128. Most component-internal spacing uses 16px (`--sp-4`) and 24px (`--sp-6`); section gutters use 48–96px; page-level gaps use 96–128px.

**Z-layers — canonical stack, never use arbitrary z-index.** `base: 0` → `elevated: 1` → `sticky: 10` → `nav: 100` → `dropdown: 200` → `overlay: 300` → `modal: 400` → `toast: 500`. Sticky nav at top. Ticker strip may run *above* the nav as a secondary channel (mono, scrolling, low-contrast metadata).

## 6. Depth & Elevation

**No elevation shadows by default.** This is a brutalist system. Depth is conveyed through:

1. **Surface tiers** — canvas → surface-panel → surface-dark → surface-alt → surface-hover → surface-overlay. A component gains weight by surface shift, never by shadow.
2. **1px hairline borders** — `rgba(156, 156, 156, 0.15)` hairline; brightens to `0.24` on hover. Strong border `0.45` available for emphasis.
3. **Lime glow** — the *only* non-border elevation idiom. `--lime-glow` (`rgba(209, 255, 0, 0.25)`) used as focus ring halo and on primary CTAs on hover. No multi-stop shadow stacks.
4. **Glassmorphism is rare.** `--glass-blur: 10px` exists but is reserved for sticky nav overlays and rectangular tab nav. Never used for cards or modals.
5. **Modal overlay dim** — `rgba(61, 61, 61, 0.5)`. Warm gray overlay, not pure black — keeps the warm palette consistent.
6. **Gradients are rare.** One canonical gradient exists: `--gradient-dark-deep` (dark → surface → elevated → surface → dark at 135deg). Reserved for pitch deck slides and hero backgrounds. Never animated.

The brand shadow vocabulary, used sparingly: `elevation.overlay` (16px 40px — popovers/dropdowns over dark surfaces), `elevation.modal` (24px 64px — dialogs), `elevation.glow` (lime halo — interactive focus). Card shadows are `none`.

## 7. Do's and Don'ts

**Do:**

- Reserve lime (#D1FF00) for exactly one action per screen — primary CTA, focus ring, or lockup accent
- Use warm cream (#F4F4E8) for body text on dark — never pure white (#FFFFFF)
- Use ink (#1D1F19) for body text on light — never pure black (#000000)
- Stack short manifesto-grade sentences as rhetoric; use em-dashes and single-line paragraphs
- Prefer hairline borders (`rgba(156, 156, 156, 0.15)`) over shadows for separation
- Use mono + bracket prefixes (`[00]`, `[AIOX]`) as structural eyebrow labels
- Cap max content width at 1400px; use 4-column grid for hero / 12-column for dashboard
- Use unicode glyphs (`·`, `/`, `_`) as structural dividers
- Address the reader in second person (PT-BR `você`), never passive voice
- Use the 15-step lime alpha scale to adjust depth — never darken or lighten the base hex
- Ship the TASA Orbiter OTF with the CSS; without it, display falls back to Geist Bold and loses the brand
- Use the canonical z-layer stack (base 0 → toast 500); arbitrary z-index is forbidden

**Don't:**

- Use emoji — anywhere, ever. This brand is brutalist-technical
- Use photographic imagery as background — grid, dot, circuit, hazard patterns only
- Gradient-fill the lime — signature means solid
- Use more than one display moment per page
- Stack lime and gold on the same surface — they are alternate themes, not siblings
- Soften hero or headline containers past 0 radius
- Use elevation shadows on cards — use surface tier shift + hairline border
- Use red (#EF4444) as destructive in product UI — use flare (#ED4609); red reads medical
- Use pure white (#FFFFFF) for foreground type; use cream (#F4F4E8) or warm-white (#FFFFED) for brand lockups
- Break the HUD register — once you introduce bracket eyebrows, commit to them throughout the surface
- Darken/lighten the lime hex — adjust via alpha scale only
- Stack two display-sized headings on the same vertical axis

## 8. Responsive Behavior

Fluid section spacing: collapses from 128px → 96px → 64px → 40px as viewport shrinks. Container max 1400px with `--bb-gutter` margin formula. On mobile, single column with `clamp(1rem, 3vw, 2rem)` side padding. Type scale holds — do not reduce body size below 14px. Hero scales fluidly via `clamp(3rem, 8vw, 6.5rem)` — the brutalist negative tracking holds at every breakpoint. Nav collapses to hamburger; CTA button stays visible. The quartered grid borders adapt to 2-column at <768px and disappear at <480px (replaced by horizontal hairlines). Bracket prefixes shrink to 9px micro at small breakpoints but never disappear — the HUD register is always present.

## 9. Accessibility & Interaction

Use **WCAG AA** contrast as a release gate. Cream `#F4F4E8` on near-black `#050505` and ink `#1D1F19` on cream-alt `#F5F4E7` are the default accessible pairs. Lime `#D1FF00` is reserved as accent and focus color; avoid using lime as the *only* carrier of meaning (always pair with text label or icon).

All interactive elements must be keyboard reachable, visibly focused (lime ring with 3px offset), and at least 44px tall when used as primary tap targets. Focus rings use `rgba(209, 255, 0, 0.50)` with offset to remain visible on dark, light, and lime surfaces.

Respect reduced-motion preferences. Do not use `scale()` press effects, parallax, autoplay motion, decorative gradients, or motion that changes layout. Preferred transitions are color, border, background, opacity, and lime-glow halo around 150–200ms with `cubic-bezier(0.33, 0, 0.67, 1)` (easy-ease).

Cursor blink animations and ticker strips are decorative HUD signatures — they MUST be paused under `prefers-reduced-motion: reduce`.

## 10. Agent Prompt Guide

### Quick Color Reference

- **Primary CTA:** Lime `#D1FF00` on near-black `#050505` (44–60px height, 0px radius)
- **Brand accent:** Lime `#D1FF00` (focus rings, glow halos, logo accent — never decorative)
- **Page background (dark):** `#050505` near-black canvas
- **Page background (light):** `#F5F4E7` warm cream-alt
- **Card background (dark):** `#0F0F11` surface-dark (0px radius, 1px hairline)
- **Border:** `rgba(156, 156, 156, 0.15)` — alpha hairline, not solid
- **Body text on dark:** Cream `#F4F4E8` — never pure white
- **Body text on light:** Ink `#1D1F19` — never pure black
- **Muted text:** `#9C9C9C` (fg-meta) for HUD labels and metadata
- **Destructive:** Flare `#ED4609` (warm orange-red — replaces medical red)
- **Focus ring:** `rgba(209, 255, 0, 0.50)` lime at 50% alpha

### Example Component Prompts

```
Build an AIOX-style hero: near-black #050505 background, TASA Orbiter Display 104px
800 weight ALL CAPS with -0.05em tracking, Geist body at 18px/1.6 cream #F4F4E8,
lime #D1FF00 primary CTA at 44px height with 0px radius, ghost secondary button
with rgba(156,156,156,0.45) hairline border. Bracket eyebrow [00] AI ORCHESTRATION
SYSTEM in lime Geist Mono 10px +0.20em UPPERCASE above the hero.
```

```
Build an AIOX research card: surface-dark #0F0F11 background, 0px border-radius,
1px hairline border rgba(156,156,156,0.15), no shadow. On hover: background shifts
to #151518 (surface-hover) and border brightens to rgba(156,156,156,0.24). Card
title in TASA Orbiter Display 24px 800. Body in Geist 16px/1.65 cream. Bracket
eyebrow [ULT] LATEST OPERATION in lime mono +0.20em above title.
```

```
Build an AIOX navigation bar: 72px height, near-black background with backdrop-filter
blur(10px), hairline border-bottom. Brand AIOX logo on left in cream/lime variant.
Nav links in Geist Mono 500 +0.10em UPPERCASE at 12px. CTA button in lime #D1FF00
with #050505 text, 44px height, 0px radius. Sticky at top with z-index 100.
```

```
Build an AIOX dark editorial closing section: cream #F4F4E8 background, ink #1D1F19
text (the inverse — light section closes the dark page), lime CTA button #D1FF00,
no gradient, 96px vertical padding. The light section is the *contrast* moment —
all surrounding sections are dark. Bracket eyebrow remains lime even on cream.
```

```
Build an AIOX HUD overlay: bracket prefix [AIOX] in lime Geist Mono 10px +0.12em
UPPERCASE, mono label "// SINGLE SOURCE OF TRUTH" in cream Geist Mono +0.15em,
unicode dividers (· / _) between segments. Optional blinking cursor at line end.
This is the brand's signature decoration — wear the wiring as ornament, not cover.
```

### Iteration Guide

1. **Lime is the signature, not the body color.** If lime appears more than once per screen as a fill, reduce to one instance. Use the 15-step alpha scale for everything else.
2. **Body is Geist, headlines are TASA Orbiter.** Never reverse — TASA Orbiter at 16px reads heavy and brutalist (correct register only at 20px+); Geist at 64px reads thin and weak.
3. **Hairline borders, not solid.** `rgba(156, 156, 156, 0.15)` adapts to every surface tier. Never use solid `#3D3D3D` as the system border.
4. **Cards are surface-dark, not canvas.** `#0F0F11` background with 0px radius. Canvas (`#050505`) is the page, not the surface.
5. **Zero radius everywhere.** Buttons, inputs, cards, badges, nav states and hero containers all use 0px radius. Do not mix rounded UI into AIOX surfaces.
6. **Cards have no shadow.** Surface tier shift on hover (`#0F0F11` → `#151518`) carries the depth. Reserve shadow for popovers, modals, and the lime glow halo.
7. **Lime stays solid on every surface.** `#D1FF00` on `#050505`, on cream, on light — same hex. The alpha scale is the only legitimate variation.
8. **HUD register is binary.** Once you introduce a bracket eyebrow, the entire surface commits to the HUD vocabulary. No mixing with neutral marketing copy.
9. **PT-BR voice.** Address the reader as `você`. Manifesto-grade sentences. Em-dashes liberal. Never passive voice.
10. **Whitespace is architectural.** Section padding 96–128px, max width 1400px, reading column 640px. The grid is generous on purpose — brutalism is *not* density.

## 11. Implementation

Use this file as the portable source of truth for AIOX-style UI generation. It should work in any modern Next.js / React / Tailwind v4 / shadcn project without requiring repository-specific files.

**Stack origin:** Next.js 15 + React 19 + Tailwind CSS v4 + shadcn/ui + Radix Primitives + Lucide Icons + Framer Motion + Geist (Vercel) + TASA Orbiter Display (self-hosted OTF). Source of truth: `apps/aiox-brandbook/src/app/globals.css` (365 tokens) + `apps/aiox-brandbook/brandbook/styles/*.css`.

Recommended setup: publish the frontmatter tokens as CSS custom properties, map semantic slots to Tailwind/shadcn theme tokens, ship the TASA Orbiter OTF via `@font-face`, and keep component behavior aligned with the rules above.

**Key shadcn/Tailwind mappings:**

| DESIGN.MD token | Tailwind utility | Value |
|-----------------|-----------------|-------|
| `colors.primary` | `bg-primary` | `#D1FF00` (lime) |
| `colors.foreground` | `text-foreground` | `#F4F4E8` (cream on dark) |
| `colors.background` | `bg-background` | `#050505` (near-black, dark default) |
| `colors.card` | `bg-card` | `#0F0F11` (surface-dark) |
| `colors.border` | `border-border` | `rgba(156, 156, 156, 0.15)` |
| `colors.destructive` | `bg-destructive` | `#ED4609` (flare — NOT red) |
| `rounded.lg` | `rounded-none` | `0px` (cards) |
| `rounded.sm` | `rounded-none` | `0px` (buttons, inputs) |
| `rounded.none` | `rounded-none` | `0px` (hero, display) |
| `shadows.glow` | `shadow-[0_0_24px_rgba(209,255,0,0.25)]` | lime halo |

**Critical CSS snippet (dark mode default):**

```css
@font-face {
  font-family: "TASAOrbiterDisplay";
  src: url("/fonts/TASAOrbiterDisplay-Bold.otf") format("opentype");
  font-weight: 700 900;
  font-style: normal;
  font-display: swap;
}

:root {
  /* AIOX defaults to DARK */
  --background: #050505;
  --foreground: #F4F4E8;
  --primary: #D1FF00;
  --primary-foreground: #050505;
  --card: #0F0F11;
  --card-foreground: #F4F4E8;
  --border: rgba(156, 156, 156, 0.15);
  --ring: rgba(209, 255, 0, 0.50);
  --destructive: #ED4609;
  --radius: 0px;                        /* square by default */
  --radius-sm: 0px;                     /* button / input */
  --radius-none: 0px;                   /* hero / display */
  --lime-glow: rgba(209, 255, 0, 0.25);
  --font-display: 'TASAOrbiterDisplay', 'Geist', system-ui, sans-serif;
  --font-body: 'Geist', system-ui, sans-serif;
  --font-mono: 'Geist Mono', 'Roboto Mono', ui-monospace, monospace;
  --hairline: 1px solid var(--border);
  --bb-gutter: max(1.5rem, calc((100% - 1400px) / 2 + 1.5rem));
}

.light {
  /* Light overlay (docs / blog / light-tenant) */
  --background: #F5F4E7;
  --foreground: #1D1F19;
  --card: #FFFFFF;
  --card-foreground: #1D1F19;
  --border: rgba(156, 156, 156, 0.24);
}

/* Lime alpha scale — the depth mechanism */
:root {
  --lime-2: rgba(209, 255, 0, 0.02);
  --lime-10: rgba(209, 255, 0, 0.10);
  --lime-15: rgba(209, 255, 0, 0.15);
  --lime-25: rgba(209, 255, 0, 0.25);
  --lime-50: rgba(209, 255, 0, 0.50);
}

/* Z-layer governance */
:root {
  --layer-base: 0;
  --layer-elevated: 1;
  --layer-sticky: 10;
  --layer-nav: 100;
  --layer-dropdown: 200;
  --layer-overlay: 300;
  --layer-modal: 400;
  --layer-toast: 500;
}
```

**Component source root:** `apps/aiox-brandbook/src/components/`. **Regenerate command:** none required — tokens are hand-curated in `globals.css`. **Drift detection:** run `npx @google/design.md diff apps/aiox-brandbook/DESIGN.MD apps/design/src/data/designs/aiox/DESIGN.MD` to surface token-level divergence between business DS and gallery export.