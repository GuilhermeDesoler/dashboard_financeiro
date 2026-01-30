import streamlit as st
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components.page_header import render_page_header


def render():
    render_page_header("Boletos")

    container = get_container()
    account_use_cases = container.account_use_cases

    try:
        # Botão de lançamento isolado
        col1, col2, col3 = st.columns([3, 1, 1])

        with col3:
            if st.button("Lançamento", use_container_width=True, type="primary"):
                st.session_state.show_ticket_modal = True

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
                key="ticket_start",
            )

        with col2:
            st.date_input(
                "Data Fim",
                value=end_of_month,
                format="DD/MM/YYYY",
                key="ticket_end",
            )

        with col3:
            st.write("")
            st.write("")
            if st.button("Atualizar", use_container_width=True):
                st.rerun()

        start_datetime = datetime.combine(
            st.session_state.ticket_start, datetime.min.time()
        )
        end_datetime = datetime.combine(
            st.session_state.ticket_end, datetime.max.time()
        )

        # Buscar apenas boletos (type=boleto)
        all_accounts = account_use_cases.list_accounts(start_datetime, end_datetime)
        boletos = [acc for acc in all_accounts if acc.type == "boleto"]

        st.divider()

        # Cards de resumo
        _render_cards_resumo(boletos, today)

        st.divider()

        # Tabela de boletos
        _render_boletos_table(boletos, account_use_cases)

        st.divider()

        # Seção de exclusão
        _render_delete_section(boletos, account_use_cases)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        import traceback

        st.code(traceback.format_exc())

    # Modal de cadastro
    if st.session_state.get("show_ticket_modal", False):
        _render_cadastro_modal(account_use_cases)

    # Modal de edição inline
    if st.session_state.get("show_edit_boleto_modal", False):
        _render_edit_modal(account_use_cases)

    # Modal de exclusão inline
    if st.session_state.get("show_delete_boleto_modal", False):
        _render_delete_modal(account_use_cases)


