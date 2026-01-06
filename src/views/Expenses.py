import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components.page_header import render_page_header


# Cores por tipo de conta
ACCOUNT_TYPE_COLORS = {
    "boleto": "#DC2626",  # Vermelho
    "payment": "#F59E0B",  # Laranja/Amarelo
    "investment": "#10B981",  # Verde
}

ACCOUNT_TYPE_LABELS = {
    "boleto": "Boleto",
    "payment": "Pagamento de Boleto",
    "investment": "Investimento",
}


def _render_new_account_form(account_use_cases):
    """Renderiza o formulário para adicionar nova conta"""
    st.subheader("Adicionar Nova Entrada", anchor=False)

    with st.container(border=True):
        col_form1, col_form2 = st.columns(2)

        with col_form1:
            account_type = st.selectbox(
                "Tipo",
                options=["boleto", "payment", "investment"],
                format_func=lambda x: ACCOUNT_TYPE_LABELS.get(x, x) or x,
                key="account_type",
            )

            value = st.number_input(
                "Valor (R$)",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                key="account_value",
            )

        with col_form2:
            date_input = st.date_input(
                "Data",
                value=datetime.now(),
                format="DD/MM/YYYY",
                key="account_date",
            )

            description = st.text_input(
                "Descrição",
                placeholder="Ex: Conta de luz, Energia, etc.",
                key="account_description",
            )

        # Validação
        is_valid = True
        validation_errors = []

        if value <= 0:
            is_valid = False
            validation_errors.append("Valor deve ser maior que zero")

        if not description or not description.strip():
            is_valid = False
            validation_errors.append("Descrição é obrigatória")

        # Botão de salvar
        if st.button(
            "Salvar Entrada",
            use_container_width=True,
            type="primary",
            disabled=not is_valid,
            key="submit_account",
        ):
            try:
                date_datetime = datetime.combine(date_input, datetime.min.time())
                account_use_cases.create_account(
                    value=value,
                    date=date_datetime,
                    description=description.strip(),
                    account_type=account_type,
                )
                st.success("Entrada salva com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar entrada: {str(e)}")

        if validation_errors:
            for error in validation_errors:
                st.error(error)


def _render_accounts_table(account_use_cases, start_datetime, end_datetime):
    """Renderiza a tabela de contas agrupadas por mês (estilo crediário)"""
    accounts = account_use_cases.list_accounts(start_datetime, end_datetime)

    if not accounts:
        st.info("Nenhuma entrada encontrada no período selecionado.")
        return

    # Agrupar por mês e dia
    from collections import defaultdict

    monthly_data = defaultdict(lambda: defaultdict(list))

    for account in accounts:
        month_key = account.date.strftime("%m/%Y")
        day_number = account.date.day
        monthly_data[month_key][day_number].append(account)

    # Ordenar meses em ordem decrescente
    sorted_months = sorted(
        monthly_data.keys(), key=lambda m: datetime.strptime(m, "%m/%Y"), reverse=True
    )

    # Criar HTML da tabela
    html_content = """
    <style>
    .expenses-scroll-container {
        overflow-x: auto;
        margin: 20px 0;
    }
    .expenses-scroll-container::-webkit-scrollbar {
        height: 12px;
        width: 12px;
    }
    .expenses-scroll-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    .expenses-scroll-container::-webkit-scrollbar-thumb {
        background: #9333EA;
        border-radius: 10px;
    }
    .expenses-scroll-container::-webkit-scrollbar-thumb:hover {
        background: #7c2cc9;
    }
    .expenses-table {
        border-collapse: collapse;
    }
    .expenses-table th {
        background-color: #9333EA;
        color: white;
        padding: 8px 10px;
        text-align: center;
        border: 1px solid #ddd;
        font-weight: bold;
        font-size: 13px;
        position: sticky;
        top: 0;
        z-index: 10;
    }
    .expenses-table td {
        padding: 6px 8px;
        border: 1px solid #ddd;
        text-align: center;
        min-width: 150px;
        font-size: 12px;
        white-space: nowrap;
        vertical-align: top;
    }
    .expenses-table .day-label {
        background-color: #f0f0f0;
        font-weight: bold;
        min-width: 60px;
        font-size: 12px;
        position: sticky;
        left: 0;
        z-index: 5;
    }
    .expenses-entry {
        margin: 3px 0;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 11px;
        line-height: 1.3;
    }
    .boleto-entry {
        background-color: rgba(220, 38, 38, 0.15);
        color: #991B1B;
        font-weight: bold;
    }
    .payment-entry {
        background-color: rgba(245, 158, 11, 0.15);
        color: #92400E;
        font-weight: bold;
    }
    .investment-entry {
        background-color: rgba(16, 185, 129, 0.15);
        color: #065F46;
        font-weight: bold;
    }
    </style>
    <div class='expenses-scroll-container'>
    <table class='expenses-table'>
    """

    # Cabeçalho com os meses e totais
    html_content += "<thead><tr><th>Dia</th>"
    month_totals = {}

    for month in sorted_months:
        month_total = sum(
            account.value
            for day_accounts in monthly_data[month].values()
            for account in day_accounts
        )
        month_totals[month] = month_total

        header_label = f"{month}"
        html_content += f"<th>{header_label}</th>"

    html_content += "</tr></thead>"

    # Corpo da tabela - 31 linhas (dias)
    html_content += "<tbody>"
    for day in range(1, 32):
        html_content += f"<tr><td class='day-label'>Dia {day:02d}</td>"

        for month in sorted_months:
            day_accounts = monthly_data[month].get(day, [])

            if day_accounts:
                # Ordenar por valor (maior para menor)
                sorted_accounts = sorted(
                    day_accounts, key=lambda x: x.value, reverse=True
                )

                entries_html = ""
                for account in sorted_accounts:
                    type_class = f"{account.type}-entry"
                    label = ACCOUNT_TYPE_LABELS.get(account.type, account.type)
                    formatted_value = (
                        f"R$ {account.value:,.2f}".replace(",", "X")
                        .replace(".", ",")
                        .replace("X", ".")
                    )

                    entries_html += f"<div class='expenses-entry {type_class}'>"
                    entries_html += f"<strong>{formatted_value}</strong><br/>"
                    entries_html += f"<small>{label}</small><br/>"
                    entries_html += f"<small>{account.description}</small>"
                    entries_html += f"</div>"

                html_content += f"<td>{entries_html}</td>"
            else:
                html_content += "<td>-</td>"

        html_content += "</tr>"

    html_content += "</tbody></table></div>"

    st.markdown(html_content, unsafe_allow_html=True)


