import streamlit as st
from dependencies import get_container


def render():
    st.title("Criar Conta", anchor=False)

    container = get_container()
    auth_use_cases = container.auth_use_cases

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("register_form"):
            st.subheader("Registre sua empresa")

            name = st.text_input(
                "Nome completo",
                placeholder="João Silva",
                key="register_name",
            )

            email = st.text_input(
                "Email",
                placeholder="seu@email.com",
                key="register_email",
            )

            password = st.text_input(
                "Senha",
                type="password",
                placeholder="••••••••",
                key="register_password",
            )

            confirm_password = st.text_input(
                "Confirmar senha",
                type="password",
                placeholder="••••••••",
                key="register_confirm_password",
            )

            st.divider()

            company_name = st.text_input(
                "Nome da Empresa",
                placeholder="Minha Empresa Ltda",
                key="register_company_name",
            )

            cnpj = st.text_input(
                "CNPJ",
                placeholder="00.000.000/0000-00",
                key="register_cnpj",
            )

            col_register, col_back = st.columns(2)

            with col_register:
                submitted = st.form_submit_button(
                    "Criar conta", use_container_width=True, type="primary"
                )

            with col_back:
                if st.form_submit_button("Voltar", use_container_width=True):
                    st.session_state.current_page = "Login"
                    st.rerun()

            if submitted:
                if not all([name, email, password, confirm_password, company_name, cnpj]):
                    st.error("Por favor, preencha todos os campos.")
                elif password != confirm_password:
                    st.error("As senhas não coincidem.")
                elif len(password) < 6:
                    st.error("A senha deve ter no mínimo 6 caracteres.")
                else:
                    try:
                        response = auth_use_cases.register(
                            email=email,
                            password=password,
                            name=name,
                            company_name=company_name,
                            cnpj=cnpj,
                        )

                        st.success(f"Conta criada com sucesso! Faça login para continuar.")
                        st.balloons()

                        # Redirect to login after 2 seconds
                        st.session_state.current_page = "Login"
                        st.rerun()

                    except Exception as e:
                        st.error(f"Erro ao criar conta: {str(e)}")

        st.divider()
        st.info("Crie uma conta para começar a usar o sistema financeiro.")
