# Temas Disponíveis para o Dashboard

Copie e cole o tema desejado no arquivo `.streamlit/config.toml` e reinicie o Streamlit.

---

## 🌙 Tema Atual - Dark Green (Padrão)
**Tema escuro com destaque verde - Perfeito para dashboards financeiros**

```toml
[theme]
primaryColor = "#00C853"              # Verde vibrante
backgroundColor = "#0E1117"           # Fundo escuro
secondaryBackgroundColor = "#1E2329"  # Cards cinza escuro
textColor = "#FAFAFA"                 # Texto branco suave
font = "sans serif"
```

---

## 💰 Tema 1 - Financial Gold
**Elegante com toques dourados**

```toml
[theme]
primaryColor = "#FFB300"              # Dourado vibrante
backgroundColor = "#1A1A2E"           # Azul escuro profundo
secondaryBackgroundColor = "#16213E"  # Azul marinho
textColor = "#EAEAEA"                 # Branco suave
font = "sans serif"
```

---

## 🌊 Tema 2 - Ocean Blue
**Azul profissional e clean**

```toml
[theme]
primaryColor = "#00B4D8"              # Azul ciano
backgroundColor = "#03045E"           # Azul marinho escuro
secondaryBackgroundColor = "#023E8A"  # Azul médio
textColor = "#CAF0F8"                 # Azul claro
font = "sans serif"
```

---

## 🌲 Tema 3 - Forest Green
**Verde natural e relaxante**

```toml
[theme]
primaryColor = "#52B788"              # Verde médio
backgroundColor = "#081C15"           # Verde escuro
secondaryBackgroundColor = "#1B4332"  # Verde floresta
textColor = "#D8F3DC"                 # Verde claro
font = "sans serif"
```

---

## 🔥 Tema 4 - Sunset Orange
**Laranja energético e moderno**

```toml
[theme]
primaryColor = "#FF6B35"              # Laranja vibrante
backgroundColor = "#2D2D2D"           # Cinza escuro
secondaryBackgroundColor = "#3D3D3D"  # Cinza médio
textColor = "#F7F7F7"                 # Branco
font = "sans serif"
```

---

## 🌸 Tema 5 - Purple Dream
**Roxo sofisticado**

```toml
[theme]
primaryColor = "#B565D8"              # Roxo vibrante
backgroundColor = "#1E1E2E"           # Roxo escuro
secondaryBackgroundColor = "#2A2A40"  # Roxo médio
textColor = "#E0E0E0"                 # Cinza claro
font = "sans serif"
```

---

## ☀️ Tema 6 - Light Mode (Claro)
**Tema claro para quem prefere fundo branco**

```toml
[theme]
primaryColor = "#00897B"              # Verde água
backgroundColor = "#FFFFFF"           # Branco
secondaryBackgroundColor = "#F5F5F5"  # Cinza muito claro
textColor = "#262730"                 # Preto suave
font = "sans serif"
```

---

## 🎨 Tema 7 - Neon Cyberpunk
**Futurístico com neon**

```toml
[theme]
primaryColor = "#00FF9F"              # Verde neon
backgroundColor = "#0A0E27"           # Azul escuro quase preto
secondaryBackgroundColor = "#1A1F3A"  # Azul escuro
textColor = "#E0E7FF"                 # Azul claro
font = "sans serif"
```

---

## 🏦 Tema 8 - Banking Blue
**Azul corporativo profissional**

```toml
[theme]
primaryColor = "#1976D2"              # Azul material
backgroundColor = "#FAFAFA"           # Branco suave
secondaryBackgroundColor = "#E3F2FD"  # Azul muito claro
textColor = "#212121"                 # Preto suave
font = "sans serif"
```

---

## 🌃 Tema 9 - Midnight Navy
**Azul marinho elegante**

```toml
[theme]
primaryColor = "#4FC3F7"              # Azul claro
backgroundColor = "#0D1B2A"           # Azul marinho muito escuro
secondaryBackgroundColor = "#1B263B"  # Azul marinho
textColor = "#E0E1DD"                 # Branco acinzentado
font = "sans serif"
```

---

## 🍃 Tema 10 - Mint Fresh
**Verde menta refrescante**

```toml
[theme]
primaryColor = "#26D07C"              # Verde menta
backgroundColor = "#F8F9FA"           # Branco gelo
secondaryBackgroundColor = "#E9ECEF"  # Cinza muito claro
textColor = "#212529"                 # Preto suave
font = "sans serif"
```

---

## 🎯 Como Aplicar um Tema

1. **Escolha um tema acima**
2. **Copie o código `[theme]`**
3. **Edite** `.streamlit/config.toml`
4. **Cole** substituindo a seção `[theme]` atual
5. **Salve** o arquivo
6. **Reinicie** o Streamlit (`Ctrl+C` e `streamlit run src/main.py`)

---

## 🎨 Personalizar Seu Próprio Tema

```toml
[theme]
primaryColor = "#HEXCOLOR"        # Cor dos botões primários, links, destaque
backgroundColor = "#HEXCOLOR"     # Cor do fundo principal
secondaryBackgroundColor = "#HEXCOLOR"  # Cor dos cards, sidebar, containers
textColor = "#HEXCOLOR"           # Cor do texto
font = "sans serif"               # Opções: "sans serif", "serif", "monospace"
```

### Ferramentas para escolher cores:
- [Coolors.co](https://coolors.co) - Gerador de paletas
- [ColorHunt.co](https://colorhunt.co) - Paletas prontas
- [Adobe Color](https://color.adobe.com) - Roda de cores

---

## 💡 Dicas de Combinação

- **Contraste**: Fundo escuro + texto claro (ou vice-versa)
- **Destaque**: Primary color deve se destacar do fundo
- **Harmonia**: Use ferramentas de paleta de cores
- **Acessibilidade**: Garanta bom contraste para leitura

---

## 🔄 Trocar Tema em Tempo Real

No canto superior direito do app Streamlit:
1. Clique no **menu ⋮**
2. Clique em **Settings**
3. Escolha **Theme** → Custom ou Light/Dark

Mas o arquivo `config.toml` define o tema padrão inicial.
