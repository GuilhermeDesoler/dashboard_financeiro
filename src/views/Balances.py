import streamlit as st
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

    # Buscar limites existentes
    bank_limit_use_cases = container.bank_limit_use_cases

    try:
        bank_limits = bank_limit_use_cases.list_bank_limits()
    except Exception as e:
        st.error(f"Erro ao carregar limites: {str(e)}")
        bank_limits = []

    # Botão para adicionar novo banco
    col1, col2, col3 = st.columns([3, 1, 1])

    with col3:
        if st.button("➕ Adicionar Banco", use_container_width=True, type="primary"):
            st.session_state.show_add_bank_modal = True

    # Renderizar cards de totais
    if bank_limits:
        # Calcular totais
        total_rotativo_available = sum(
            limit.rotativo_available for limit in bank_limits
        )
        total_rotativo_used = sum(limit.rotativo_used for limit in bank_limits)
        total_cheque_available = sum(limit.cheque_available for limit in bank_limits)
        total_cheque_used = sum(limit.cheque_used for limit in bank_limits)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_rot_avail_fmt = (
                f"R$ {total_rotativo_available:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.markdown(
                f"""
                <div style="border: 2px solid #28a745; border-radius: 8px; padding: 15px; background: #d4edda; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #155724; font-weight: 600;">ROTATIVO DISPONÍVEL</p>
                    <h2 style="margin: 5px 0; font-size: 24px; color: #28a745;">{total_rot_avail_fmt}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            total_rot_used_fmt = (
                f"R$ {total_rotativo_used:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.markdown(
                f"""
                <div style="border: 2px solid #6c757d; border-radius: 8px; padding: 15px; background: #e2e3e5; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #383d41; font-weight: 600;">ROTATIVO EM USO</p>
                    <h2 style="margin: 5px 0; font-size: 24px; color: #6c757d;">{total_rot_used_fmt}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            total_cheq_avail_fmt = (
                f"R$ {total_cheque_available:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.markdown(
                f"""
                <div style="border: 2px solid #dc3545; border-radius: 8px; padding: 15px; background: #f8d7da; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #721c24; font-weight: 600;">CHEQUE DISPONÍVEL</p>
                    <h2 style="margin: 5px 0; font-size: 24px; color: #dc3545;">{total_cheq_avail_fmt}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col4:
            total_cheq_used_fmt = (
                f"R$ {total_cheque_used:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.markdown(
                f"""
                <div style="border: 2px solid #6c757d; border-radius: 8px; padding: 15px; background: #e2e3e5; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #383d41; font-weight: 600;">CHEQUE EM USO</p>
                    <h2 style="margin: 5px 0; font-size: 24px; color: #6c757d;">{total_cheq_used_fmt}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        # Preparar dados para o data_editor
        table_data = []
        bank_map = {}  # Para mapear índices de volta aos IDs

        for idx, limit in enumerate(bank_limits):
            table_data.append(
                {
                    "Banco": limit.bank_name,
                    "Rotativo Disponível": limit.rotativo_available,
                    "Rotativo Em Uso": limit.rotativo_used,
                    "Taxa Rotativo (%)": limit.rotativo_rate,
                    "Cheque Disponível": limit.cheque_available,
                    "Cheque Em Uso": limit.cheque_used,
                    "Taxa Cheque (%)": limit.cheque_rate,
                }
            )
            bank_map[idx] = limit.id

        # Renderizar tabela editável
        edited_df = st.data_editor(
            table_data,
            use_container_width=True,
            hide_index=True,
            disabled=["Banco"],  # Nome do banco não pode ser editado
            column_config={
                "Banco": st.column_config.TextColumn("Banco", width="medium"),
                "Rotativo Disponível": st.column_config.NumberColumn(
                    "Rotativo Disponível",
                    width="small",
                    format="R$ %.2f",
                    min_value=0.0,
                    step=1000.0,
                ),
                "Rotativo Em Uso": st.column_config.NumberColumn(
                    "Rotativo Em Uso",
                    width="small",
                    format="R$ %.2f",
                    min_value=0.0,
                    step=100.0,
                ),
                "Taxa Rotativo (%)": st.column_config.NumberColumn(
                    "Taxa Rotativo (%)",
                    width="small",
                    format="%.2f%%",
                    min_value=0.0,
                    step=0.1,
                ),
                "Cheque Disponível": st.column_config.NumberColumn(
                    "Cheque Disponível",
                    width="small",
                    format="R$ %.2f",
                    min_value=0.0,
                    step=1000.0,
                ),
                "Cheque Em Uso": st.column_config.NumberColumn(
                    "Cheque Em Uso",
                    width="small",
                    format="R$ %.2f",
                    min_value=0.0,
                    step=100.0,
                ),
                "Taxa Cheque (%)": st.column_config.NumberColumn(
                    "Taxa Cheque (%)",
                    width="small",
                    format="%.2f%%",
                    min_value=0.0,
                    step=0.1,
                ),
            },
            key="bank_limits_table",
        )

        # Detectar mudanças e atualizar
        # Converter edited_df para lista de dicts (se necessário)
        if hasattr(edited_df, "to_dict"):
            edited_data = edited_df.to_dict("records")
        else:
            edited_data = edited_df

        for idx, (original, edited) in enumerate(zip(table_data, edited_data)):
            # Comparar apenas os campos editáveis
            campos_editaveis = [
                "Rotativo Disponível",
                "Rotativo Em Uso",
                "Taxa Rotativo (%)",
                "Cheque Disponível",
                "Cheque Em Uso",
                "Taxa Cheque (%)",
            ]

            mudou = any(original[campo] != edited[campo] for campo in campos_editaveis)

            if mudou:
                bank_id = bank_map.get(idx)

                if not bank_id:
                    st.error(f"Erro: ID do banco não encontrado para índice {idx}")
                    continue

                try:
                    bank_limit_use_cases.update_bank_limit(
                        bank_id,
                        edited["Banco"],
                        edited["Rotativo Disponível"],
                        edited["Rotativo Em Uso"],
                        edited["Cheque Disponível"],
                        edited["Cheque Em Uso"],
                        edited["Taxa Rotativo (%)"],
                        edited["Taxa Cheque (%)"],
                        0.0,  # interest_rate mantido para compatibilidade
                    )
                    st.success(f"Banco '{edited['Banco']}' atualizado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar: {str(e)}")

    else:
        st.info(
            "Nenhum limite bancário cadastrado. Clique em 'Adicionar Banco' para começar."
        )

    # Modal de cadastro
    if st.session_state.get("show_add_bank_modal", False):
        _render_add_bank_modal(bank_limit_use_cases)


@st.dialog("Adicionar Novo Banco")
def _render_add_bank_modal(bank_limit_use_cases):
    """Modal para cadastro de novo banco"""
    st.write("Preencha as informações do banco:")

    with st.form("form_novo_banco"):
        bank_name = st.text_input(
            "Nome do Banco", placeholder="Ex: Sicredi, Sicoob, Banco do Brasil, etc."
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Rotativo**")
            rotativo_available = st.number_input(
                "Disponível (R$)",
                min_value=0.0,
                step=1000.00,
                format="%.2f",
                key="modal_rotativo_available",
            )

            rotativo_used = st.number_input(
                "Em Uso (R$)",
                min_value=0.0,
                step=100.00,
                format="%.2f",
                key="modal_rotativo_used",
            )

            rotativo_rate = st.number_input(
                "Taxa (%)",
                min_value=0.0,
                step=0.1,
                format="%.2f",
                key="modal_rotativo_rate",
            )

        with col2:
            st.markdown("**Cheque Especial**")
            cheque_available = st.number_input(
                "Disponível (R$)",
                min_value=0.0,
                step=1000.00,
                format="%.2f",
                key="modal_cheque_available",
            )

            cheque_used = st.number_input(
                "Em Uso (R$)",
                min_value=0.0,
                step=100.00,
                format="%.2f",
                key="modal_cheque_used",
            )

            cheque_rate = st.number_input(
                "Taxa (%)",
                min_value=0.0,
                step=0.1,
                format="%.2f",
                key="modal_cheque_rate",
            )

        # Botões de ação
        col_save, col_cancel = st.columns(2)

        with col_save:
            submit = st.form_submit_button(
                "Salvar", use_container_width=True, type="primary"
            )

        with col_cancel:
            cancel = st.form_submit_button("Cancelar", use_container_width=True)

        if submit:
            if not bank_name or not bank_name.strip():
                st.error("Nome do banco é obrigatório!")
            else:
                try:
                    bank_limit_use_cases.create_bank_limit(
                        bank_name.strip(),
                        rotativo_available,
                        rotativo_used,
                        cheque_available,
                        cheque_used,
                        rotativo_rate,
                        cheque_rate,
                        0.0,  # interest_rate mantido para compatibilidade
                    )
                    st.success("Banco cadastrado com sucesso!")
                    st.session_state.show_add_bank_modal = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")

        if cancel:
            st.session_state.show_add_bank_modal = False
            st.rerun()
