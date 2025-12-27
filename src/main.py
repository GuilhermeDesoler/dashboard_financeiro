import streamlit as st
from views import Home, Dashboard, Database, Ticket
from config import Environment, EnvironmentError

# Valida variáveis de ambiente na inicialização
try:
    env = Environment()
except EnvironmentError as e:
    st.error(f"🚨 Erro de Configuração\n\n{str(e)}")
    st.stop()

st.set_page_config(
    page_title="Financeiro",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📈",
)

PAGES = {
    "Home": Home,
    "Dashboard": Dashboard,
    "Database": Database,
    "Boletos": Ticket,
}

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

st.sidebar.title("Navegação")
for page in PAGES.keys():
    selected = page == st.session_state.current_page

    if st.sidebar.button(
        page,
        key=page,
        use_container_width=True,
        type="primary" if selected else "secondary",
    ):
        st.session_state.current_page = page
        st.rerun()

PAGES[st.session_state.current_page].render()
