import streamlit as st
import pandas as pd


def render():
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Métrica 1", "100", "+10%")
    with col2:
        st.metric("Métrica 2", "200", "-5%")
    with col3:
        st.metric("Métrica 3", "300", "+15%")

    st.subheader("Dados de exemplo")
    df = pd.DataFrame({"x": range(10), "y": range(10)})
    st.line_chart(df.set_index("x"))
