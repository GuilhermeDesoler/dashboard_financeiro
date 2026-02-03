import streamlit as st
from dependencies import get_container
from presentation.auth_persistence import save_auth_to_session_state


def Login():
    container = get_container()
    auth_use_cases = container.auth_use_cases
    http_client = container.http_client

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("## 🔐 Login")

        if "login_error" in st.session_state:
            st.error(st.session_state.login_error)
            del st.session_state.login_error

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email",
                placeholder="usuario@empresa.com",
                help="Digite seu email cadastrado no sistema",
            )

            password = st.text_input(
                "Senha",
                type="password",
                placeholder="••••••••",
                help="Digite sua senha",
            )

            col_btn1, col_btn2 = st.columns([1, 1])

            with col_btn2:
                login_button = st.form_submit_button(
                    "Entrar", use_container_width=True, type="primary"
                )

            # with col_btn2:
            #     # Placeholder for future "Forgot password" feature
            #     st.markdown(
            #         '<div style="padding-top: 8px; text-align: center; color: #666;">Esqueceu a senha?</div>',
            #         unsafe_allow_html=True
            #     )

        if login_button:
            if not email or not password:
                st.error("Por favor, preencha email e senha")
            else:
                try:
                    with st.spinner("Autenticando..."):
                        auth_token = auth_use_cases.login(email, password)

                        save_auth_to_session_state(
                            auth_token.token, auth_token.refresh_token, auth_token.user
                        )

                        http_client.set_auth_token(auth_token.token)

                        if auth_token.user.is_super_admin:
                            st.session_state.current_page = "Admin"
                        else:
                            st.session_state.current_page = "Lançamentos"

                        st.success(f"Bem-vindo(a), {auth_token.user.name}!")
                        st.rerun()

                except Exception as e:
                    error_msg = str(e)
                    if "401" in error_msg or "Unauthorized" in error_msg:
                        st.error("Email ou senha incorretos")
                    elif "403" in error_msg or "Forbidden" in error_msg:
                        st.error(
                            "Usuário desativado. Entre em contato com o administrador."
                        )
                    else:
                        st.error(f"Erro ao fazer login: {error_msg}")

        st.info(
            "**Sistema Privado**\n\n"
            "Este é um sistema de acesso restrito. "
            "Entre em contato com o administrador para criar sua conta."
        )

        if st.session_state.get("show_debug", False):
            with st.expander("Debug Info"):
                st.json(
                    {
                        "is_authenticated": st.session_state.get(
                            "is_authenticated", False
                        ),
                        "has_token": "access_token" in st.session_state,
                        "current_page": st.session_state.get("current_page", "Login"),
                    }
                )
