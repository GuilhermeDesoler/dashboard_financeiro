#!/bin/bash

# Script de setup para o Render.com

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"seu-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = \$PORT\n\
\n\
[theme]\n\
primaryColor = \"#00C853\"\n\
backgroundColor = \"#0E1117\"\n\
secondaryBackgroundColor = \"#1E2329\"\n\
textColor = \"#FAFAFA\"\n\
font = \"sans serif\"\n\
" > ~/.streamlit/config.toml
