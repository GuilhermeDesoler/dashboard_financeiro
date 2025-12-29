import streamlit as st
from views import Home, Dashboard, Database, Ticket, Modalities
from config import Environment, EnvironmentError
from presentation.components.custom_styles import apply_custom_styles
from presentation.components.theme_toggle import render_theme_toggle

try:
    env = Environment()
except EnvironmentError as e:
    st.error(f"Erro de Configuração\n\n{str(e)}")
    st.stop()

st.set_page_config(
    page_title="Financeiro",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_styles()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

render_theme_toggle()

PAGES = {
    "Home": Home,
    "Dashboard": Dashboard,
    "Lançamentos": Database,
    "Modalidades": Modalities,
    "Boletos": Ticket,
}

with st.sidebar:
    st.title("Guilherme")
    st.divider()

    for page_name in PAGES.keys():
        if st.button(page_name, use_container_width=True):
            st.session_state.current_page = page_name

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

PAGES[st.session_state.current_page].render()
