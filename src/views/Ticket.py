import streamlit as st


def render():
    st.title("Boletos")

    col1, col2, _ = st.columns([1, 1, 4])

    with col1:
        options = ["2025", "2026"]
        selected_year = st.selectbox(
            "Ano",
            options=options,
            index=0,
            key="year_selector",
            label_visibility="visible",
        )

    with col2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        st.button("Buscar", use_container_width=True)

    st.divider()
