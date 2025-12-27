import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components import render_api_health_check


def render():
    st.title("📊 Dashboard Financeiro")

    # Componente de debug da API
    render_api_health_check()

    container = get_container()
    entry_use_cases = container.financial_entry_use_cases

    try:
        col1, col2, col3 = st.columns(3)

        today = datetime.now()
        start_of_month = datetime(today.year, today.month, 1)
        end_of_month = today.replace(
            day=1, month=today.month % 12 + 1, year=today.year + (today.month // 12)
        ) - timedelta(days=1)

        with col1:
            st.date_input(
                "📅 Data Início",
                value=start_of_month,
                format="DD/MM/YYYY",
                key="dashboard_start",
            )

        with col2:
            st.date_input(
                "📅 Data Fim",
                value=end_of_month,
                format="DD/MM/YYYY",
                key="dashboard_end",
            )

        with col3:
            st.write("")
            st.write("")
            if st.button("🔄 Atualizar", use_container_width=True):
                st.rerun()

        start_datetime = datetime.combine(
            st.session_state.dashboard_start, datetime.min.time()
        )
        end_datetime = datetime.combine(
            st.session_state.dashboard_end, datetime.max.time()
        )

        entries = entry_use_cases.list_entries(start_datetime, end_datetime)
        total = entry_use_cases.get_total_by_period(start_datetime, end_datetime)
        grouped = entry_use_cases.get_entries_grouped_by_modality(
            start_datetime, end_datetime
        )

        st.divider()

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric(
                label="💰 Total do Período",
                value=f"R$ {total:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", "."),
            )

        with metric_col2:
            st.metric(label="📝 Total de Lançamentos", value=len(entries))

        with metric_col3:
            avg = total / len(entries) if entries else 0
            st.metric(
                label="📊 Ticket Médio",
                value=f"R$ {avg:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", "."),
            )

        st.divider()

        if not entries:
            st.info("ℹ️ Nenhum lançamento encontrado no período selecionado.")
            return

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("📈 Evolução Diária")

            daily_totals = {}
            for entry in entries:
                date_key = entry.date.strftime("%Y-%m-%d")
                if date_key not in daily_totals:
                    daily_totals[date_key] = 0
                daily_totals[date_key] += entry.value

            df_daily = pd.DataFrame(
                [
                    {"Data": date, "Valor": value}
                    for date, value in sorted(daily_totals.items())
                ]
            )
            df_daily["Data"] = pd.to_datetime(df_daily["Data"])

            st.line_chart(df_daily.set_index("Data"), use_container_width=True)

        with col_chart2:
            st.subheader("🥧 Por Modalidade")

            modality_totals = {}
            for modality_name, modality_entries in grouped.items():
                modality_totals[modality_name] = sum(e.value for e in modality_entries)

            df_modality = pd.DataFrame(
                [
                    {"Modalidade": name, "Valor": value}
                    for name, value in sorted(
                        modality_totals.items(), key=lambda x: x[1], reverse=True
                    )
                ]
            )

            if not df_modality.empty:
                st.bar_chart(
                    df_modality.set_index("Modalidade"), use_container_width=True
                )

        st.divider()
        st.subheader("📋 Detalhamento por Modalidade")

        for modality_name, modality_entries in sorted(
            grouped.items(), key=lambda x: sum(e.value for e in x[1]), reverse=True
        ):
            modality_total = sum(e.value for e in modality_entries)
            percentage = (modality_total / total * 100) if total > 0 else 0

            with st.expander(
                f"💳 {modality_name} - R$ {modality_total:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + f" ({percentage:.1f}%)"
            ):
                df_entries = pd.DataFrame(
                    [
                        {
                            "Data": e.date.strftime("%d/%m/%Y"),
                            "Valor": f"R$ {e.value:,.2f}".replace(",", "X")
                            .replace(".", ",")
                            .replace("X", "."),
                        }
                        for e in sorted(modality_entries, key=lambda x: x.date)
                    ]
                )

                st.dataframe(df_entries, use_container_width=True, hide_index=True)

                st.markdown(
                    f"**Total de lançamentos:** {len(modality_entries)} | "
                    f"**Ticket médio:** R$ {(modality_total / len(modality_entries)):,.2f}".replace(
                        ",", "X"
                    )
                    .replace(".", ",")
                    .replace("X", ".")
                )

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        st.info("ℹ️ Verifique se a URL da API está configurada corretamente no arquivo .env")
