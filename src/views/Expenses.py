import streamlit as st
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components.page_header import render_page_header


def render():
    render_page_header("Despesas")

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

        st.divider()

        # Seção de exclusão
        _render_delete_section(expenses, account_use_cases)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        import traceback

        st.code(traceback.format_exc())

    # Modal de cadastro
    if st.session_state.get("show_expense_modal", False):
        _render_cadastro_modal(account_use_cases)

    # Modal de edição inline
    if st.session_state.get("show_edit_expense_modal", False):
        _render_edit_modal(account_use_cases)

    # Modal de exclusão inline
    if st.session_state.get("show_delete_expense_modal", False):
        _render_delete_modal(account_use_cases)


def _render_cards_resumo(expenses, today):
    """Renderiza cards de resumo"""
    # A pagar: não pagas com data <= hoje
    expenses_a_pagar = [exp for exp in expenses if not exp.paid and exp.date.date() <= today.date()]
    total_a_pagar = sum(exp.value for exp in expenses_a_pagar)

    # A vencer: não pagas com data > hoje
    expenses_a_vencer = [exp for exp in expenses if not exp.paid and exp.date.date() > today.date()]
    total_a_vencer = sum(exp.value for exp in expenses_a_vencer)

    # Total pago: todas pagas
    expenses_pagas = [exp for exp in expenses if exp.paid]
    total_pago = sum(exp.value for exp in expenses_pagas)

    # Total geral
    total_geral = sum(exp.value for exp in expenses)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_a_pagar_fmt = (
            f"R$ {total_a_pagar:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        st.markdown(
            f"""
            <div style="border: 3px solid #DC2626; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #991B1B; font-weight: 600;">A PAGAR</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #DC2626;">{total_a_pagar_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #991B1B;">{len(expenses_a_pagar)} despesa(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        total_a_vencer_fmt = (
            f"R$ {total_a_vencer:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        st.markdown(
            f"""
            <div style="border: 3px solid #6B7280; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #374151; font-weight: 600;">A VENCER</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #6B7280;">{total_a_vencer_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #374151;">{len(expenses_a_vencer)} despesa(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        total_pago_fmt = (
            f"R$ {total_pago:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        st.markdown(
            f"""
            <div style="border: 3px solid #10B981; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #047857; font-weight: 600;">TOTAL PAGO</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #10B981;">{total_pago_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #047857;">{len(expenses_pagas)} despesa(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        total_geral_fmt = (
            f"R$ {total_geral:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        st.markdown(
            f"""
            <div style="border: 3px solid #F59E0B; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #92400E; font-weight: 600;">TOTAL</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #F59E0B;">{total_geral_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #92400E;">{len(expenses)} despesa(s)</p>
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

    # Ordenar meses (mais antigo primeiro - ordem crescente)
    sorted_months = sorted(expenses_by_month.keys(), reverse=False)

    # Renderizar cada mês em um expander com data_editor
    for month_key in sorted_months:
        month_data = expenses_by_month[month_key]
        month_expenses = sorted(
            month_data["expenses"], key=lambda x: x.date, reverse=False
        )

        # Calcular total do mês
        month_total = sum(exp.value for exp in month_expenses)
        month_total_fmt = f"R$ {month_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        with st.expander(f"📅 {month_data['label']} - {month_total_fmt}", expanded=True):
            # Configuração de paginação
            items_per_page = 10
            page_key = f"expense_page_{month_key}"

            # Inicializar página no session_state
            if page_key not in st.session_state:
                st.session_state[page_key] = 0

            total_items = len(month_expenses)
            total_pages = (total_items + items_per_page - 1) // items_per_page
            current_page = st.session_state[page_key]

            # Garantir que a página atual está dentro dos limites
            if current_page >= total_pages:
                current_page = max(0, total_pages - 1)
                st.session_state[page_key] = current_page

            # Calcular índices para a página atual
            start_idx = current_page * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)

            # Renderizar tabela com checkboxes individuais da página atual
            for expense in month_expenses[start_idx:end_idx]:
                _render_expense_row(expense, account_use_cases)

            # Controles de paginação
            if total_pages > 1:
                st.divider()
                col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

                with col1:
                    if st.button("⏮️ Primeira", key=f"first_{month_key}", disabled=current_page == 0, use_container_width=True):
                        st.session_state[page_key] = 0
                        st.rerun()

                with col2:
                    if st.button("◀️ Anterior", key=f"prev_{month_key}", disabled=current_page == 0, use_container_width=True):
                        st.session_state[page_key] = current_page - 1
                        st.rerun()

                with col3:
                    st.markdown(f"<div style='text-align: center; padding-top: 8px;'>Página {current_page + 1} de {total_pages} ({total_items} itens)</div>", unsafe_allow_html=True)

                with col4:
                    if st.button("Próxima ▶️", key=f"next_{month_key}", disabled=current_page >= total_pages - 1, use_container_width=True):
                        st.session_state[page_key] = current_page + 1
                        st.rerun()

                with col5:
                    if st.button("Última ⏭️", key=f"last_{month_key}", disabled=current_page >= total_pages - 1, use_container_width=True):
                        st.session_state[page_key] = total_pages - 1
                        st.rerun()


