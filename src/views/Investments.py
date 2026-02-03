import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components.page_header import render_page_header


def render():
    render_page_header("Investimentos")

    container = get_container()
    account_use_cases = container.account_use_cases

    try:
        # Botão de lançamento isolado
        col1, col2, col3 = st.columns([3, 1, 1])

        with col3:
            if st.button("Lançamento", use_container_width=True, type="primary"):
                st.session_state.show_investment_modal = True

        # Filtros de data - Anualizado (início do ano até hoje)
        col1, col2, col3 = st.columns([2, 2, 1])

        today = datetime.now()
        start_of_year = datetime(today.year, 1, 1)
        end_of_year = today

        with col1:
            st.date_input(
                "Data Início",
                value=start_of_year,
                format="DD/MM/YYYY",
                key="investments_start",
            )

        with col2:
            st.date_input(
                "Data Fim",
                value=end_of_year,
                format="DD/MM/YYYY",
                key="investments_end",
            )

        with col3:
            st.write("")
            st.write("")
            if st.button("Atualizar", use_container_width=True):
                st.rerun()

        start_datetime = datetime.combine(
            st.session_state.investments_start, datetime.min.time()
        )
        end_datetime = datetime.combine(
            st.session_state.investments_end, datetime.max.time()
        )

        # Buscar apenas investimentos
        all_accounts = account_use_cases.list_accounts(start_datetime, end_datetime)
        investments = [acc for acc in all_accounts if acc.type == "investment"]

        st.divider()

        # Cards de resumo
        _render_cards_resumo(investments, today)

        st.divider()

        # Tabela de investimentos
        _render_investments_table(investments, account_use_cases)

        st.divider()

        # Seção de exclusão
        _render_delete_section(investments, account_use_cases)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        import traceback

        st.code(traceback.format_exc())

    # Modal de cadastro
    if st.session_state.get("show_investment_modal", False):
        _render_cadastro_modal(account_use_cases)


