import streamlit as st
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components.company_header import render_company_header


def render():
    render_company_header("Despesas")

    container = get_container()
    account_use_cases = container.account_use_cases

    try:
        # Botão de lançamento isolado
        col1, col2, col3 = st.columns([3, 1, 1])

        with col3:
            if st.button("Lançamento", use_container_width=True, type="primary"):
                st.session_state.show_expense_modal = True

        # Filtros de data
        col1, col2, col3 = st.columns([2, 2, 1])

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
                key="expenses_start",
            )

        with col2:
            st.date_input(
                "Data Fim",
                value=end_of_month,
                format="DD/MM/YYYY",
                key="expenses_end",
            )

        with col3:
            st.write("")
            st.write("")
            if st.button("Atualizar", use_container_width=True):
                st.rerun()

        start_datetime = datetime.combine(
            st.session_state.expenses_start, datetime.min.time()
        )
        end_datetime = datetime.combine(
            st.session_state.expenses_end, datetime.max.time()
        )

        # Buscar apenas despesas (type=payment)
        all_accounts = account_use_cases.list_accounts(start_datetime, end_datetime)
        expenses = [acc for acc in all_accounts if acc.type == "payment"]

        st.divider()

        # Cards de resumo
        _render_cards_resumo(expenses, today)

        st.divider()

        # Tabela de despesas agrupadas por mês
        _render_expenses_table(expenses, account_use_cases)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        import traceback

        st.code(traceback.format_exc())

    # Modal de cadastro
    if st.session_state.get("show_expense_modal", False):
        _render_cadastro_modal(account_use_cases)


def _render_cards_resumo(expenses, today):
    """Renderiza cards de resumo"""
    expenses_pagas = [exp for exp in expenses if exp.paid]
    total_pago = sum(exp.value for exp in expenses_pagas)
    total_geral = sum(exp.value for exp in expenses)

    expenses_hoje = [
        exp for exp in expenses if not exp.paid and exp.date.date() == today.date()
    ]
    total_hoje = sum(exp.value for exp in expenses_hoje)

    col1, col2, col3 = st.columns(3)

    with col1:
        total_hoje_fmt = (
            f"R$ {total_hoje:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        st.markdown(
            f"""
            <div style="border: 3px solid #DC2626; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #991B1B; font-weight: 600;">A PAGAR HOJE</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #DC2626;">{total_hoje_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #991B1B;">{len(expenses_hoje)} despesa(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        total_pago_fmt = (
            f"R$ {total_pago:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        st.markdown(
            f"""
            <div style="border: 3px solid #10B981; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #047857; font-weight: 600;">JÁ PAGAS</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #10B981;">{total_pago_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #047857;">{len(expenses_pagas)} despesa(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        total_geral_fmt = (
            f"R$ {total_geral:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        st.markdown(
            f"""
            <div style="border: 3px solid #9333EA; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #6b21a8; font-weight: 600;">TOTAL</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #9333EA;">{total_geral_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #6b21a8;">{len(expenses)} despesa(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_expenses_table(expenses, account_use_cases):
    """Renderiza tabela de despesas com data_editor agrupada por mês"""
    if not expenses:
        st.info("Nenhuma despesa encontrada no período selecionado.")
        return

    st.subheader("Lista de Despesas por Mês", anchor=False)

    # Agrupar despesas por mês
    expenses_by_month = {}
    for expense in expenses:
        month_key = expense.date.strftime("%Y-%m")
        month_label = expense.date.strftime("%b/%Y")

        if month_key not in expenses_by_month:
            expenses_by_month[month_key] = {"label": month_label, "expenses": []}

        expenses_by_month[month_key]["expenses"].append(expense)

    # Ordenar meses (mais recente primeiro)
    sorted_months = sorted(expenses_by_month.keys(), reverse=True)

    # Renderizar cada mês em um expander com data_editor
    for month_key in sorted_months:
        month_data = expenses_by_month[month_key]
        month_expenses = sorted(
            month_data["expenses"], key=lambda x: x.date, reverse=True
        )

        with st.expander(f"📅 {month_data['label']}", expanded=True):
            # Preparar dados para o data_editor
            table_data = []
            expense_map = {}  # Para mapear índices de volta aos IDs

            for idx, expense in enumerate(month_expenses):
                value_str = (
                    f"R$ {expense.value:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
                table_data.append(
                    {
                        "Data": expense.date.strftime("%d/%m/%Y"),
                        "Descrição": expense.description,
                        "Valor": value_str,
                        "Pago": expense.paid,
                    }
                )
                expense_map[idx] = expense.id

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
                    "Pago": st.column_config.CheckboxColumn("Pago", width="small"),
                },
                key=f"expenses_table_{month_key}",
            )

            # Detectar mudanças e atualizar
            for idx, (original, edited) in enumerate(zip(table_data, edited_df)):
                if original["Pago"] != edited["Pago"]:
                    expense_id = expense_map[idx]
                    try:
                        account_use_cases.update_account(
                            expense_id, paid=edited["Pago"]
                        )
                        st.success(f"Status atualizado para: {edited['Descrição']}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar: {str(e)}")


@st.dialog("Nova Despesa")
def _render_cadastro_modal(account_use_cases):
    """Modal para cadastro de nova despesa"""
    st.write("Preencha os dados da despesa:")

    with st.form("form_nova_despesa"):
        data_despesa = st.date_input("Data", value=datetime.now(), format="DD/MM/YYYY")

        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f")

        descricao = st.text_input(
            "Descrição", placeholder="Ex: Combustível, Alimentação, etc."
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
                    date_datetime = datetime.combine(data_despesa, datetime.min.time())
                    account_use_cases.create_account(
                        value=valor,
                        date=date_datetime,
                        description=descricao.strip(),
                        account_type="payment",
                    )
                    st.success("Despesa cadastrada com sucesso!")
                    st.session_state.show_expense_modal = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")

        if cancel:
            st.session_state.show_expense_modal = False
            st.rerun()
