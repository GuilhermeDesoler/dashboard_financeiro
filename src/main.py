import streamlit as st
from views import Dashboard, Database, Ticket, Modalities, Expenses, Investments, Balances
from views.Login import Login
from views.Admin import Admin
from config import Environment, EnvironmentError
from presentation.components.custom_styles import apply_custom_styles
from presentation.components.theme_toggle import render_theme_toggle
from presentation.components.impersonate_timer import render_impersonate_timer
from presentation.auth_persistence import restore_auth_if_exists, clear_auth_session
from dependencies import get_container

try:
    env = Environment()
except EnvironmentError as e:
    st.error(f"Erro de Configuração\n\n{str(e)}")
    st.stop()

st.set_page_config(
    page_title="Dashboard Financeiro",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💰",
)

apply_custom_styles()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

render_theme_toggle()

if "auth_restore_attempted" not in st.session_state:
    st.session_state.auth_restore_attempted = True
    restore_auth_if_exists()

if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "Login"

PUBLIC_PAGES = {
    "Login": Login,
}

# Páginas para Super Admin (quando está em modo impersonate)
SUPER_ADMIN_PAGES = {
    "Dashboard": Dashboard,
    "Despesas": Expenses,
    "Boletos": Ticket,
    "Saldos e Limites": Balances,
    "Lançamentos": Database,
    "Investimentos": Investments,
    "Modalidades": Modalities,
}

# Páginas para usuários normais
USER_PAGES = {
    "Lançamentos": Database,
    "Despesas": Expenses,
    "Boletos": Ticket,
    "Saldos e Limites": Balances,
    "Investimentos": Investments,
}

ADMIN_PAGES = {
    "Admin": Admin,
}

if not st.session_state.is_authenticated:
    if st.session_state.current_page != "Login":
        st.session_state.current_page = "Login"
    Login()
else:
    current_user = st.session_state.get("current_user")

    container = get_container()
    http_client = container.http_client

    if "impersonate_token" in st.session_state:
        http_client.set_auth_token(st.session_state.impersonate_token)
    elif "access_token" in st.session_state:
        http_client.set_auth_token(st.session_state.access_token)

    with st.sidebar:
        if current_user:
            st.markdown(f"### {current_user.name}")
            st.caption(f"{current_user.email}")

            if "impersonate_token" in st.session_state:
                render_impersonate_timer()

            if (
                current_user
                and current_user.is_super_admin
                and "impersonate_token" in st.session_state
            ):
                if st.button(
                    "Sair do Impersonate", use_container_width=True, type="primary"
                ):
                    del st.session_state.impersonate_token
                    del st.session_state.impersonating_company
                    if "impersonate_start_time" in st.session_state:
                        del st.session_state.impersonate_start_time

                    http_client.set_auth_token(st.session_state.access_token)

                    st.session_state.current_page = "Admin"

                    st.success(
                        "Modo impersonate desativado. Voltando ao painel admin..."
                    )
                    st.rerun()

            st.divider()

        if (
            current_user
            and current_user.is_super_admin
            and "impersonate_token" not in st.session_state
        ):
            st.markdown("#### Administração")
            for page_name in ADMIN_PAGES.keys():
                if st.button(
                    page_name, use_container_width=True, key=f"admin_{page_name}"
                ):
                    st.session_state.current_page = page_name
                    st.rerun()
            st.divider()

            st.info(
                "💡 **Para acessar dados operacionais:**\n\n"
                "Use o botão **Impersonate** em uma empresa para "
                "visualizar dashboards e lançamentos."
            )

        if current_user and (
            not current_user.is_super_admin or "impersonate_token" in st.session_state
        ):
            st.markdown("#### Sistema")
            # Definir quais páginas mostrar baseado no tipo de usuário
            if current_user.is_super_admin and "impersonate_token" in st.session_state:
                pages_to_show = SUPER_ADMIN_PAGES
            else:
                pages_to_show = USER_PAGES

            for page_name in pages_to_show.keys():
                if st.button(
                    page_name, use_container_width=True, key=f"page_{page_name}"
                ):
                    st.session_state.current_page = page_name
                    st.rerun()

        st.divider()

        if st.button("Sair", use_container_width=True, type="secondary"):
            clear_auth_session()

            http_client.set_auth_token(None)

            st.session_state.is_authenticated = False
            st.session_state.current_page = "Login"

            st.rerun()

    # Determinar quais páginas estão disponíveis
    all_pages = {**SUPER_ADMIN_PAGES, **USER_PAGES}

    if st.session_state.current_page in all_pages:
        if (
            current_user
            and current_user.is_super_admin
            and "impersonate_token" not in st.session_state
        ):
            st.error("**Acesso Negado**")
            st.warning(
                "Super admins não podem acessar páginas operacionais diretamente.\n\n"
                "**Para visualizar dados de uma empresa:**\n\n"
                "1. Vá para a página **Admin**\n"
                "2. Clique em **Impersonate** na empresa desejada\n"
                "3. Você terá acesso aos dashboards e lançamentos dessa empresa por 1 hora"
            )
            st.info(
                "**Por quê?**\n\n"
                "Super admins gerenciam empresas e usuários. Para ver dados operacionais, "
                "você precisa escolher qual empresa deseja visualizar através do impersonate. "
                "Isso garante clareza sobre qual empresa você está acessando."
            )
            if st.button("Ir para Página Admin", type="primary"):
                st.session_state.current_page = "Admin"
                st.rerun()
        else:
            all_pages[st.session_state.current_page].render()
    elif st.session_state.current_page in ADMIN_PAGES:
        ADMIN_PAGES[st.session_state.current_page]()
    else:
        if (
            current_user
            and current_user.is_super_admin
            and "impersonate_token" not in st.session_state
        ):
            st.session_state.current_page = "Admin"
        else:
            st.session_state.current_page = "Dashboard"
        st.rerun()