def _render_cards_resumo(boletos, today):
    """Renderiza cards de resumo"""
    # A pagar: não pagos com data <= hoje
    boletos_a_pagar = [b for b in boletos if not b.paid and b.date.date() <= today.date()]
    total_a_pagar = sum(b.value for b in boletos_a_pagar)

    # A vencer: não pagos com data > hoje
    boletos_a_vencer = [b for b in boletos if not b.paid and b.date.date() > today.date()]
    total_a_vencer = sum(b.value for b in boletos_a_vencer)

    # Total pago: todos pagos
    boletos_pagos = [b for b in boletos if b.paid]
    total_pago = sum(b.value for b in boletos_pagos)

    # Total geral
    total_geral = sum(b.value for b in boletos)

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
                <p style="margin: 0; font-size: 12px; color: #991B1B;">{len(boletos_a_pagar)} boleto(s)</p>
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
                <p style="margin: 0; font-size: 12px; color: #374151;">{len(boletos_a_vencer)} boleto(s)</p>
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
                <p style="margin: 0; font-size: 12px; color: #047857;">{len(boletos_pagos)} boleto(s)</p>
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
                <p style="margin: 0; font-size: 12px; color: #92400E;">{len(boletos)} boleto(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_boletos_table(boletos, account_use_cases):
    """Renderiza tabela de boletos com data_editor agrupada por mês"""
    if not boletos:
        st.info("Nenhum boleto encontrado no período selecionado.")
        return

    st.subheader("Lista de Boletos por Mês", anchor=False)

    # Agrupar boletos por mês
    boletos_by_month = {}
    for boleto in boletos:
        month_key = boleto.date.strftime("%Y-%m")
        month_label = boleto.date.strftime("%b/%Y")

        if month_key not in boletos_by_month:
            boletos_by_month[month_key] = {"label": month_label, "boletos": []}

        boletos_by_month[month_key]["boletos"].append(boleto)

    # Ordenar meses (mais antigo primeiro - ordem crescente)
    sorted_months = sorted(boletos_by_month.keys(), reverse=False)

    # Renderizar cada mês em um expander com data_editor
    for month_key in sorted_months:
        month_data = boletos_by_month[month_key]
        month_boletos = sorted(
            month_data["boletos"], key=lambda x: x.date, reverse=False
        )

        # Calcular total do mês
        month_total = sum(bol.value for bol in month_boletos)
        month_total_fmt = f"R$ {month_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        with st.expander(f"📅 {month_data['label']} - {month_total_fmt}", expanded=True):
            # Configuração de paginação
            items_per_page = 10
            page_key = f"boleto_page_{month_key}"

            # Inicializar página no session_state
            if page_key not in st.session_state:
                st.session_state[page_key] = 0

            total_items = len(month_boletos)
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
            for boleto in month_boletos[start_idx:end_idx]:
                _render_boleto_row(boleto, account_use_cases)

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


def _render_boleto_row(boleto, account_use_cases):
    """Renderiza uma linha de boleto com checkbox e botões de ação"""
    col1, col2, col3, col4, col5 = st.columns([0.5, 1.8, 3.5, 2, 1])

    with col1:
        # Botão de delete
        if st.button("🗑️", key=f"delete_btn_boleto_{boleto.id}", help="Excluir boleto"):
            st.session_state.delete_boleto_id = boleto.id
            st.session_state.show_delete_boleto_modal = True
            st.rerun()

    with col2:
        st.text(boleto.date.strftime("%d/%m/%Y"))

    with col3:
        st.text(boleto.description)

    with col4:
        # Valor editável inline
        value_key = f"boleto_value_{boleto.id}"
        value_sync_key = f"boleto_value_sync_{boleto.id}"

        # Inicializar sync_key com valor do banco
        if value_sync_key not in st.session_state:
            st.session_state[value_sync_key] = float(boleto.value)

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
                account_use_cases.update_account(boleto.id, value=new_value)
                st.session_state[value_sync_key] = new_value
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {str(e)}")

    with col5:
        checkbox_key = f"boleto_paid_{boleto.id}"
        sync_key = f"boleto_sync_{boleto.id}"

        # Inicializar sync_key com valor do banco (só na primeira vez)
        if sync_key not in st.session_state:
            st.session_state[sync_key] = boleto.paid

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
                account_use_cases.update_account(boleto.id, paid=new_paid)
                st.session_state[sync_key] = new_paid
            except Exception as e:
                st.error(f"Erro: {str(e)}")


@st.dialog("Novo Boleto")
def _render_cadastro_modal(account_use_cases):
    """Modal para cadastro de novo boleto"""
    st.write("Preencha os dados do boleto:")

    with st.form("form_novo_boleto"):
        data_boleto = st.date_input(
            "Data de Vencimento", value=datetime.now(), format="DD/MM/YYYY"
        )

        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f")

        descricao = st.text_input(
            "Descrição", placeholder="Ex: Conta de Luz, Água, Internet, etc."
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
                    date_datetime = datetime.combine(data_boleto, datetime.min.time())
                    account_use_cases.create_account(
                        value=valor,
                        date=date_datetime,
                        description=descricao.strip(),
                        account_type="boleto",
                    )
                    st.success("Boleto cadastrado com sucesso!")
                    st.session_state.show_ticket_modal = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")

        if cancel:
            st.session_state.show_ticket_modal = False
            st.rerun()


@st.dialog("Editar Boleto")
def _render_edit_modal(account_use_cases):
    """Modal para edição de boleto"""
    boleto_id = st.session_state.get("edit_boleto_id")
    if not boleto_id:
        st.session_state.show_edit_boleto_modal = False
        st.rerun()
        return

    try:
        # Buscar boleto
        all_accounts = account_use_cases.list_accounts(None, None)
        boleto = next((acc for acc in all_accounts if acc.id == boleto_id and acc.type == "boleto"), None)

        if not boleto:
            st.error("Boleto não encontrado!")
            st.session_state.show_edit_boleto_modal = False
            st.rerun()
            return

        st.write("Editar dados do boleto:")

        with st.form("form_edit_boleto"):
            data_boleto = st.date_input("Data", value=boleto.date.date(), format="DD/MM/YYYY")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f", value=float(boleto.value))
            descricao = st.text_input("Descrição", value=boleto.description)
            pago = st.checkbox("Pago", value=boleto.paid)

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
                        date_datetime = datetime.combine(data_boleto, datetime.min.time())
                        account_use_cases.update_account(
                            boleto_id,
                            value=valor,
                            date=date_datetime,
                            description=descricao.strip(),
                            paid=pago
                        )
                        st.success("Boleto atualizado com sucesso!")
                        st.session_state.show_edit_boleto_modal = False
                        del st.session_state.edit_boleto_id
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar: {str(e)}")

            if cancel:
                st.session_state.show_edit_boleto_modal = False
                del st.session_state.edit_boleto_id
                st.rerun()

    except Exception as e:
        st.error(f"Erro ao carregar boleto: {str(e)}")
        st.session_state.show_edit_boleto_modal = False
        st.rerun()


@st.dialog("Confirmar Exclusão")
def _render_delete_modal(account_use_cases):
    """Modal para confirmação de exclusão"""
    boleto_id = st.session_state.get("delete_boleto_id")
    if not boleto_id:
        st.session_state.show_delete_boleto_modal = False
        st.rerun()
        return

    try:
        # Buscar boleto
        all_accounts = account_use_cases.list_accounts(None, None)
        boleto = next((acc for acc in all_accounts if acc.id == boleto_id and acc.type == "boleto"), None)

        if not boleto:
            st.error("Boleto não encontrado!")
            st.session_state.show_delete_boleto_modal = False
            st.rerun()
            return

        value_str = f"R$ {boleto.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        date_str = boleto.date.strftime("%d/%m/%Y")

        st.write("Tem certeza que deseja excluir este boleto?")
        st.write(f"**{date_str} - {boleto.description} - {value_str}**")
        st.warning("⚠️ Esta ação não pode ser desfeita!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sim, excluir", type="primary", use_container_width=True):
                try:
                    account_use_cases.delete_account(boleto_id)
                    st.success("Boleto excluído com sucesso!")
                    st.session_state.show_delete_boleto_modal = False
                    del st.session_state.delete_boleto_id
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {str(e)}")

        with col2:
            if st.button("Cancelar", use_container_width=True):
                st.session_state.show_delete_boleto_modal = False
                del st.session_state.delete_boleto_id
                st.rerun()

    except Exception as e:
        st.error(f"Erro: {str(e)}")
        st.session_state.show_delete_boleto_modal = False
        st.rerun()


def _render_delete_section(boletos, account_use_cases):
    """Renderiza seção de exclusão de boletos"""
    if not boletos:
        return

    st.subheader("Excluir Boleto", anchor=False)

    # Preparar lista de boletos para seleção
    boleto_options = []
    boleto_map = {}

    # Ordenar por data decrescente (mais recentes primeiro no select)
    for boleto in sorted(boletos, key=lambda x: x.date, reverse=True):
        value_str = f"R$ {boleto.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        date_str = boleto.date.strftime("%d/%m/%Y")
        status_str = "✅ Pago" if boleto.paid else "⏳ Pendente"

        option_label = f"{date_str} - {boleto.description} - {value_str} - {status_str}"
        boleto_options.append(option_label)
        boleto_map[option_label] = boleto.id

    boleto_to_delete = st.selectbox(
        "Selecione o boleto para excluir",
        options=boleto_options,
        key="delete_boleto",
    )

    @st.dialog("Confirmar Exclusão")
    def confirm_delete_modal():
        st.write("Tem certeza que deseja excluir este boleto?")
        st.write(f"**{boleto_to_delete}**")
        st.warning("⚠️ Esta ação não pode ser desfeita!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sim, excluir", type="primary", use_container_width=True):
                boleto_id = boleto_map[boleto_to_delete]
                try:
                    account_use_cases.delete_account(boleto_id)
                    st.success("Boleto excluído com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {str(e)}")

        with col2:
            if st.button("Cancelar", use_container_width=True):
                st.rerun()

    if st.button("Excluir", type="primary", use_container_width=True):
        confirm_delete_modal()
