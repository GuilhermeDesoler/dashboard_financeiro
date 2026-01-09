import streamlit as st
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components.company_header import render_company_header


def render():
    render_company_header("Boletos")

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

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        import traceback

        st.code(traceback.format_exc())

    # Modal de cadastro
    if st.session_state.get("show_ticket_modal", False):
        _render_cadastro_modal(account_use_cases)


def _render_cards_resumo(boletos, today):
    """Renderiza cards de resumo"""
    # Calcular boletos pagos e a pagar
    boletos_pagos = [b for b in boletos if b.paid]

    total_pago = sum(b.value for b in boletos_pagos)

    # Boletos a pagar hoje (incluindo final de semana se for segunda-feira)
    if today.weekday() == 0:  # Segunda-feira
        sabado = today - timedelta(days=2)
        domingo = today - timedelta(days=1)
        boletos_hoje = [
            b
            for b in boletos
            if not b.paid
            and (
                b.date.date() == today.date()
                or b.date.date() == sabado.date()
                or b.date.date() == domingo.date()
            )
        ]
    else:
        boletos_hoje = [
            b for b in boletos if not b.paid and b.date.date() == today.date()
        ]

    total_hoje = sum(b.value for b in boletos_hoje)

    col1, col2 = st.columns(2)

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
                <p style="margin: 0; font-size: 12px; color: #991B1B;">{len(boletos_hoje)} boleto(s)</p>
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
                <p style="margin: 0; font-size: 14px; color: #047857; font-weight: 600;">JÁ PAGOS</p>
                <h1 style="margin: 10px 0; font-size: 32px; color: #10B981;">{total_pago_fmt}</h1>
                <p style="margin: 0; font-size: 12px; color: #047857;">{len(boletos_pagos)} boleto(s)</p>
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

    # Ordenar meses (mais recente primeiro)
    sorted_months = sorted(boletos_by_month.keys(), reverse=True)

    # Renderizar cada mês em um expander com data_editor
    for month_key in sorted_months:
        month_data = boletos_by_month[month_key]
        month_boletos = sorted(
            month_data["boletos"], key=lambda x: x.date, reverse=True
        )

        with st.expander(f"📅 {month_data['label']}", expanded=True):
            # Preparar dados para o data_editor
            table_data = []
            boleto_map = {}  # Para mapear índices de volta aos IDs

            for idx, boleto in enumerate(month_boletos):
                value_str = (
                    f"R$ {boleto.value:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
                table_data.append(
                    {
                        "Data": boleto.date.strftime("%d/%m/%Y"),
                        "Descrição": boleto.description,
                        "Valor": value_str,
                        "Pago": boleto.paid,
                    }
                )
                boleto_map[idx] = boleto.id

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
                key=f"boletos_table_{month_key}",
            )

            # Detectar mudanças e atualizar
            for idx, (original, edited) in enumerate(zip(table_data, edited_df)):
                if original["Pago"] != edited["Pago"]:
                    boleto_id = boleto_map[idx]
                    try:
                        account_use_cases.update_account(boleto_id, paid=edited["Pago"])
                        st.success(f"Status atualizado para: {edited['Descrição']}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar: {str(e)}")


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
