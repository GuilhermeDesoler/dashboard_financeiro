import streamlit as st
from dependencies import get_container
from presentation.components.page_header import render_page_header
from collections import defaultdict


def render():
    render_page_header("Modalidades de Pagamento")

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
    modality_use_cases = container.payment_modality_use_cases
    settings_use_cases = container.platform_settings_use_cases

    # Platform Settings Section
    _render_platform_settings(settings_use_cases)

    st.divider()

    # Botão para criar nova modalidade
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➕ Criar Nova Modalidade", use_container_width=True, type="primary"):
            st.session_state.show_create_modal = True

    st.divider()

    # Renderizar modalidades
    _render_modalities_by_bank(modality_use_cases)

    # Modais
    if st.session_state.get("show_create_modal", False):
        _show_create_modality_modal(modality_use_cases)

    if st.session_state.get("show_edit_modal", False):
        _show_edit_modality_modal(modality_use_cases)


def _render_platform_settings(settings_use_cases):
    """Render platform settings section with anticipation toggle"""
    st.subheader("Configurações da Plataforma", anchor=False)

    try:
        settings = settings_use_cases.get_settings()

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
                """
                <div style="padding: 15px; background-color: #f0f2f6; border-radius: 8px;">
                    <h4 style="margin: 0 0 8px 0;">Antecipação de Valores</h4>
                    <p style="margin: 0; color: #666; font-size: 14px;">
                        Permite que os usuários antecipem valores futuros no sistema.
                        Quando ativado, as modalidades que permitem antecipação estarão disponíveis.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            status_text = (
                "Ativada" if settings.is_anticipation_enabled else "Desativada"
            )
            status_color = "#4CAF50" if settings.is_anticipation_enabled else "Desativada"

            st.markdown(
                f"""
                <div style="
                    padding: 10px;
                    background-color: {status_color}20;
                    border-radius: 8px;
                    text-align: center;
                    margin-bottom: 10px;
                ">
                    <span style="color: {status_color}; font-weight: bold; font-size: 14px;">
                        {status_text}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            toggle_label = "Desativar" if settings.is_anticipation_enabled else "Ativar"
            button_type = "secondary" if settings.is_anticipation_enabled else "primary"

            if st.button(
                toggle_label,
                key="toggle_anticipation",
                use_container_width=True,
                type=button_type,
            ):
                try:
                    updated_settings = settings_use_cases.toggle_anticipation()
                    action = (
                        "ativada"
                        if updated_settings.is_anticipation_enabled
                        else "desativada"
                    )
                    st.success(f"Antecipação {action} com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao alterar configuração: {str(e)}")

    except Exception as e:
        st.error(f"Erro ao carregar configurações: {str(e)}")
        st.info(
            "Verifique se a URL da API está configurada corretamente no arquivo .env"
        )


def _render_modalities_by_bank(use_cases):
    """Renderiza modalidades agrupadas por banco"""
    st.subheader("Modalidades por Banco", anchor=False)

    try:
        modalities = use_cases.list_modalities()

        if not modalities:
            st.info("Nenhuma modalidade cadastrada ainda.")
            return

        # Agrupar modalidades por banco
        modalities_by_bank = defaultdict(list)
        for modality in modalities:
            bank = modality.bank_name if modality.bank_name else "Sem Banco"
            modalities_by_bank[bank].append(modality)

        # Renderizar seções por banco
        for bank_name in sorted(modalities_by_bank.keys()):
            bank_modalities = modalities_by_bank[bank_name]

            # Header do banco
            st.markdown(f"### 🏦 {bank_name}")
            st.markdown(f"**{len(bank_modalities)} modalidade(s)**")

            # Cards das modalidades do banco
            cols = st.columns(3)
            for idx, modality in enumerate(sorted(bank_modalities, key=lambda x: x.name)):
                with cols[idx % 3]:
                    _render_modality_card_compact(modality)

            st.divider()

    except Exception as e:
        st.error(f"Erro ao carregar modalidades: {str(e)}")
        st.info(
            "Verifique se a URL da API está configurada corretamente no arquivo .env"
        )