def render():
    render_page_header("Despesas / Investimentos")

    container = get_container()
    account_use_cases = container.account_use_cases

    try:
        # Abas principais
        tab1, tab2 = st.tabs(["Lançamentos", "Nova Entrada"])

        with tab1:
            # Filtros de data
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

            st.divider()

            # Tabela de contas
            _render_accounts_table(account_use_cases, start_datetime, end_datetime)

            # Seção de exclusão
            accounts = account_use_cases.list_accounts(start_datetime, end_datetime)

            if accounts:
                st.divider()

                # Preparar dados para o selectbox
                df_data = []
                for account in sorted(accounts, key=lambda x: x.date, reverse=True):
                    label = ACCOUNT_TYPE_LABELS.get(account.type, account.type)
                    formatted_value = (
                        f"R$ {account.value:,.2f}".replace(",", "X")
                        .replace(".", ",")
                        .replace("X", ".")
                    )
                    date_formatted = account.date.strftime("%d/%m/%Y")

                    df_data.append(
                        {
                            "Data": date_formatted,
                            "Tipo": label,
                            "Descrição": account.description,
                            "Valor": formatted_value,
                            "ID": account.id,
                        }
                    )

                st.subheader("Excluir Entrada", anchor=False)
                account_to_delete = st.selectbox(
                    "Selecione a entrada para excluir",
                    options=[
                        f"{e['Data']} - {e['Tipo']} - {e['Descrição']} - {e['Valor']}"
                        for e in df_data
                    ],
                    key="delete_account",
                )

                @st.dialog("Confirmar Exclusão")
                def confirm_delete_modal():
                    st.write("Tem certeza que deseja excluir esta entrada?")
                    st.write(f"**{account_to_delete}**")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(
                            "Sim, excluir", type="primary", use_container_width=True
                        ):
                            idx = [
                                f"{e['Data']} - {e['Tipo']} - {e['Descrição']} - {e['Valor']}"
                                for e in df_data
                            ].index(account_to_delete)
                            account_id = df_data[idx]["ID"]
                            try:
                                account_use_cases.delete_account(account_id)
                                st.success("Entrada excluída com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao excluir: {str(e)}")

                    with col2:
                        if st.button("Cancelar", use_container_width=True):
                            st.rerun()

                if st.button("Excluir", type="primary"):
                    confirm_delete_modal()

        with tab2:
            # Formulário para adicionar nova conta
            _render_new_account_form(account_use_cases)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.info(
            "Verifique se a URL da API está configurada corretamente no arquivo .env"
        )
