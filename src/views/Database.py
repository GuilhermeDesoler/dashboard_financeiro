import streamlit as st
from data import (
    TransactionType,
    add,
    get_all,
    AddRequest,
    get_transaction_options,
    get_transaction_label,
)
import locale

try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except:
    try:
        locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")
    except:
        pass


def render():
    st.title("🗄️ Database")

    with st.form("database_form"):
        date = st.date_input("Data", format="DD/MM/YYYY")

        col1, col2 = st.columns(2)
        with col1:
            value = st.number_input("Valor (R$)", min_value=0.0, step=0.01)

        with col2:
            tipo_options = get_transaction_options()
            tipo_selecionado = st.selectbox("Tipo", options=list(tipo_options.keys()))
            transaction_type = tipo_options[tipo_selecionado]

        _, col_button = st.columns([3, 1])
        with col_button:
            submitted = st.form_submit_button("Salvar", use_container_width=True)

        if submitted:
            request = AddRequest(
                day=date.strftime("%d/%m/%Y"), value=value, type=transaction_type
            )
            add(request)
            st.success("✅ Salvo!")

    st.divider()
    st.subheader("📊 Transações Registradas")

    data = get_all()
    if not data:
        st.info("Nenhuma transação registrada ainda.")
    else:
        import pandas as pd
        from datetime import datetime

        st.markdown("### 🔍 Filtros")
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            data_inicio = st.date_input(
                "Data Início", value=None, format="DD/MM/YYYY", key="filtro_inicio"
            )

        with col2:
            data_fim = st.date_input(
                "Data Fim", value=None, format="DD/MM/YYYY", key="filtro_fim"
            )

        with col3:
            st.write("")
            st.write("")
            if st.button("Limpar Filtros", use_container_width=True):
                st.session_state.filtro_inicio = None
                st.session_state.filtro_fim = None
                st.rerun()

        filtered_data = {}
        for date_key, transactions in data.items():
            try:
                date_obj = datetime.strptime(date_key, "%d/%m/%Y").date()

                incluir = True
                if data_inicio and date_obj < data_inicio:
                    incluir = False
                if data_fim and date_obj > data_fim:
                    incluir = False

                if incluir:
                    filtered_data[date_key] = transactions
            except:
                filtered_data[date_key] = transactions

        if not filtered_data:
            st.warning("Nenhuma transação encontrada no período selecionado.")
        else:
            sorted_dates = sorted(filtered_data.keys(), reverse=True)

            max_transactions = max(
                len(transactions) for transactions in filtered_data.values()
            )

            table_data = {}
            totals = {}

            for date_key in sorted_dates:
                transactions = filtered_data[date_key]
                total = 0
                col_data = []

                for t in transactions:
                    valor = t["valor"]
                    tipo = t["type"]

                    if tipo == TransactionType.RECEBIMENTO_CREDITARIO:
                        total += valor
                    else:
                        total += valor

                    tipo_display = get_transaction_label(tipo)

                    col_data.append(
                        {"valor": valor, "tipo": tipo_display, "tipo_enum": tipo}
                    )

                table_data[date_key] = col_data
                totals[date_key] = total

            total_geral = sum(totals.values())

            st.markdown(f"### 💰 Total: R$ {total_geral:,.2f}")
            st.divider()

            rows = []
            columns = []

            for date_key in sorted_dates:
                columns.append(
                    (f"{date_key} - Total: R$ {totals[date_key]:,.2f}", "Valor")
                )
                columns.append(
                    (f"{date_key} - Total: R$ {totals[date_key]:,.2f}", "Modalidade")
                )

            for i in range(max_transactions):
                row = []
                for date_key in sorted_dates:
                    if i < len(table_data[date_key]):
                        t = table_data[date_key][i]
                        row.append(f"R$ {t['valor']:,.2f}")
                        row.append(t["tipo"])
                    else:
                        row.append("")
                        row.append("")
                rows.append(row)

            df = pd.DataFrame(rows, columns=pd.MultiIndex.from_tuples(columns))

            st.dataframe(df, use_container_width=True, hide_index=True, height=400)