def _render_modality_card_compact(modality):
    """Renderiza um card compacto e clicável de modalidade"""
    # Status color - Verde para ativo, Vermelho para inativo
    status_color = "#4CAF50" if modality.is_active else "#F44336"
    status_text = "Ativa" if modality.is_active else "Inativa"

    # Build features text
    features = []
    if modality.is_credit_plan:
        features.append("Crediário")
    if modality.allows_anticipation:
        features.append("Antecipação")
    if modality.allows_credit_payment:
        features.append("Pgto Crediário")

    features_text = " • ".join(features) if features else "Sem recursos especiais"

    # Format fee
    fee_text = f"{modality.fee_percentage:.1f}%" if modality.fee_percentage > 0 else "Sem taxa"

    # Format rental
    rental_row = ""
    if modality.rental_fee > 0:
        rental_formatted = f"R$ {modality.rental_fee:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        rental_row = f'<p style="margin: 0; font-size: 11px; color: #e74c3c;"><strong>Aluguel:</strong> {rental_formatted}</p>'

    # Build complete HTML (single line to avoid whitespace issues)
    card_html = f'<div style="background: linear-gradient(135deg, {modality.color}15 0%, {modality.color}05 100%); border-left: 4px solid {modality.color}; border-radius: 8px; padding: 16px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); min-height: 140px;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;"><h4 style="margin: 0; color: {modality.color}; font-size: 16px;">{modality.name}</h4><div style="display: flex; align-items: center; gap: 6px;"><span style="font-size: 11px; color: {status_color}; font-weight: bold;">{status_text}</span><div style="width: 12px; height: 12px; background-color: {status_color}; border-radius: 50%;"></div></div></div><p style="margin: 4px 0; font-size: 13px; color: #555;"><strong>Taxa:</strong> {fee_text}</p>{rental_row}<p style="margin: 8px 0 0 0; font-size: 11px; color: #888; font-style: italic;">{features_text}</p></div>'

    st.markdown(card_html, unsafe_allow_html=True)

    # Botão clicável sobre o card
    if st.button("✏️ Editar", key=f"edit_{modality.id}", use_container_width=True):
        st.session_state.show_edit_modal = True
        st.session_state.edit_modality_id = modality.id
        st.rerun()


@st.dialog("➕ Criar Nova Modalidade")
def _show_create_modality_modal(use_cases):
    """Modal para criar nova modalidade"""
    with st.form(key="create_modality_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Nome da Modalidade *",
                placeholder="Ex: PIX, Débito, Crédito à vista...",
                max_chars=100,
            )

            bank_name = st.text_input(
                "Banco",
                placeholder="Ex: Sicredi, Sicoob, Link Sicredi...",
                help="Deixe em branco se não houver banco associado",
                max_chars=100,
            )

            fee_percentage = st.number_input(
                "Taxa (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                format="%.2f",
                help="Taxa percentual da modalidade (ex: 0.9, 1.1, 1.4)"
            )

        with col2:
            color = st.color_picker("Cor", value="#9333EA")

            rental_fee = st.number_input(
                "Aluguel Mensal (R$)",
                min_value=0.0,
                value=0.0,
                step=1.0,
                format="%.2f",
                help="Valor do aluguel mensal (se houver)"
            )

            is_active = st.checkbox(
                "Modalidade Ativa",
                value=True,
                help="Modalidades inativas não aparecem como opção ao criar lançamentos",
            )

        st.markdown("#### Configurações Avançadas")

        col1, col2, col3 = st.columns(3)

        with col1:
            is_credit_plan = st.checkbox(
                "É Crediário",
                value=False,
                help="Indica se esta modalidade é usada para vendas a crediário",
            )

        with col2:
            allows_anticipation = st.checkbox(
                "Permite Antecipação",
                value=False,
                help="Permite antecipar valores futuros",
            )

        with col3:
            allows_credit_payment = st.checkbox(
                "Permite Pgto Crediário",
                value=False,
                help="Permite usar esta modalidade para pagar parcelas de crediário",
            )

        st.markdown("---")

        col_save, col_cancel = st.columns([3, 1])

        with col_save:
            submitted = st.form_submit_button(
                "💾 Salvar", use_container_width=True, type="primary"
            )

        with col_cancel:
            cancel = st.form_submit_button("Cancelar", use_container_width=True)

        if cancel:
            st.session_state.show_create_modal = False
            st.rerun()

        if submitted:
            if not name or not name.strip():
                st.error("Por favor, informe o nome da modalidade.")
            else:
                try:
                    use_cases.create_modality(
                        name=name.strip(),
                        color=color,
                        bank_name=bank_name.strip() if bank_name else "",
                        fee_percentage=fee_percentage,
                        rental_fee=rental_fee,
                        is_active=is_active,
                        is_credit_plan=is_credit_plan,
                        allows_anticipation=allows_anticipation,
                        allows_credit_payment=allows_credit_payment,
                    )
                    st.success(f"Modalidade '{name}' criada com sucesso!")
                    st.balloons()
                    st.session_state.show_create_modal = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")


