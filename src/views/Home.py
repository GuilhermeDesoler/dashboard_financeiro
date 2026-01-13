import streamlit as st


def render():
    st.title("Home")
    st.write("Bem-vindo à página inicial")

    st.info("Esta é a página Home")

    # TEMPORÁRIO - Mostrar token para desenvolvimento
    with st.expander("🔑 TOKEN DE DESENVOLVIMENTO (TEMPORÁRIO)", expanded=False):
        access_token = st.session_state.get("access_token", "Token não encontrado")
        st.code(access_token, language="text")
        st.caption("⚠️ Use este token no script import_lancamentos.py")

    if st.button("Clique aqui"):
        st.success("Botão clicado!")
