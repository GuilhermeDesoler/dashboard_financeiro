import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components.company_header import render_company_header
import plotly.express as px


def render():
    render_company_header("Dashboard Financeiro")

    # Verificar se o usuário é admin
    current_user = st.session_state.get("current_user")
    if not current_user or not current_user.is_admin():
        st.error("**Acesso Negado**")
        st.warning(
            "Esta página está disponível apenas para **Administradores**.\n\n"
            "Se você precisa acessar esta funcionalidade, entre em contato com o administrador da sua empresa."
        )
        return

    container = get_container()
    entry_use_cases = container.financial_entry_use_cases
    modality_use_cases = container.payment_modality_use_cases
    installment_use_cases = container.installment_use_cases

    try:
        col1, col2, col3 = st.columns(3)

        today = datetime.now()
        start_of_month = datetime(today.year, today.month, 1)
        end_of_month = today.replace(
            day=1, month=today.month % 12 + 1, year=today.year + (today.month // 12)
        ) - timedelta(days=1)

        with col1:
            st.date_input(
                "Data Início",
                value=start_of_month,
                format="DD/MM/YYYY",
                key="dashboard_start",
            )

        with col2:
            st.date_input(
                "Data Fim",
                value=end_of_month,
                format="DD/MM/YYYY",
                key="dashboard_end",
            )

        with col3:
            st.write("")
            st.write("")
            if st.button("Atualizar", use_container_width=True):
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

        # Cards principais: Total Geral e Total sem Crediário
        col_card1, col_card2 = st.columns(2)

        # Calcular total sem crediário (usando o campo booleano is_credit_plan)
        total_sem_crediario = sum(
            e.value for e in entries
            if not e.is_credit_plan
        )

        with col_card1:
            total_formatted = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.markdown(
                f"""
                <div style="border: 3px solid #9333EA; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); text-align: center;">
                    <p style="margin: 0; font-size: 14px; color: #6b21a8; font-weight: 600;">TOTAL GERAL</p>
                    <h1 style="margin: 10px 0; font-size: 32px; color: #9333EA;">{total_formatted}</h1>
                    <p style="margin: 0; font-size: 12px; color: #6b21a8;">{len(entries)} lançamentos</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_card2:
            total_sem_crediario_formatted = f"R$ {total_sem_crediario:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.markdown(
                f"""
                <div style="border: 3px solid #10B981; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); text-align: center;">
                    <p style="margin: 0; font-size: 14px; color: #047857; font-weight: 600;">TOTAL SEM CREDIÁRIO</p>
                    <h1 style="margin: 10px 0; font-size: 32px; color: #10B981;">{total_sem_crediario_formatted}</h1>
                    <p style="margin: 0; font-size: 12px; color: #047857;">Excluindo lançamentos crediário</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        # Cards de métricas estilo dashboard
        modalities = modality_use_cases.list_active_modalities()

        # Criar mapeamento de modality_id para cor, nome e banco
        modality_color_map = {m.id: m.color for m in modalities}
        modality_name_map = {}
        for m in modalities:
            # Incluir banco no nome se disponível
            display_name = f"{m.name} ({m.bank_name})" if m.bank_name else m.name
            modality_name_map[m.id] = display_name

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

            cards_html += "</div>"
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
        st.subheader("Detalhamento por Modalidade", anchor=False)

        for modality_name, modality_entries in sorted(
            grouped.items(), key=lambda x: sum(e.value for e in x[1]), reverse=True
        ):
            modality_total = sum(e.value for e in modality_entries)
            percentage = (modality_total / total * 100) if total > 0 else 0

            with st.expander(
                f"{modality_name} - R$ {modality_total:,.2f}".replace(",", "X")
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

        st.divider()

        # Seção de Resumo Diário do Crediário (última seção)
        st.subheader("📊 Resumo Diário - Crediário", anchor=False)

        try:
            daily_summary = installment_use_cases.get_daily_summary(
                start_datetime, end_datetime
            )

            if daily_summary:
                # Organizar dados por mês e dia
                from collections import defaultdict
                monthly_data = defaultdict(lambda: {})

                for day in daily_summary:
                    date_obj = datetime.fromisoformat(day["date"])
                    month_key = date_obj.strftime("%m/%Y")
                    day_number = date_obj.day

                    if month_key not in monthly_data:
                        monthly_data[month_key] = {}

                    monthly_data[month_key][day_number] = {
                        "receivable": day["total_receivable"],
                        "received": day["total_received"],
                        "difference": day["difference"]
                    }

                # Ordenar meses (mais recente primeiro)
                sorted_months = sorted(monthly_data.keys(),
                                      key=lambda x: datetime.strptime(x, "%m/%Y"),
                                      reverse=True)

                # Criar HTML da tabela
                html_content = """
                <style>
                .credit-scroll-container {
                    overflow-x: auto;
                    margin: 20px 0;
                }
                .credit-scroll-container::-webkit-scrollbar {
                    height: 12px;
                    width: 12px;
                }
                .credit-scroll-container::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 10px;
                }
                .credit-scroll-container::-webkit-scrollbar-thumb {
                    background: #9333EA;
                    border-radius: 10px;
                }
                .credit-scroll-container::-webkit-scrollbar-thumb:hover {
                    background: #7c2cc9;
                }
                .credit-table {
                    border-collapse: collapse;
                }
                .credit-table th {
                    background-color: #9333EA;
                    color: white;
                    padding: 6px 8px;
                    text-align: center;
                    border: 1px solid #ddd;
                    font-weight: bold;
                    font-size: 12px;
                    position: sticky;
                    top: 0;
                    z-index: 10;
                }
                .credit-table td {
                    padding: 4px 6px;
                    border: 1px solid #ddd;
                    text-align: center;
                    min-width: 90px;
                    font-size: 11px;
                    white-space: nowrap;
                }
                .credit-table .day-label {
                    background-color: #f0f0f0;
                    font-weight: bold;
                    min-width: 45px;
                    font-size: 11px;
                    position: sticky;
                    left: 0;
                    z-index: 5;
                }
                .receivable-cell-filled {
                    background-color: rgba(255, 193, 7, 0.6);
                    color: #856404;
                    font-weight: bold;
                }
                .received-cell-filled {
                    background-color: rgba(40, 167, 69, 0.6);
                    color: #155724;
                    font-weight: bold;
                }
                </style>
                <div class='credit-scroll-container'>
                <table class='credit-table'>
                """

                # Cabeçalho com os meses
                html_content += "<thead><tr><th>Dia</th>"
                month_totals = {}
                for month in sorted_months:
                    month_receivable = sum(data.get("receivable", 0) for data in monthly_data[month].values())
                    month_received = sum(data.get("received", 0) for data in monthly_data[month].values())
                    month_totals[month] = {"receivable": month_receivable, "received": month_received}

                    header_label = f"{month}<br/>A Rec: R$ {month_receivable:,.2f} | Receb: R$ {month_received:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    html_content += f"<th colspan='2'>{header_label}</th>"
                html_content += "</tr>"

                # Sub-cabeçalho (A Receber / Recebido)
                html_content += "<tr><th></th>"
                for month in sorted_months:
                    html_content += "<th style='background-color: rgba(255, 193, 7, 0.6); color: #856404;'>A Receber</th>"
                    html_content += "<th style='background-color: rgba(40, 167, 69, 0.6); color: #155724;'>Recebido</th>"
                html_content += "</tr></thead>"

                # Corpo da tabela - 31 linhas (dias)
                html_content += "<tbody>"
                for day in range(1, 32):
                    html_content += f"<tr><td class='day-label'>Dia {day:02d}</td>"

                    for month in sorted_months:
                        day_data = monthly_data[month].get(day, {"receivable": 0, "received": 0})

                        # A Receber - só pinta se tiver valor
                        if day_data['receivable'] > 0:
                            receivable_formatted = f"R$ {day_data['receivable']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                            html_content += f"<td class='receivable-cell-filled'>{receivable_formatted}</td>"
                        else:
                            html_content += "<td>-</td>"

                        # Recebido - só pinta se tiver valor
                        if day_data['received'] > 0:
                            received_formatted = f"R$ {day_data['received']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                            html_content += f"<td class='received-cell-filled'>{received_formatted}</td>"
                        else:
                            html_content += "<td>-</td>"

                    html_content += "</tr>"

                html_content += "</tbody></table></div>"

                st.markdown(html_content, unsafe_allow_html=True)

            else:
                st.info("Nenhum dado de crediário encontrado no período selecionado.")

        except Exception as e:
            st.error(f"Erro ao carregar resumo do crediário: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.info(
            "Verifique se a URL da API está configurada corretamente no arquivo .env"
        )