@st.dialog("✏️ Editar Modalidade")
def _show_edit_modality_modal(use_cases):
    """Modal para editar modalidade existente"""
    modality_id = st.session_state.get("edit_modality_id")
    if not modality_id:
        st.error("Modalidade não encontrada")
        return

    # Buscar modalidade
    modalities = use_cases.list_modalities()
    selected_modality = next((m for m in modalities if m.id == modality_id), None)

    if not selected_modality:
        st.error("Modalidade não encontrada")
        return

    with st.form(key="edit_modality_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Nome da Modalidade *",
                value=selected_modality.name,
                placeholder="Ex: PIX, Débito, Crédito à vista...",
                max_chars=100,
            )

            bank_name = st.text_input(
                "Banco",
                value=selected_modality.bank_name,
                placeholder="Ex: Sicredi, Sicoob, Link Sicredi...",
                help="Deixe em branco se não houver banco associado",
                max_chars=100,
            )

            fee_percentage = st.number_input(
                "Taxa (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(selected_modality.fee_percentage),
                step=0.1,
                format="%.2f",
                help="Taxa percentual da modalidade (ex: 0.9, 1.1, 1.4)"
            )

        with col2:
            color = st.color_picker("Cor", value=selected_modality.color)

            rental_fee = st.number_input(
                "Aluguel Mensal (R$)",
                min_value=0.0,
                value=float(selected_modality.rental_fee),
                step=1.0,
                format="%.2f",
                help="Valor do aluguel mensal (se houver)"
            )

            is_active = st.checkbox(
                "Modalidade Ativa",
                value=selected_modality.is_active,
                help="Modalidades inativas não aparecem como opção ao criar lançamentos",
            )

        st.markdown("#### Configurações Avançadas")

        col1, col2, col3 = st.columns(3)

        with col1:
            is_credit_plan = st.checkbox(
                "É Crediário",
                value=selected_modality.is_credit_plan,
                help="Indica se esta modalidade é usada para vendas a crediário",
            )

        with col2:
            allows_anticipation = st.checkbox(
                "Permite Antecipação",
                value=selected_modality.allows_anticipation,
                help="Permite antecipar valores futuros",
            )

        with col3:
            allows_credit_payment = st.checkbox(
                "Permite Pgto Crediário",
                value=selected_modality.allows_credit_payment,
                help="Permite usar esta modalidade para pagar parcelas de crediário",
            )

        st.markdown("---")

        col_save, col_delete, col_cancel = st.columns([2, 1, 1])

        with col_save:
            submitted = st.form_submit_button(
                "💾 Atualizar", use_container_width=True, type="primary"
            )

        with col_delete:
            delete_clicked = st.form_submit_button(
                "🗑️ Excluir", use_container_width=True
            )

        with col_cancel:
            cancel = st.form_submit_button("Cancelar", use_container_width=True)

        if cancel:
            st.session_state.show_edit_modal = False
            st.session_state.edit_modality_id = None
            st.rerun()

        if submitted:
            if not name or not name.strip():
                st.error("Por favor, informe o nome da modalidade.")
            else:
                try:
                    use_cases.update_modality(
                        selected_modality.id,
                        name=name.strip(),
                        color=color,
                        bank_name=bank_name.strip() if bank_name else "",
                        fee_percentage=fee_percentage,
                        rental_fee=rental_fee,
                        is_active=is_active,
                        is_credit_plan=is_credit_plan,
                        allows_anticipation=allows_anticipation,
                        allows_credit_payment=allows_credit_payment,
                    )
                    st.success(f"Modalidade '{name}' atualizada com sucesso!")
                    st.session_state.show_edit_modal = False
                    st.session_state.edit_modality_id = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")

        if delete_clicked:
            try:
                use_cases.delete_modality(selected_modality.id)
                st.success("Modalidade excluída com sucesso!")
                st.session_state.show_edit_modal = False
                st.session_state.edit_modality_id = None
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao excluir: {str(e)}")


