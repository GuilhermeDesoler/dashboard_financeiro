import streamlit as st


def apply_custom_styles():
    """Aplica estilos CSS customizados globalmente para o Streamlit."""
    st.markdown(
        """
        <style>
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
        </style>
        """,
        unsafe_allow_html=True
    )
