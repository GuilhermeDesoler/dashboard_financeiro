import streamlit as st
import pandas as pd
from datetime import datetime
from dependencies import get_container


def render():
    st.title("🗄️ Lançamentos Financeiros")

    container = get_container()
    modality_use_cases = container.payment_modality_use_cases
    entry_use_cases = container.financial_entry_use_cases

    try:
        modalities = modality_use_cases.list_active_modalities()

        if not modalities:
            st.warning(
                "⚠️ Nenhuma modalidade de pagamento cadastrada. "
                "Por favor, cadastre modalidades na página 'Modalidades'."
            )
            return

        with st.form("database_form"):
            date = st.date_input("Data", format="DD/MM/YYYY", value=datetime.now())

            col1, col2 = st.columns(2)
            with col1:
                value = st.number_input("Valor (R$)", min_value=0.0, step=0.01)

            with col2:
                modality_options = {m.name: m for m in modalities}
                selected_name = st.selectbox("Modalidade", options=list(modality_options.keys()))
                selected_modality = modality_options[selected_name]

            _, col_button = st.columns([3, 1])
            with col_button:
                submitted = st.form_submit_button("💾 Salvar", use_container_width=True)

            if submitted:
                try:
                    entry_datetime = datetime.combine(date, datetime.min.time())
                    entry_use_cases.create_entry(
                        value=value,
                        date=entry_datetime,
                        modality_id=selected_modality.id,
                        modality_name=selected_modality.name,
                    )
                    st.success("✅ Lançamento salvo com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar: {str(e)}")

        st.divider()
        st.subheader("📊 Lançamentos Registrados")

        st.markdown("### 🔍 Filtros")
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            start_date = st.date_input(
                "Data Início", value=None, format="DD/MM/YYYY", key="filtro_inicio"
            )

        with col2:
            end_date = st.date_input(
                "Data Fim", value=None, format="DD/MM/YYYY", key="filtro_fim"
            )

        with col3:
            st.write("")
            st.write("")
            if st.button("🔄 Limpar", use_container_width=True):
                st.session_state.filtro_inicio = None
                st.session_state.filtro_fim = None
                st.rerun()

        try:
            start_datetime = (
                datetime.combine(start_date, datetime.min.time()) if start_date else None
            )
            end_datetime = (
                datetime.combine(end_date, datetime.max.time()) if end_date else None
            )

            entries = entry_use_cases.list_entries(start_datetime, end_datetime)

            if not entries:
                st.info("ℹ️ Nenhum lançamento encontrado no período selecionado.")
            else:
                total = entry_use_cases.get_total_by_period(start_datetime, end_datetime)
                st.markdown(f"### 💰 Total: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                st.divider()

                df_data = []
                for entry in sorted(entries, key=lambda x: x.date, reverse=True):
                    df_data.append(
                        {
                            "Data": entry.date.strftime("%d/%m/%Y"),
                            "Valor": f"R$ {entry.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                            "Modalidade": entry.modality_name,
                            "ID": entry.id,
                        }
                    )

                df = pd.DataFrame(df_data)

                st.dataframe(
                    df[["Data", "Valor", "Modalidade"]],
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                )

                st.subheader("🗑️ Excluir Lançamento")
                entry_to_delete = st.selectbox(
                    "Selecione o lançamento para excluir",
                    options=[f"{e['Data']} - {e['Modalidade']} - {e['Valor']}" for e in df_data],
                    key="delete_entry",
                )

                if st.button("🗑️ Excluir", type="primary"):
                    idx = [f"{e['Data']} - {e['Modalidade']} - {e['Valor']}" for e in df_data].index(
                        entry_to_delete
                    )
                    entry_id = df_data[idx]["ID"]
                    try:
                        entry_use_cases.delete_entry(entry_id)
                        st.success("✅ Lançamento excluído com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao excluir: {str(e)}")

        except Exception as e:
            st.error(f"❌ Erro ao carregar lançamentos: {str(e)}")

    except Exception as e:
        st.error(f"❌ Erro ao conectar com a API: {str(e)}")
        st.info("ℹ️ Verifique se a URL da API está configurada corretamente no arquivo .env")
