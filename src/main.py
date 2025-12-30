import streamlit as st
from views import Dashboard, Database, Ticket, Modalities
from views.Login import Login
from views.Admin import Admin
from config import Environment, EnvironmentError
from presentation.components.custom_styles import apply_custom_styles
from presentation.components.theme_toggle import render_theme_toggle
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
    page_icon="💰"
)

apply_custom_styles()

# Initialize theme
if "theme" not in st.session_state:
    st.session_state.theme = "light"

render_theme_toggle()

# Initialize authentication state
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "Login"

# Define pages
PUBLIC_PAGES = {
    "Login": Login,
}

AUTHENTICATED_PAGES = {
    "Dashboard": Dashboard,
    "Lançamentos": Database,
    "Modalidades": Modalities,
    "Boletos": Ticket,
}

ADMIN_PAGES = {
    "Admin": Admin,
}

# Authentication middleware
if not st.session_state.is_authenticated:
    # User is not authenticated - show login page
    if st.session_state.current_page != "Login":
        st.session_state.current_page = "Login"
    Login()
else:
    # User is authenticated - show sidebar and pages
    current_user = st.session_state.get("current_user")

    # Set HTTP client token if available
    container = get_container()
    http_client = container.http_client

    # Use impersonate token if active, otherwise use normal token
    if "impersonate_token" in st.session_state:
        http_client.set_auth_token(st.session_state.impersonate_token)
    elif "access_token" in st.session_state:
        http_client.set_auth_token(st.session_state.access_token)

    # Sidebar navigation
    with st.sidebar:
        # User info
        if current_user:
            st.markdown(f"### 👤 {current_user.name}")
            st.caption(f"📧 {current_user.email}")

            # Show impersonate warning in sidebar
            if "impersonate_token" in st.session_state:
                st.warning(f"🎭 Impersonando:\n**{st.session_state.get('impersonating_company')}**")

            st.divider()

        # Navigation buttons - Admin pages (if super admin and NOT impersonating)
        if current_user and current_user.is_super_admin and "impersonate_token" not in st.session_state:
            st.markdown("#### ⚙️ Administração")
            for page_name in ADMIN_PAGES.keys():
                if st.button(page_name, use_container_width=True, key=f"admin_{page_name}"):
                    st.session_state.current_page = page_name
                    st.rerun()
            st.divider()

            # Info box explaining impersonate requirement
            st.info(
                "💡 **Para acessar dados operacionais:**\n\n"
                "Use o botão **Impersonate** em uma empresa para "
                "visualizar dashboards e lançamentos."
            )

        # Navigation buttons - Regular pages (only if NOT super admin OR if impersonating)
        # Super admin can only see operational pages when impersonating
        if current_user and (not current_user.is_super_admin or "impersonate_token" in st.session_state):
            st.markdown("#### 📊 Sistema")
            for page_name in AUTHENTICATED_PAGES.keys():
                if st.button(page_name, use_container_width=True, key=f"page_{page_name}"):
                    st.session_state.current_page = page_name
                    st.rerun()

        st.divider()

        # Exit Impersonate button (if impersonating)
        if current_user and current_user.is_super_admin and "impersonate_token" in st.session_state:
            if st.button("🔙 Sair do Impersonate", use_container_width=True, type="primary"):
                # Clear impersonate data
                del st.session_state.impersonate_token
                del st.session_state.impersonating_company
                if "impersonate_expires" in st.session_state:
                    del st.session_state.impersonate_expires

                # Restore super admin token
                http_client.set_auth_token(st.session_state.access_token)

                # Redirect to Admin page
                st.session_state.current_page = "Admin"

                st.success("✅ Modo impersonate desativado. Voltando ao painel admin...")
                st.rerun()

            st.divider()

        # Logout button
        if st.button("🚪 Sair", use_container_width=True, type="secondary"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]

            # Reset to initial state
            st.session_state.is_authenticated = False
            st.session_state.current_page = "Login"

            # Clear HTTP client token
            http_client.set_auth_token(None)

            st.rerun()

    # Render current page
    if st.session_state.current_page in AUTHENTICATED_PAGES:
        # Check if super admin is trying to access operational pages without impersonating
        if current_user and current_user.is_super_admin and "impersonate_token" not in st.session_state:
            st.error("❌ **Acesso Negado**")
            st.warning(
                "⚠️ Super admins não podem acessar páginas operacionais diretamente.\n\n"
                "**Para visualizar dados de uma empresa:**\n\n"
                "1. Vá para a página **Admin**\n"
                "2. Clique em **Impersonate** na empresa desejada\n"
                "3. Você terá acesso aos dashboards e lançamentos dessa empresa por 1 hora"
            )
            st.info(
                "💡 **Por quê?**\n\n"
                "Super admins gerenciam empresas e usuários. Para ver dados operacionais, "
                "você precisa escolher qual empresa deseja visualizar através do impersonate. "
                "Isso garante clareza sobre qual empresa você está acessando."
            )
            # Redirect to Admin page
            if st.button("➡️ Ir para Página Admin", type="primary"):
                st.session_state.current_page = "Admin"
                st.rerun()
        else:
            # Regular user or super admin impersonating - allow access
            AUTHENTICATED_PAGES[st.session_state.current_page].render()
    elif st.session_state.current_page in ADMIN_PAGES:
        ADMIN_PAGES[st.session_state.current_page]()
    else:
        # Fallback based on user type
        if current_user and current_user.is_super_admin and "impersonate_token" not in st.session_state:
            # Super admin without impersonate - go to Admin page
            st.session_state.current_page = "Admin"
        else:
            # Regular user or impersonating - go to Dashboard
            st.session_state.current_page = "Dashboard"
        st.rerun()
