import streamlit as st


def render_theme_toggle():
    """Aplica o tema selecionado via CSS."""
    # Aplicar o tema correspondente via CSS
    theme = st.session_state.get("theme", "light")
    apply_theme(theme)


def apply_theme(theme):
    """Aplica o tema selecionado via CSS customizado."""
    if theme == "dark":
        st.markdown(
            """
            <style>
            /* Dark Mode - Azul Marinho */
            [data-testid="stAppViewContainer"] {
                background-color: #0F172A !important;
            }
            [data-testid="stSidebar"] {
                background-color: #1E293B !important;
            }
            [data-testid="stHeader"] {
                background-color: #0F172A !important;
            }
            .stApp {
                background-color: #0F172A !important;
            }
            h1, h2, h3, h4, h5, h6, p, span, div, label {
                color: #F1F5F9 !important;
            }
            .stButton>button {
                border-color: #3B82F6 !important;
            }
            .stButton>button[kind="primary"] {
                background-color: #3B82F6 !important;
                color: white !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            /* Light Mode - Roxo */
            [data-testid="stAppViewContainer"] {
                background-color: #FAFAFA !important;
            }
            [data-testid="stSidebar"] {
                background-color: #FFFFFF !important;
            }
            [data-testid="stHeader"] {
                background-color: #FAFAFA !important;
            }
            .stApp {
                background-color: #FAFAFA !important;
            }
            h1, h2, h3, h4, h5, h6, p, span, div, label {
                color: #1F2937 !important;
            }
            .stButton>button[kind="primary"] {
                background-color: #9333EA !important;
                color: white !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
