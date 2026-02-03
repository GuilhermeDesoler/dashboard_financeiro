import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components.page_header import render_page_header
import plotly.express as px


def render():
    render_page_header("Registrar Lançamento")

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

        # Cards principais: Total Geral, Total sem Crediário e Acumulado Anual
        col_card1, col_card2, col_card3 = st.columns(3)

        # Calcular total sem crediário (usando o campo booleano is_credit_plan)
        total_sem_crediario = sum(e.value for e in entries if not e.is_credit_plan)

        # Calcular acumulado anual (ano atual até hoje)
        year_start = datetime(today.year, 1, 1)
        year_end = datetime.now()
        entries_year = entry_use_cases.list_entries(year_start, year_end)
        total_year = sum(e.value for e in entries_year)

        with col_card1:
            total_formatted = (
                f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )
            st.markdown(
                f"""
                <div style="border: 3px solid #9333EA; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); text-align: center;">
                    <p style="margin: 0; font-size: 14px; color: #6b21a8; font-weight: 600;">TOTAL GERAL (PERÍODO)</p>
                    <h1 style="margin: 10px 0; font-size: 32px; color: #9333EA;">{total_formatted}</h1>
                    <p style="margin: 0; font-size: 12px; color: #6b21a8;">{len(entries)} lançamentos</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_card2:
            total_sem_crediario_formatted = (
                f"R$ {total_sem_crediario:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.markdown(
                f"""
                <div style="border: 3px solid #10B981; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); text-align: center;">
                    <p style="margin: 0; font-size: 14px; color: #047857; font-weight: 600;">TOTAL SEM CREDIÁRIO</p>
                    <h1 style="margin: 10px 0; font-size: 32px; color: #10B981;">{total_sem_crediario_formatted}</h1>
                    <p style="margin: 0; font-size: 12px; color: #047857;">Excluindo lançamentos crediário</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_card3:
            # Formatar valor por extenso
            def format_currency_text(value):
                """Formata valor em reais por extenso (simplificado)"""
                if value >= 1000000:
                    return f"{value/1000000:.1f}".replace(".", ",") + " milhões"
                elif value >= 1000:
                    return f"{value/1000:.1f}".replace(".", ",") + " mil"
                else:
                    return f"{value:.2f}".replace(".", ",")

            total_year_formatted = (
                f"R$ {total_year:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )
            total_year_text = format_currency_text(total_year)

            st.markdown(
                f"""
                <div style="border: 3px solid #F59E0B; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); text-align: center;">
                    <p style="margin: 0; font-size: 14px; color: #92400e; font-weight: 600;">ACUMULADO ANUAL {today.year}</p>
                    <h1 style="margin: 10px 0; font-size: 32px; color: #F59E0B;">{total_year_formatted}</h1>
                    <p style="margin: 0; font-size: 12px; color: #92400e;">Aproximadamente R$ {total_year_text}</p>
                </div>
                """,
                unsafe_allow_html=True,
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

        # Card de Pagamentos de Crediário
        credit_payments = [e for e in entries if e.credit_payment]

        if credit_payments:
            # Agrupar pagamentos de crediário por modalidade
            credit_payment_by_modality = {}
            for entry in credit_payments:
                modality_key = entry.modality_id
                # Usar o nome da modalidade com banco do mapeamento
                modality_display_name = modality_name_map.get(
                    entry.modality_id, entry.modality_name
                )

                if modality_key not in credit_payment_by_modality:
                    credit_payment_by_modality[modality_key] = {
                        "modality_name": modality_display_name,
                        "total": 0,
                        "count": 0,
                    }
                credit_payment_by_modality[modality_key]["total"] += entry.value
                credit_payment_by_modality[modality_key]["count"] += 1

            # Calcular total geral de pagamentos de crediário
            total_credit_payments = sum(e.value for e in credit_payments)
            total_credit_payments_formatted = (
                f"R$ {total_credit_payments:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            # Card de Pagamentos de Crediário (estilo compacto com subcards, alinhado à esquerda)
            card_html = f"""<div style="border: 2px solid #F59E0B; border-radius: 8px; padding: 15px; background: #fffbeb; margin-bottom: 15px;">
<p style="margin: 0 0 8px 0; font-size: 12px; color: #92400e; font-weight: 600;">Pagamento de Crediário</p>
<h2 style="margin: 0 0 10px 0; font-size: 24px; color: #F59E0B;">{total_credit_payments_formatted}</h2>
<p style="margin: 0 0 12px 0; font-size: 11px; color: #92400e;">{len(credit_payments)} lançamentos</p>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 8px; margin-top: 12px;">"""

            # Adicionar cada modalidade (informações em linha dentro de cada subcard)
            for modality_data in sorted(
                credit_payment_by_modality.values(),
                key=lambda x: x["total"],
                reverse=True,
            ):
                modality_total_formatted = (
                    f"R$ {modality_data['total']:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
                card_html += f"""<div style="background: white; border: 1px solid #FCD34D; border-radius: 6px; padding: 10px; text-align: left;">
<p style="margin: 0 0 4px 0; font-size: 11px; color: #92400e; font-weight: 600;">{modality_data['modality_name']} - {modality_data['count']} lançamentos</p>
<p style="margin: 0; font-size: 16px; color: #F59E0B; font-weight: bold;">{modality_total_formatted}</p>
</div>"""

            card_html += "</div></div>"
            st.markdown(card_html, unsafe_allow_html=True)

            st.divider()

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

        if entries:
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

                # Separar crediário de não-crediário
                crediario_entries = [e for e in modality_entries if e.is_credit_plan]
                pagamentos_crediario = [e for e in modality_entries if e.credit_payment]
                outros_entries = [e for e in modality_entries if not e.is_credit_plan and not e.credit_payment]

                crediario_total = sum(e.value for e in crediario_entries)
                pagamentos_total = sum(e.value for e in pagamentos_crediario)
                outros_total = sum(e.value for e in outros_entries)

                with st.expander(
                    f"{modality_name} - R$ {modality_total:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                    + f" ({percentage:.1f}%)"
                ):
                    # Se houver crediário, mostrar separado
                    if crediario_entries:
                        st.markdown("### 💳 Pagamento de Crediário")
                        crediario_fmt = f"R$ {crediario_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        st.markdown(f"**Total:** {crediario_fmt} ({len(crediario_entries)} lançamentos)")

                        df_crediario = pd.DataFrame(
                            [
                                {
                                    "Data": e.date.strftime("%d/%m/%Y"),
                                    "Valor": f"R$ {e.value:,.2f}".replace(",", "X")
                                    .replace(".", ",")
                                    .replace("X", "."),
                                }
                                for e in sorted(crediario_entries, key=lambda x: x.date)
                            ]
                        )
                        st.dataframe(df_crediario, use_container_width=True, hide_index=True)
                        st.divider()

                    # Se houver pagamentos de crediário recebidos
                    if pagamentos_crediario:
                        st.markdown("### ✅ Recebimento de Crediário")
                        pagamentos_fmt = f"R$ {pagamentos_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        st.markdown(f"**Total:** {pagamentos_fmt} ({len(pagamentos_crediario)} lançamentos)")

                        df_pagamentos = pd.DataFrame(
                            [
                                {
                                    "Data": e.date.strftime("%d/%m/%Y"),
                                    "Valor": f"R$ {e.value:,.2f}".replace(",", "X")
                                    .replace(".", ",")
                                    .replace("X", "."),
                                }
                                for e in sorted(pagamentos_crediario, key=lambda x: x.date)
                            ]
                        )
                        st.dataframe(df_pagamentos, use_container_width=True, hide_index=True)
                        st.divider()

                    # Mostrar outros lançamentos
                    if outros_entries:
                        st.markdown("### 📊 Outros Lançamentos")
                        outros_fmt = f"R$ {outros_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        st.markdown(f"**Total:** {outros_fmt} ({len(outros_entries)} lançamentos)")

                        df_outros = pd.DataFrame(
                            [
                                {
                                    "Data": e.date.strftime("%d/%m/%Y"),
                                    "Valor": f"R$ {e.value:,.2f}".replace(",", "X")
                                    .replace(".", ",")
                                    .replace("X", "."),
                                }
                                for e in sorted(outros_entries, key=lambda x: x.date)
                            ]
                        )
                        st.dataframe(df_outros, use_container_width=True, hide_index=True)

                    # Ticket médio
                    st.markdown(
                        f"**Total de lançamentos:** {len(modality_entries)} | "
                        f"**Ticket médio:** R$ {(modality_total / len(modality_entries)):,.2f}".replace(
                            ",", "X"
                        )
                        .replace(".", ",")
                        .replace("X", ".")
                    )

        st.divider()

        # Seção de Agenda de Crediário (última seção)
        st.subheader("📅 Agenda de Crediário", anchor=False)

        # Filtro independente para a seção de Crediário
        col_cred1, col_cred2, col_cred3 = st.columns(3)

        with col_cred1:
            st.date_input(
                "Data Início",
                value=start_of_month,
                format="DD/MM/YYYY",
                key="crediario_start",
            )

        with col_cred2:
            st.date_input(
                "Data Fim",
                value=end_of_month,
                format="DD/MM/YYYY",
                key="crediario_end",
            )

        with col_cred3:
            st.write("")
            st.write("")
            if st.button("Filtrar Crediário", use_container_width=True, key="btn_crediario"):
                st.rerun()

        crediario_start_datetime = datetime.combine(
            st.session_state.crediario_start, datetime.min.time()
        )
        crediario_end_datetime = datetime.combine(
            st.session_state.crediario_end, datetime.max.time()
        )

        try:
            daily_summary = installment_use_cases.get_daily_summary(
                crediario_start_datetime, crediario_end_datetime
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
                        "difference": day["difference"],
                    }

                # Ordenar meses (de janeiro a dezembro - ordem crescente)
                sorted_months = sorted(
                    monthly_data.keys(),
                    key=lambda x: datetime.strptime(x, "%m/%Y"),
                    reverse=False,
                )

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
                    month_receivable = sum(
                        data.get("receivable", 0)
                        for data in monthly_data[month].values()
                    )
                    month_received = sum(
                        data.get("received", 0) for data in monthly_data[month].values()
                    )
                    month_totals[month] = {
                        "receivable": month_receivable,
                        "received": month_received,
                    }

                    header_label = (
                        f"{month}<br/>A Rec: R$ {month_receivable:,.2f} | Receb: R$ {month_received:,.2f}".replace(
                            ",", "X"
                        )
                        .replace(".", ",")
                        .replace("X", ".")
                    )
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
                        day_data = monthly_data[month].get(
                            day, {"receivable": 0, "received": 0}
                        )

                        # A Receber - só pinta se tiver valor
                        if day_data["receivable"] > 0:
                            receivable_formatted = (
                                f"R$ {day_data['receivable']:,.2f}".replace(",", "X")
                                .replace(".", ",")
                                .replace("X", ".")
                            )
                            html_content += f"<td class='receivable-cell-filled'>{receivable_formatted}</td>"
                        else:
                            html_content += "<td>-</td>"

                        # Recebido - só pinta se tiver valor
                        if day_data["received"] > 0:
                            received_formatted = (
                                f"R$ {day_data['received']:,.2f}".replace(",", "X")
                                .replace(".", ",")
                                .replace("X", ".")
                            )
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
