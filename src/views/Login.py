import streamlit as st
from dependencies import get_container


def render():
    st.title("Login", anchor=False)

    container = get_container()
    auth_use_cases = container.auth_use_cases

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            st.subheader("Acesse sua conta")

            email = st.text_input(
                "Email",
                placeholder="seu@email.com",
                key="login_email",
            )

            password = st.text_input(
                "Senha",
                type="password",
                placeholder="••••••••",
                key="login_password",
            )

            col_login, col_register = st.columns(2)

            with col_login:
                submitted = st.form_submit_button(
                    "Entrar", use_container_width=True, type="primary"
                )

            with col_register:
                if st.form_submit_button("Criar conta", use_container_width=True):
                    st.session_state.current_page = "Register"
                    st.rerun()

            if submitted:
                if not email or not password:
                    st.error("Por favor, preencha todos os campos.")
                else:
                    try:
                        auth_response = auth_use_cases.login(email, password)

                        # Store authentication data in session state
                        st.session_state.auth_token = auth_response.token
                        st.session_state.refresh_token = auth_response.refresh_token
                        st.session_state.user = auth_response.user
                        st.session_state.is_authenticated = True

                        st.success("Login realizado com sucesso!")
                        st.session_state.current_page = "Dashboard"
                        st.rerun()

                    except Exception as e:
                        st.error(f"Erro ao fazer login: {str(e)}")

        st.divider()
        st.info("Faça login para acessar o sistema financeiro.")
