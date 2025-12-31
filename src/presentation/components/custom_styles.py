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

        /* Customização de botões primários */
        .stButton > button[kind="primary"],
        button[kind="primary"] {
            background-color: var(--primary-color) !important;
            border-color: var(--primary-color) !important;
            color: white !important;
        }

        .stButton > button[kind="primary"]:hover,
        button[kind="primary"]:hover {
            background-color: var(--primary-hover) !important;
            border-color: var(--primary-hover) !important;
        }

        .stButton > button[kind="primary"]:active,
        button[kind="primary"]:active {
            background-color: var(--primary-active) !important;
            border-color: var(--primary-active) !important;
        }

        /* Ocultar ícones de âncora nos headers */
        [data-testid='stHeaderActionElements'] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
