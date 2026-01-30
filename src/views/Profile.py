import streamlit as st
from dependencies import get_container
from presentation.components.page_header import render_page_header


def render():
    render_page_header("Perfil")

    container = get_container()
    auth_use_cases = container.auth_use_cases

    # Informações de segurança
    with st.expander("ℹ️ Dicas de Segurança"):
        st.markdown("""
        **Recomendações para uma senha segura:**

        - Use pelo menos 8 caracteres
        - Combine letras maiúsculas e minúsculas
        - Inclua números e caracteres especiais
        - Não use informações pessoais óbvias
        - Não reutilize senhas de outras contas
        - Troque sua senha periodicamente
        """)

    st.divider()

    # Seção de troca de senha
    st.subheader("Alterar Senha", anchor=False)
    st.write("Preencha os campos abaixo para alterar sua senha:")

    with st.form("change_password_form", clear_on_submit=True):
        current_password = st.text_input(
            "Senha Atual",
            type="password",
            placeholder="Digite sua senha atual",
            help="Digite a senha que você usa atualmente"
        )

        new_password = st.text_input(
            "Nova Senha",
            type="password",
            placeholder="Digite a nova senha",
            help="A nova senha deve ter pelo menos 6 caracteres"
        )

        confirm_password = st.text_input(
            "Confirmar Nova Senha",
            type="password",
            placeholder="Digite a nova senha novamente",
            help="Digite a mesma senha para confirmar"
        )

        col1, col2 = st.columns([1, 3])

        with col1:
            submit_button = st.form_submit_button(
                "Alterar Senha",
                use_container_width=True,
                type="primary"
            )

        if submit_button:
            # Validações
            if not current_password or not new_password or not confirm_password:
                st.error("⚠️ Todos os campos são obrigatórios!")
            elif len(new_password) < 6:
                st.error("⚠️ A nova senha deve ter pelo menos 6 caracteres!")
            elif new_password != confirm_password:
                st.error("⚠️ A nova senha e a confirmação não coincidem!")
            elif current_password == new_password:
                st.warning("⚠️ A nova senha deve ser diferente da senha atual!")
            else:
                try:
                    with st.spinner("Alterando senha..."):
                        auth_use_cases.change_password(current_password, new_password)
                        st.success("✅ Senha alterada com sucesso!")
                        st.info("💡 Por segurança, você será desconectado. Faça login novamente com a nova senha.")

                        # Aguardar 2 segundos antes de deslogar
                        import time
                        time.sleep(2)

                        # Limpar sessão e redirecionar para login
                        st.session_state.clear()
                        st.session_state.current_page = "Login"
                        st.rerun()

                except Exception as e:
                    error_msg = str(e)
                    if "Senha atual incorreta" in error_msg or "incorreta" in error_msg.lower():
                        st.error("❌ Senha atual incorreta!")
                    elif "pelo menos 6 caracteres" in error_msg:
                        st.error("⚠️ A nova senha deve ter pelo menos 6 caracteres!")
                    else:
                        st.error(f"❌ Erro ao alterar senha: {error_msg}")

