import streamlit as st
import pandas as pd
from datetime import datetime
from dependencies import get_container
from presentation.components.page_header import render_page_header


def render():
    render_page_header("Saldos e Limites")

    container = get_container()

    try:
        # Renderizar seção de limites bancários
        _render_limites_bancarios(container)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.info(
            "Verifique se a URL da API está configurada corretamente no arquivo .env"
        )


def _render_limites_bancarios(container):
    """Renderiza a seção de Limites Bancários com tabela editável"""
    st.subheader("📊 Limites Bancários", anchor=False)

    # Buscar limites existentes
    bank_limit_use_cases = container.bank_limit_use_cases

    try:
        bank_limits = bank_limit_use_cases.list_bank_limits()
    except Exception as e:
        st.error(f"Erro ao carregar limites: {str(e)}")
        bank_limits = []

    # Botões de ação
    col1, col2 = st.columns([3, 1])

    with col2:
        if st.button("➕ Adicionar Banco", use_container_width=True, type="primary"):
            st.session_state.adding_new_bank = True

    st.divider()

    # Tabela com scroll horizontal
    if bank_limits:
        # Calcular totais
        total_rotativo_available = sum(limit.rotativo_available for limit in bank_limits)
        total_rotativo_used = sum(limit.rotativo_used for limit in bank_limits)
        total_cheque_available = sum(limit.cheque_available for limit in bank_limits)
        total_cheque_used = sum(limit.cheque_used for limit in bank_limits)

        html_content = """
        <style>
        .bank-limits-container {
            overflow-x: auto;
            margin: 20px 0;
        }
        .bank-limits-container::-webkit-scrollbar {
            height: 12px;
        }
        .bank-limits-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        .bank-limits-container::-webkit-scrollbar-thumb {
            background: #9333EA;
            border-radius: 10px;
        }
        .bank-limits-container::-webkit-scrollbar-thumb:hover {
            background: #7c2cc9;
        }
        .bank-limits-table {
            width: 100%;
            border-collapse: collapse;
            min-width: 1000px;
        }
        .bank-limits-table th {
            background-color: #9333EA;
            color: white;
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd;
            font-weight: bold;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        .bank-limits-table td {
            padding: 10px;
            border: 1px solid #ddd;
            background-color: white;
            text-align: center;
        }
        .bank-limits-table tr:hover {
            background-color: #f5f5f5;
        }
        .bank-limits-table .bank-col {
            text-align: left;
            font-weight: bold;
        }
        .bank-limits-table .total-row {
            background-color: #e6e6fa !important;
            font-weight: bold;
        }
        .green-bg {
            background-color: #d4edda !important;
        }
        .red-bg {
            background-color: #f8d7da !important;
        }
        </style>
        <div class='bank-limits-container'>
        <table class='bank-limits-table'>
        <thead>
            <tr>
                <th rowspan="2">Banco</th>
                <th colspan="2" style="background-color: #28a745;">Rotativo</th>
                <th colspan="2" style="background-color: #dc3545;">Cheque Especial</th>
            </tr>
            <tr>
                <th style="background-color: #28a745;">Disponível</th>
                <th style="background-color: #28a745;">Em Uso</th>
                <th style="background-color: #dc3545;">Disponível</th>
                <th style="background-color: #dc3545;">Em Uso</th>
            </tr>
        </thead>
        <tbody>
        """

        # Renderizar linhas dos bancos
        for limit in bank_limits:
            rotativo_available_fmt = f"R$ {limit.rotativo_available:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            rotativo_used_fmt = f"R$ {limit.rotativo_used:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            cheque_available_fmt = f"R$ {limit.cheque_available:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            cheque_used_fmt = f"R$ {limit.cheque_used:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            html_content += f"<tr><td class='bank-col'>{limit.bank_name}</td><td class='green-bg'>{rotativo_available_fmt}</td><td>{rotativo_used_fmt}</td><td class='red-bg'>{cheque_available_fmt}</td><td>{cheque_used_fmt}</td></tr>"

        # Linha de total
        total_rot_avail = f"R$ {total_rotativo_available:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_rot_used = f"R$ {total_rotativo_used:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_cheq_avail = f"R$ {total_cheque_available:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_cheq_used = f"R$ {total_cheque_used:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        html_content += f"<tr class='total-row'><td class='bank-col'>Total</td><td class='green-bg'>{total_rot_avail}</td><td>{total_rot_used}</td><td class='red-bg'>{total_cheq_avail}</td><td>{total_cheq_used}</td></tr>"

        html_content += """
        </tbody>
        </table>
        </div>
        """

        st.markdown(html_content, unsafe_allow_html=True)

        st.divider()

    else:
        st.info("Nenhum limite bancário cadastrado. Clique em 'Adicionar Banco' para começar.")

    # Seção de edição/criação
    st.subheader("Editar / Adicionar Banco", anchor=False)

    with st.container(border=True):
        # Seletor para editar ou criar novo
        options = ["-- Criar Novo --"] + [f"{limit.bank_name}" for limit in bank_limits]
        selected_option = st.selectbox(
            "Selecione um banco para editar ou crie um novo",
            options=options,
            key="bank_limit_selector"
        )

        # Determinar se é edição ou criação
        is_editing = selected_option != "-- Criar Novo --"
        selected_limit = None

        if is_editing:
            selected_limit = next((l for l in bank_limits if l.bank_name == selected_option), None)

        # Formulário
        bank_name = st.text_input(
            "Nome do Banco",
            value=selected_limit.bank_name if selected_limit else "",
            placeholder="Ex: Sicredi, Sicoob, etc.",
            key="bank_name_input"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Rotativo**")
            rotativo_available = st.number_input(
                "Disponível (R$)",
                min_value=0.0,
                value=float(selected_limit.rotativo_available) if selected_limit else 0.0,
                step=1000.00,
                format="%.2f",
                key="rotativo_available_input"
            )

            rotativo_used = st.number_input(
                "Em Uso (R$)",
                min_value=0.0,
                value=float(selected_limit.rotativo_used) if selected_limit else 0.0,
                step=1000.00,
                format="%.2f",
                key="rotativo_used_input"
            )

        with col2:
            st.markdown("**Cheque Especial**")
            cheque_available = st.number_input(
                "Disponível (R$)",
                min_value=0.0,
                value=float(selected_limit.cheque_available) if selected_limit else 0.0,
                step=1000.00,
                format="%.2f",
                key="cheque_available_input"
            )

            cheque_used = st.number_input(
                "Em Uso (R$)",
                min_value=0.0,
                value=float(selected_limit.cheque_used) if selected_limit else 0.0,
                step=1000.00,
                format="%.2f",
                key="cheque_used_input"
            )

        # Botões de ação
        col_save, col_delete = st.columns(2)

        with col_save:
            button_label = "Atualizar" if is_editing else "Salvar"
            if st.button(button_label, type="primary", use_container_width=True):
                try:
                    if is_editing and selected_limit:
                        # Atualizar
                        bank_limit_use_cases.update_bank_limit(
                            selected_limit.id,
                            bank_name,
                            rotativo_available,
                            rotativo_used,
                            cheque_available,
                            cheque_used
                        )
                        st.success("Limite atualizado com sucesso!")
                    else:
                        # Criar novo
                        bank_limit_use_cases.create_bank_limit(
                            bank_name,
                            rotativo_available,
                            rotativo_used,
                            cheque_available,
                            cheque_used
                        )
                        st.success("Banco adicionado com sucesso!")
                        st.session_state.adding_new_bank = False

                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")

        with col_delete:
            if is_editing and selected_limit:
                if st.button("🗑️ Excluir", use_container_width=True):
                    try:
                        bank_limit_use_cases.delete_bank_limit(selected_limit.id)
                        st.success("Banco excluído com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir: {str(e)}")
