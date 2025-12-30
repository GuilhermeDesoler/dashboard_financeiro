import streamlit as st
from views import Home, Dashboard, Database, Ticket, Modalities, Login, Register
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

# Initialize session state
if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if "auth_token" not in st.session_state:
    st.session_state.auth_token = None

if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None

if "user" not in st.session_state:
    st.session_state.user = None

# Public pages (no auth required)
PUBLIC_PAGES = {
    "Login": Login,
    "Register": Register,
}

# Protected pages (auth required)
PROTECTED_PAGES = {
    "Home": Home,
    "Dashboard": Dashboard,
    "Lançamentos": Database,
    "Modalidades": Modalities,
    "Boletos": Ticket,
}

# Check if user is authenticated
if not st.session_state.is_authenticated:
    # Show login/register pages
    render_theme_toggle()

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Login"

    # Only allow public pages when not authenticated
    if st.session_state.current_page not in PUBLIC_PAGES:
        st.session_state.current_page = "Login"

    PUBLIC_PAGES[st.session_state.current_page].render()

else:
    # User is authenticated - show protected pages
    render_theme_toggle()

    with st.sidebar:
        # Show user info
        if st.session_state.user:
            st.markdown(f"**{st.session_state.user.get('name', 'Usuário')}**")
            st.caption(st.session_state.user.get("email", ""))
            st.divider()

        # Navigation
        for page_name in PROTECTED_PAGES.keys():
            if st.button(page_name, use_container_width=True):
                st.session_state.current_page = page_name

        st.divider()

        # Logout button
        if st.button("Sair", use_container_width=True, type="secondary"):
            # Clear session state
            st.session_state.is_authenticated = False
            st.session_state.auth_token = None
            st.session_state.refresh_token = None
            st.session_state.user = None
            st.session_state.current_page = "Login"
            st.rerun()

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    # Only allow protected pages when authenticated
    if st.session_state.current_page not in PROTECTED_PAGES:
        st.session_state.current_page = "Home"

    PROTECTED_PAGES[st.session_state.current_page].render()
