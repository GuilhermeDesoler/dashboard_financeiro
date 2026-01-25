import streamlit as st


def apply_custom_styles():
    """Aplica estilos CSS customizados globalmente para o Streamlit."""
    st.markdown(
        """
        <style>
        /* Variáveis de cores globais */
        :root {
            --primary-color: #9333EA;
            --primary-hover: #7E22CE;
            --primary-active: #6B21A8;
        }

        /* Largura mínima para inputs */
        input[type="text"],
        input[type="number"],
        input[type="date"],
        input[type="time"],
        input[type="email"],
        input[type="password"],
        select,
        textarea,
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input,
        .stSelectbox > div > div > div,
        .stTextArea > div > div > textarea {
            min-width: 180px !important;
        }

        /* Largura mínima para botões */
        .stButton > button {
            min-width: 180px !important;
        }

        /* Customização de botões primários - incluindo formulários */
        .stButton > button[kind="primary"],
        button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"],
        button[data-testid="baseButton-primary"],
        .stForm button[kind="primary"],
        form button[kind="primary"],
        button[data-baseweb="button"][kind="primary"],
        .stFormSubmitButton > button,
        [data-testid="stFormSubmitButton"] > button {
            background-color: var(--primary-color) !important;
            border-color: var(--primary-color) !important;
            color: white !important;
        }

        /* Garantir texto branco em todos os elementos dentro do botão primary */
        .stButton > button[kind="primary"] *,
        button[kind="primary"] *,
        .stButton > button[data-testid="baseButton-primary"] *,
        button[data-testid="baseButton-primary"] *,
        .stForm button[kind="primary"] *,
        form button[kind="primary"] *,
        button[data-baseweb="button"][kind="primary"] *,
        .stFormSubmitButton > button *,
        [data-testid="stFormSubmitButton"] > button *,
        .stFormSubmitButton > button p,
        [data-testid="stFormSubmitButton"] > button p,
        .stFormSubmitButton > button div,
        [data-testid="stFormSubmitButton"] > button div {
            color: white !important;
        }

        .stButton > button[kind="primary"]:hover,
        button[kind="primary"]:hover,
        .stButton > button[data-testid="baseButton-primary"]:hover,
        button[data-testid="baseButton-primary"]:hover,
        .stForm button[kind="primary"]:hover,
        form button[kind="primary"]:hover,
        button[data-baseweb="button"][kind="primary"]:hover,
        .stFormSubmitButton > button:hover,
        [data-testid="stFormSubmitButton"] > button:hover {
            background-color: var(--primary-hover) !important;
            border-color: var(--primary-hover) !important;
            color: white !important;
        }

        .stButton > button[kind="primary"]:active,
        button[kind="primary"]:active,
        .stButton > button[data-testid="baseButton-primary"]:active,
        button[data-testid="baseButton-primary"]:active,
        .stForm button[kind="primary"]:active,
        form button[kind="primary"]:active,
        button[data-baseweb="button"][kind="primary"]:active,
        .stFormSubmitButton > button:active,
        [data-testid="stFormSubmitButton"] > button:active {
            background-color: var(--primary-active) !important;
            border-color: var(--primary-active) !important;
            color: white !important;
        }

        /* Ocultar ícones de âncora nos headers */
        [data-testid='stHeaderActionElements'] {
            display: none !important;
        }

        /* Estilos para linhas de tabela de despesas/boletos */
        .table-row {
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #e5e7eb;
        }

        .table-row:last-child {
            border-bottom: none;
        }

        .table-row .col-date {
            flex: 2;
            font-size: 14px;
            color: #374151;
        }

        .table-row .col-desc {
            flex: 4;
            font-size: 14px;
            color: #374151;
        }

        .table-row .col-value {
            flex: 2;
            font-size: 14px;
            font-weight: 500;
            color: #111827;
        }

        /* Reduzir espaçamento entre elementos do Streamlit dentro de expanders */
        [data-testid="stExpander"] [data-testid="stVerticalBlock"] > div {
            margin-bottom: -12px !important;
        }

        [data-testid="stExpander"] [data-testid="stHorizontalBlock"] {
            border-bottom: 1px solid #e5e7eb;
            padding: 6px 0 !important;
            margin-bottom: 0 !important;
        }

        [data-testid="stExpander"] [data-testid="stHorizontalBlock"]:last-child {
            border-bottom: none;
        }

        /* Reduzir padding dos textos nas linhas */
        [data-testid="stExpander"] [data-testid="stText"] {
            padding: 0 !important;
            margin: 0 !important;
        }

        [data-testid="stExpander"] [data-testid="stText"] p {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.4 !important;
        }

        /* Reduzir espaçamento do checkbox */
        [data-testid="stExpander"] [data-testid="stCheckbox"] {
            padding: 0 !important;
            margin: 0 !important;
        }

        [data-testid="stExpander"] [data-testid="stCheckbox"] > label {
            padding: 0 !important;
            min-height: auto !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
