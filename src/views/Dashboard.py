import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components import render_api_health_check
from presentation.components.page_header import render_page_header
import plotly.express as px
import plotly.graph_objects as go


def render():
    render_page_header("Dashboard Financeiro")

    container = get_container()
    entry_use_cases = container.financial_entry_use_cases
    modality_use_cases = container.payment_modality_use_cases

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

        # Cards de métricas estilo dashboard
        modalities = modality_use_cases.list_active_modalities()

        # Criar mapeamento de modality_id para cor
        modality_color_map = {m.id: m.color for m in modalities}
        modality_name_map = {m.id: m.name for m in modalities}

        # Agrupar lançamentos por modalidade
        modality_stats = {}
        for entry in entries:
            # Usar a cor da modalidade atual, não a cor salva no entry
            modality_color = modality_color_map.get(
                entry.modality_id, entry.modality_color
            )
            modality_name = modality_name_map.get(
                entry.modality_id, entry.modality_name
            )

            if modality_name not in modality_stats:
                modality_stats[modality_name] = {
                    "count": 0,
                    "total": 0,
                    "color": modality_color,
                }
            modality_stats[modality_name]["count"] += 1
            modality_stats[modality_name]["total"] += entry.value

        # Exibir TODOS os cards de métricas com scroll horizontal
        top_modalities = sorted(
            modality_stats.items(), key=lambda x: x[1]["total"], reverse=True
        )

        if top_modalities:
            # Container flex com scroll horizontal
            cards_html = '<div style="display: flex; gap: 12px; overflow-x: auto; overflow-y: visible; padding-bottom: 15px;">'

            for modality_name, stats in top_modalities:
                formatted_value = (
                    f"R$ {stats['total']:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
                cards_html += f'<div style="border: 2px solid {stats["color"]}; border-radius: 8px; padding: 15px; background: #f5f5f5; min-width: 200px; flex-shrink: 0;"><p style="margin: 0; font-size: 12px; color: #666;">{modality_name}</p><h2 style="margin: 5px 0; font-size: 24px;">{formatted_value}</h2><p style="margin: 0; font-size: 14px; color: #28a745; font-weight: bold;">{stats["count"]} lançamentos</p></div>'

            cards_html += '</div>'
            st.markdown(cards_html, unsafe_allow_html=True)

            st.divider()
        else:
            st.info("Nenhum lançamento encontrado no período selecionado.")
            return

        if not entries:
            st.info("Nenhum lançamento encontrado no período selecionado.")
            return

        # Gráfico de barras por data com cores das modalidades
        st.subheader("Lançamentos por Data", anchor=False)

        # Agrupar por data e modalidade
        date_modality_data = {}
        for entry in entries:
            date_str = entry.date.strftime("%d/%m/%Y")
            # Usar a cor da modalidade atual, não a cor salva no entry
            modality_color = modality_color_map.get(
                entry.modality_id, entry.modality_color
            )
            modality_name = modality_name_map.get(
                entry.modality_id, entry.modality_name
            )

            if date_str not in date_modality_data:
                date_modality_data[date_str] = {}
            if modality_name not in date_modality_data[date_str]:
                date_modality_data[date_str][modality_name] = {
                    "count": 0,
                    "color": modality_color,
                }
            date_modality_data[date_str][modality_name]["count"] += 1

        # Criar dados para o gráfico
        chart_data = []
        for date_str, modalities_data in sorted(date_modality_data.items()):
            for modality_name, data in modalities_data.items():
                chart_data.append(
                    {
                        "Data": date_str,
                        "Modalidade": modality_name,
                        "Quantidade": data["count"],
                        "Cor": data["color"],
                    }
                )

        if chart_data:
            df_chart = pd.DataFrame(chart_data)

            # Criar gráfico de barras com plotly
            color_map = {
                row["Modalidade"]: row["Cor"] for _, row in df_chart.iterrows()
            }

            fig = px.bar(
                df_chart,
                x="Data",
                y="Quantidade",
                color="Modalidade",
                color_discrete_map=color_map,
                barmode="group",
                height=400,
            )

            fig.update_layout(
                xaxis_title="",
                yaxis_title="Quantidade",
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("📋 Detalhamento por Modalidade", anchor=False)

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
        st.info(
            "ℹ️ Verifique se a URL da API está configurada corretamente no arquivo .env"
        )