def _render_cards_resumo(investments, today):
    """Renderiza cards de resumo"""
    # Total de investimentos realizados e pendentes
    investments_realizados = [inv for inv in investments if inv.paid]
    investments_pendentes = [inv for inv in investments if not inv.paid]

    total_realizado = sum(inv.value for inv in investments_realizados)
    total_pendente = sum(inv.value for inv in investments_pendentes)
    total_geral = sum(inv.value for inv in investments)

    col1, col2, col3 = st.columns(3)

    with col1:
        total_realizado_fmt = f"R$ {total_realizado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.markdown(
            f"""
            <div style="border: 3px solid #10B981; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #047857; font-weight: 600;">REALIZADOS</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #10B981;">{total_realizado_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #047857;">{len(investments_realizados)} investimento(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        total_pendente_fmt = f"R$ {total_pendente:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.markdown(
            f"""
            <div style="border: 3px solid #F59E0B; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #92400E; font-weight: 600;">PENDENTES</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #F59E0B;">{total_pendente_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #92400E;">{len(investments_pendentes)} investimento(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        total_geral_fmt = f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.markdown(
            f"""
            <div style="border: 3px solid #9333EA; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #6b21a8; font-weight: 600;">TOTAL</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #9333EA;">{total_geral_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #6b21a8;">{len(investments)} investimento(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_investments_table(investments, account_use_cases):
    """Renderiza tabela de investimentos com data_editor agrupada por mês"""
    if not investments:
        st.info("Nenhum investimento encontrado no período selecionado.")
        return

    st.subheader("Lista de Investimentos por Mês", anchor=False)

    # Agrupar investimentos por mês
    investments_by_month = {}
    for investment in investments:
        month_key = investment.date.strftime("%Y-%m")
        month_label = investment.date.strftime("%b/%Y")

        if month_key not in investments_by_month:
            investments_by_month[month_key] = {
                "label": month_label,
                "investments": []
            }

        investments_by_month[month_key]["investments"].append(investment)

    # Ordenar meses (mais recente primeiro)
    sorted_months = sorted(investments_by_month.keys(), reverse=True)

    # Renderizar cada mês em um expander com data_editor
    for month_key in sorted_months:
        month_data = investments_by_month[month_key]
        month_investments = sorted(
            month_data["investments"], key=lambda x: x.date, reverse=True
        )

        # Calcular total do mês
        month_total = sum(inv.value for inv in month_investments)
        month_total_fmt = f"R$ {month_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        with st.expander(f"📅 {month_data['label']} - {month_total_fmt}", expanded=True):
            # Preparar dados para o data_editor
            table_data = []
            investment_map = {}  # Para mapear índices de volta aos IDs

            for idx, investment in enumerate(month_investments):
                value_str = (
                    f"R$ {investment.value:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
                table_data.append({
                    "Data": investment.date.strftime("%d/%m/%Y"),
                    "Descrição": investment.description,
                    "Valor": value_str,
                    "Realizado": investment.paid
                })
                investment_map[idx] = investment.id

            # Renderizar tabela editável
            edited_df = st.data_editor(
                table_data,
                use_container_width=True,
                hide_index=True,
                disabled=["Data", "Descrição", "Valor"],
                column_config={
                    "Data": st.column_config.TextColumn("Data", width="small"),
                    "Descrição": st.column_config.TextColumn(
                        "Descrição", width="medium"
                    ),
                    "Valor": st.column_config.TextColumn("Valor", width="small"),
                    "Realizado": st.column_config.CheckboxColumn("Realizado", width="small")
                },
                key=f"investments_table_{month_key}"
            )

            # Detectar mudanças e atualizar
            for idx, (original, edited) in enumerate(zip(table_data, edited_df)):
                if original["Realizado"] != edited["Realizado"]:
                    investment_id = investment_map[idx]
                    try:
                        account_use_cases.update_account(investment_id, paid=edited["Realizado"])
                        st.success(f"Status atualizado para: {edited['Descrição']}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar: {str(e)}")


@st.dialog("Novo Investimento")
def _render_cadastro_modal(account_use_cases):
    """Modal para cadastro de novo investimento"""
    st.write("Preencha os dados do investimento:")

    with st.form("form_novo_investimento"):
        data_investimento = st.date_input(
            "Data", value=datetime.now(), format="DD/MM/YYYY"
        )

        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f")

        descricao = st.text_input(
            "Descrição", placeholder="Ex: CDB, Tesouro Direto, Ações, etc."
        )

        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button(
                "Salvar", use_container_width=True, type="primary"
            )

        with col2:
            cancel = st.form_submit_button("Cancelar", use_container_width=True)

        if submit:
            if not descricao or not descricao.strip():
                st.error("Descrição é obrigatória!")
            elif valor <= 0:
                st.error("Valor deve ser maior que zero!")
            else:
                try:
                    date_datetime = datetime.combine(
                        data_investimento, datetime.min.time()
                    )
                    account_use_cases.create_account(
                        value=valor,
                        date=date_datetime,
                        description=descricao.strip(),
                        account_type="investment",
                    )
                    st.success("Investimento cadastrado com sucesso!")
                    st.session_state.show_investment_modal = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")

        if cancel:
            st.session_state.show_investment_modal = False
            st.rerun()


def _render_delete_section(investments, account_use_cases):
    """Renderiza seção de exclusão de investimentos"""
    if not investments:
        return

    st.subheader("Excluir Investimento", anchor=False)

    # Preparar lista de investimentos para seleção
    investment_options = []
    investment_map = {}

    for investment in sorted(investments, key=lambda x: x.date, reverse=True):
        value_str = f"R$ {investment.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        date_str = investment.date.strftime("%d/%m/%Y")
        status_str = "✅ Realizado" if investment.paid else "⏳ Pendente"

        option_label = f"{date_str} - {investment.description} - {value_str} - {status_str}"
        investment_options.append(option_label)
        investment_map[option_label] = investment.id

    investment_to_delete = st.selectbox(
        "Selecione o investimento para excluir",
        options=investment_options,
        key="delete_investment",
    )

    @st.dialog("Confirmar Exclusão")
    def confirm_delete_modal():
        st.write("Tem certeza que deseja excluir este investimento?")
        st.write(f"**{investment_to_delete}**")
        st.warning("⚠️ Esta ação não pode ser desfeita!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sim, excluir", type="primary", use_container_width=True):
                investment_id = investment_map[investment_to_delete]
                try:
                    account_use_cases.delete_account(investment_id)
                    st.success("Investimento excluído com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {str(e)}")

        with col2:
            if st.button("Cancelar", use_container_width=True):
                st.rerun()

    if st.button("Excluir", type="primary", use_container_width=True):
        confirm_delete_modal()