def _render_expense_row(expense, account_use_cases):
    """Renderiza uma linha de despesa com checkbox e botões de ação"""
    col1, col2, col3, col4, col5 = st.columns([0.5, 1.8, 3.5, 2, 1])

    with col1:
        # Botão de delete
        if st.button("🗑️", key=f"delete_btn_expense_{expense.id}", help="Excluir despesa"):
            st.session_state.delete_expense_id = expense.id
            st.session_state.show_delete_expense_modal = True
            st.rerun()

    with col2:
        st.text(expense.date.strftime("%d/%m/%Y"))

    with col3:
        st.text(expense.description)

    with col4:
        # Valor editável inline
        value_key = f"expense_value_{expense.id}"
        value_sync_key = f"expense_value_sync_{expense.id}"

        # Inicializar sync_key com valor do banco
        if value_sync_key not in st.session_state:
            st.session_state[value_sync_key] = float(expense.value)

        # Inicializar value_key
        if value_key not in st.session_state:
            st.session_state[value_key] = st.session_state[value_sync_key]

        new_value = st.number_input(
            "Valor",
            min_value=0.01,
            step=0.01,
            format="%.2f",
            key=value_key,
            label_visibility="collapsed"
        )

        # Atualizar banco quando valor muda
        if abs(new_value - st.session_state[value_sync_key]) > 0.001:
            try:
                account_use_cases.update_account(expense.id, value=new_value)
                st.session_state[value_sync_key] = new_value
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {str(e)}")

    with col5:
        checkbox_key = f"expense_paid_{expense.id}"
        sync_key = f"expense_sync_{expense.id}"

        # Inicializar sync_key com valor do banco (só na primeira vez)
        if sync_key not in st.session_state:
            st.session_state[sync_key] = expense.paid

        # Inicializar checkbox com valor sincronizado
        if checkbox_key not in st.session_state:
            st.session_state[checkbox_key] = st.session_state[sync_key]

        new_paid = st.checkbox(
            "Pago",
            key=checkbox_key,
            label_visibility="collapsed"
        )

        # Atualizar banco quando valor muda (comparar com sync_key)
        if new_paid != st.session_state[sync_key]:
            try:
                account_use_cases.update_account(expense.id, paid=new_paid)
                st.session_state[sync_key] = new_paid
            except Exception as e:
                st.error(f"Erro: {str(e)}")


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

        recorrencia = st.number_input(
            "Recorrência (meses)",
            min_value=1,
            value=1,
            step=1,
            help="Quantidade de meses para repetir esta despesa (1 = apenas este mês)"
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
                    account_use_cases.create_recurring_account(
                        value=valor,
                        date=date_datetime,
                        description=descricao.strip(),
                        account_type="payment",
                        recurrence=int(recorrencia),
                    )
                    if recorrencia > 1:
                        st.success(f"Despesa cadastrada para {int(recorrencia)} meses!")
                    else:
                        st.success("Despesa cadastrada com sucesso!")
                    st.session_state.show_expense_modal = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")

        if cancel:
            st.session_state.show_expense_modal = False
            st.rerun()


@st.dialog("Editar Despesa")
def _render_edit_modal(account_use_cases):
    """Modal para edição de despesa"""
    expense_id = st.session_state.get("edit_expense_id")
    if not expense_id:
        st.session_state.show_edit_expense_modal = False
        st.rerun()
        return

    try:
        # Buscar despesa
        all_accounts = account_use_cases.list_accounts(None, None)
        expense = next((acc for acc in all_accounts if acc.id == expense_id and acc.type == "payment"), None)

        if not expense:
            st.error("Despesa não encontrada!")
            st.session_state.show_edit_expense_modal = False
            st.rerun()
            return

        st.write("Editar dados da despesa:")

        with st.form("form_edit_despesa"):
            data_despesa = st.date_input("Data", value=expense.date.date(), format="DD/MM/YYYY")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f", value=float(expense.value))
            descricao = st.text_input("Descrição", value=expense.description)
            pago = st.checkbox("Pago", value=expense.paid)

            col1, col2 = st.columns(2)

            with col1:
                submit = st.form_submit_button("Salvar", use_container_width=True, type="primary")

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
                        account_use_cases.update_account(
                            expense_id,
                            value=valor,
                            date=date_datetime,
                            description=descricao.strip(),
                            paid=pago
                        )
                        st.success("Despesa atualizada com sucesso!")
                        st.session_state.show_edit_expense_modal = False
                        del st.session_state.edit_expense_id
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar: {str(e)}")

            if cancel:
                st.session_state.show_edit_expense_modal = False
                del st.session_state.edit_expense_id
                st.rerun()

    except Exception as e:
        st.error(f"Erro ao carregar despesa: {str(e)}")
        st.session_state.show_edit_expense_modal = False
        st.rerun()


@st.dialog("Confirmar Exclusão")
def _render_delete_modal(account_use_cases):
    """Modal para confirmação de exclusão"""
    expense_id = st.session_state.get("delete_expense_id")
    if not expense_id:
        st.session_state.show_delete_expense_modal = False
        st.rerun()
        return

    try:
        # Buscar despesa
        all_accounts = account_use_cases.list_accounts(None, None)
        expense = next((acc for acc in all_accounts if acc.id == expense_id and acc.type == "payment"), None)

        if not expense:
            st.error("Despesa não encontrada!")
            st.session_state.show_delete_expense_modal = False
            st.rerun()
            return

        value_str = f"R$ {expense.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        date_str = expense.date.strftime("%d/%m/%Y")

        st.write("Tem certeza que deseja excluir esta despesa?")
        st.write(f"**{date_str} - {expense.description} - {value_str}**")
        st.warning("⚠️ Esta ação não pode ser desfeita!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sim, excluir", type="primary", use_container_width=True):
                try:
                    account_use_cases.delete_account(expense_id)
                    st.success("Despesa excluída com sucesso!")
                    st.session_state.show_delete_expense_modal = False
                    del st.session_state.delete_expense_id
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {str(e)}")

        with col2:
            if st.button("Cancelar", use_container_width=True):
                st.session_state.show_delete_expense_modal = False
                del st.session_state.delete_expense_id
                st.rerun()

    except Exception as e:
        st.error(f"Erro: {str(e)}")
        st.session_state.show_delete_expense_modal = False
        st.rerun()


def _render_delete_section(expenses, account_use_cases):
    """Renderiza seção de exclusão de despesas"""
    if not expenses:
        return

    st.subheader("Excluir Despesa", anchor=False)

    # Preparar lista de despesas para seleção
    expense_options = []
    expense_map = {}

    # Ordenar por data decrescente (mais recentes primeiro no select)
    for expense in sorted(expenses, key=lambda x: x.date, reverse=True):
        value_str = f"R$ {expense.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        date_str = expense.date.strftime("%d/%m/%Y")
        status_str = "✅ Paga" if expense.paid else "⏳ Pendente"

        option_label = f"{date_str} - {expense.description} - {value_str} - {status_str}"
        expense_options.append(option_label)
        expense_map[option_label] = expense.id

    expense_to_delete = st.selectbox(
        "Selecione a despesa para excluir",
        options=expense_options,
        key="delete_expense",
    )

    @st.dialog("Confirmar Exclusão")
    def confirm_delete_modal():
        st.write("Tem certeza que deseja excluir esta despesa?")
        st.write(f"**{expense_to_delete}**")
        st.warning("⚠️ Esta ação não pode ser desfeita!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sim, excluir", type="primary", use_container_width=True):
                expense_id = expense_map[expense_to_delete]
                try:
                    account_use_cases.delete_account(expense_id)
                    st.success("Despesa excluída com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {str(e)}")

        with col2:
            if st.button("Cancelar", use_container_width=True):
                st.rerun()

    if st.button("Excluir", type="primary", use_container_width=True):
        confirm_delete_modal()
