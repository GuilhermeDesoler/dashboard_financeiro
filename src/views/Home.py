import streamlit as st


def render():
    st.title("🏠 Home")
    st.write("Bem-vindo à página inicial")

    st.info("Esta é a página Home")

    if st.button("Clique aqui"):
        st.success("Botão clicado!")
