import streamlit as st
from datetime import datetime, timedelta
from dependencies import get_container
from presentation.components.page_header import render_page_header


def render():
    render_page_header("Registrar Lançamento")

    # Exibir toast se existir no session_state
    if "toast_message" in st.session_state:
        st.toast(st.session_state.toast_message)
        del st.session_state.toast_message

    container = get_container()
    modality_use_cases = container.payment_modality_use_cases
    entry_use_cases = container.financial_entry_use_cases

    try:
        modalities = modality_use_cases.list_active_modalities()

        if not modalities:
            st.warning(
                "Nenhuma modalidade de pagamento cadastrada. "
                "Por favor, cadastre modalidades na página 'Modalidades'."
            )
            return

        # Container to make it look like a single form
        with st.container(border=True):
            st.subheader("Novo Lançamento", anchor=False)

            # Basic fields
            col1, col2 = st.columns(2)

            with col1:
                # Usar session_state para manter a data sem recarregar
                if "entry_date_value" not in st.session_state:
                    st.session_state.entry_date_value = datetime.now()

                date = st.date_input(
                    "Data",
                    format="DD/MM/YYYY",
                    value=st.session_state.entry_date_value,
                    key="entry_date"
                )

            with col2:
                value = st.number_input(
                    "Valor (R$)",
                    min_value=0.0,
                    value=None,
                    step=0.01,
                    format="%.2f",
                    key="entry_value",
                    help="Digite o valor do lançamento (mínimo R$ 0,01)"
                )

            # Criar opções com formato "nome (banco)" - apenas modalidades ativas
            modality_options = {}
            for m in modalities:
                if m.is_active:  # Apenas modalidades ativas
                    display_name = f"{m.name} ({m.bank_name})" if m.bank_name else m.name
                    modality_options[display_name] = m

            selected_display_name = st.selectbox(
                "Modalidade",
                options=list(modality_options.keys()),
                key="modality_selector",
            )
            selected_modality = modality_options[selected_display_name]

            # Initialize variables
            is_credit_payment = False
            installments_count = None
            start_date = None
            can_submit = True

            # Conditional fields based on modality type
            if selected_modality.is_credit_plan:
                # Modality IS a credit plan - show installment configuration
                st.markdown("**Configuração do Crediário**")

                col_inst1, col_inst2 = st.columns(2)

                with col_inst1:
                    installments_count = st.number_input(
                        "Número de Parcelas",
                        min_value=1,
                        max_value=100,
                        value=10,
                        step=1,
                        help="Quantas parcelas serão geradas para este crediário",
                        key="installments_count",
                    )

                with col_inst2:
                    start_date_input = st.date_input(
                        "Data da Primeira Parcela",
                        format="DD/MM/YYYY",
                        value=datetime.now() + timedelta(days=30),
                        help="Data de vencimento da primeira parcela",
                        key="start_date",
                    )
                    start_date = datetime.combine(start_date_input, datetime.min.time())

            elif selected_modality.allows_credit_payment:
                # Modality is NOT credit_plan but ALLOWS credit payment - show checkbox
                is_credit_payment = st.checkbox(
                    "Este é um pagamento de crediário?",
                    value=False,
                    help="Marque se este valor é referente ao recebimento de uma parcela de crediário",
                    key="is_credit_payment",
                )

            # Validate required fields
            is_valid = True
            validation_errors = []

            if value is None or value <= 0:
                is_valid = False
                if value is not None:  # Só mostra erro se usuário digitou algo inválido
                    validation_errors.append("Valor deve ser maior que zero")

            if selected_modality.is_credit_plan:
                if not installments_count or installments_count < 1:
                    is_valid = False
                    validation_errors.append("Número de parcelas é obrigatório")
                if not start_date:
                    is_valid = False
                    validation_errors.append("Data da primeira parcela é obrigatória")

            # Show validation errors if any
            if validation_errors:
                for error in validation_errors:
                    st.warning(f"⚠️ {error}")

            # Submit button com loading
            submit_button = st.button(
                "Salvar Lançamento",
                use_container_width=True,
                type="primary",
                disabled=not can_submit or not is_valid,
                key="submit_entry",
            )

            if submit_button:
                # Mostrar spinner durante o envio
                with st.spinner("Salvando lançamento..."):
                    try:
                        entry_datetime = datetime.combine(date, datetime.min.time())

                        # Nome da modalidade com banco se disponível
                        modality_display_name = f"{selected_modality.name} ({selected_modality.bank_name})" if selected_modality.bank_name else selected_modality.name

                        result = entry_use_cases.create_entry(
                            value=value,
                            date=entry_datetime,
                            modality_id=selected_modality.id or "",
                            modality_name=modality_display_name,
                            modality_color=selected_modality.color,
                            is_credit_payment=is_credit_payment,
                            installments_count=installments_count,
                            start_date=start_date,
                        )

                        # Formatar valor para exibição
                        value_formatted = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        date_formatted = entry_datetime.strftime("%d/%m/%Y")

                        # Salvar mensagem de sucesso no session_state para exibir após rerun
                        if installments_count and installments_count >= 1:
                            installment_value = value / installments_count
                            installment_value_formatted = f"R$ {installment_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                            st.session_state.success_message = (
                                f"✅ **Crediário criado com sucesso!**\n\n"
                                f"**Valor:** {value_formatted}\n\n"
                                f"**Data:** {date_formatted}\n\n"
                                f"**Modalidade:** {modality_display_name}\n\n"
                                f"**Parcelas:** {installments_count}x de {installment_value_formatted}"
                            )

                            # Salvar toast para exibir após rerun
                            st.session_state.toast_message = f"✅ Crediário criado: {value_formatted}"
                        else:
                            st.session_state.success_message = (
                                f"✅ **Lançamento enviado com sucesso!**\n\n"
                                f"**Valor:** {value_formatted}\n\n"
                                f"**Data:** {date_formatted}\n\n"
                                f"**Modalidade:** {modality_display_name}"
                            )

                            # Salvar toast para exibir após rerun
                            st.session_state.toast_message = f"✅ Lançamento salvo: {value_formatted}"

                        # Limpar campos do formulário
                        if "entry_value" in st.session_state:
                            del st.session_state.entry_value
                        if "entry_date" in st.session_state:
                            st.session_state.entry_date_value = datetime.now()
                        if "modality_selector" in st.session_state:
                            del st.session_state.modality_selector
                        if "is_credit_payment" in st.session_state:
                            del st.session_state.is_credit_payment
                        if "installments_count" in st.session_state:
                            del st.session_state.installments_count
                        if "start_date" in st.session_state:
                            del st.session_state.start_date

                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar: {str(e)}")

            # Mostrar mensagem de sucesso abaixo do formulário
            if "success_message" in st.session_state:
                st.success(st.session_state.success_message)
                # Limpar a mensagem após exibir
                del st.session_state.success_message

        st.divider()
        st.subheader("Lançamentos Registrados", anchor=False)

        st.markdown("### Filtros")
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            start_date = st.date_input(
                "Data Início", value=None, format="DD/MM/YYYY", key="filtro_inicio"
            )

        with col2:
            end_date = st.date_input(
                "Data Fim", value=None, format="DD/MM/YYYY", key="filtro_fim"
            )

        with col3:
            st.write("")
            st.write("")
            if st.button("Limpar", use_container_width=True):
                st.session_state.filtro_inicio = None
                st.session_state.filtro_fim = None
                st.rerun()

        try:
            start_datetime = (
                datetime.combine(start_date, datetime.min.time())
                if start_date
                else None
            )
            end_datetime = (
                datetime.combine(end_date, datetime.max.time()) if end_date else None
            )

            entries = entry_use_cases.list_entries(start_datetime, end_datetime)

            # Criar mapeamento de modality_id para cor, nome e banco
            modality_color_map = {m.id: m.color for m in modalities}
            modality_name_map = {}
            for m in modalities:
                # Incluir banco no nome se disponível
                display_name = f"{m.name} ({m.bank_name})" if m.bank_name else m.name
                modality_name_map[m.id] = display_name

            if not entries:
                st.info("Nenhum lançamento encontrado no período selecionado.")
            else:
                total = entry_use_cases.get_total_by_period(
                    start_datetime, end_datetime
                )
                st.markdown(
                    f"### Total Geral: R$ {total:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
                st.divider()

                entries_by_date = {}
                # Ordena por created_at crescente (primeiro lançamento embaixo, mais recente em cima)
                for entry in sorted(entries, key=lambda x: x.created_at or x.date, reverse=False):
                    date_str = entry.date.strftime("%d/%m/%Y")
                    if date_str not in entries_by_date:
                        entries_by_date[date_str] = []
                    entries_by_date[date_str].append(entry)

                max_entries = max(
                    len(date_entries) for date_entries in entries_by_date.values()
                )

                # Ordena as datas usando datetime para comparação correta
                dates_sorted = sorted(
                    entries_by_date.keys(),
                    key=lambda d: datetime.strptime(d, "%d/%m/%Y"),
                    reverse=True,
                )

                html_content = """
                <style>
                .scroll-container {
                    overflow-x: auto;
                    max-height: 700px;
                    overflow-y: auto;
                    margin: 20px 0;
                }
                .scroll-container::-webkit-scrollbar {
                    height: 12px;
                    width: 12px;
                }
                .scroll-container::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 10px;
                }
                .scroll-container::-webkit-scrollbar-thumb {
                    background: #9333EA;
                    border-radius: 10px;
                }
                .scroll-container::-webkit-scrollbar-thumb:hover {
                    background: #7c2cc9;
                }
                </style>
                <div class='scroll-container'>"""

                html_content += "<table style='border-collapse: collapse;'>"

                html_content += "<thead><tr>"
                for date_str in dates_sorted:
                    date_entries = entries_by_date[date_str]
                    daily_total = sum(e.value for e in date_entries)
                    header_label = (
                        f"{date_str} - Total: R$ {daily_total:,.2f}".replace(",", "X")
                        .replace(".", ",")
                        .replace("X", ".")
                    )
                    html_content += f"<th colspan='2' style='background-color: #f0f0f0; padding: 12px; text-align: center; border: 1px solid #ddd; font-weight: bold;'>{header_label}</th>"
                html_content += "</tr></thead>"

                html_content += "<tbody>"

                # Criar estrutura para rastrear IDs dos entries por posição
                entries_grid = {}  # {(row_idx, col_idx): entry}

                for i in range(max_entries):
                    html_content += "<tr>"
                    for col_idx, date_str in enumerate(dates_sorted):
                        date_entries = entries_by_date[date_str]
                        if i < len(date_entries):
                            entry = date_entries[i]
                            entries_grid[(i, col_idx)] = entry

                            value_formatted = (
                                f"R$ {entry.value:,.2f}".replace(",", "X")
                                .replace(".", ",")
                                .replace("X", ".")
                            )

                            # Usar a cor da modalidade atual, não a cor salva no entry
                            modality_color = modality_color_map.get(
                                entry.modality_id, entry.modality_color
                            )
                            modality_name = modality_name_map.get(
                                entry.modality_id, entry.modality_name
                            )

                            html_content += f"<td style='padding: 10px; text-align: right; border: 1px solid #ddd; min-width: 180px; white-space: nowrap;'>{value_formatted}</td>"

                            # Converter cor hex para rgba com 60% opacidade
                            def hex_to_rgba(hex_color, opacity=0.6):
                                hex_color = hex_color.lstrip("#")
                                r, g, b = tuple(
                                    int(hex_color[i : i + 2], 16) for i in (0, 2, 4)
                                )
                                return f"rgba({r}, {g}, {b}, {opacity})"

                            # Se for pagamento de crediário, usar cor verde; senão, usar cor da modalidade
                            if entry.credit_payment:
                                # Verde para recebimento de crediário
                                bg_color = "rgba(34, 197, 94, 0.7)"  # Verde mais forte
                                display_text = f"Recebimento Crediário<br><span style='font-size: 11px; font-weight: normal;'>{modality_name}</span>"
                            elif entry.is_credit_plan:
                                # Mostrar "Pgto Crediário" abaixo do nome da modalidade
                                bg_color = hex_to_rgba(modality_color, 0.6)
                                display_text = f"{modality_name}<br><span style='font-size: 11px; font-weight: normal;'>Pgto Crediário</span>"
                            else:
                                bg_color = hex_to_rgba(modality_color, 0.6)
                                display_text = modality_name

                            html_content += (
                                f"<td style='padding: 10px; text-align: center; border: 1px solid #ddd; min-width: 180px; white-space: nowrap; "
                                f"background-color: {bg_color}; color: #333; font-weight: bold;'>"
                                f"{display_text}</td>"
                            )
                        else:
                            html_content += "<td style='padding: 10px; border: 1px solid #ddd; min-width: 180px;'></td>"
                            html_content += "<td style='padding: 10px; border: 1px solid #ddd; min-width: 180px;'></td>"
                    html_content += "</tr>"
                html_content += "</tbody></table>"
                html_content += "</div>"

                st.markdown(html_content, unsafe_allow_html=True)

                # Modal de confirmação
                if st.session_state.get("show_delete_modal", False):
                    @st.dialog("Confirmar Exclusão")
                    def confirm_delete_modal():
                        st.write("Tem certeza que deseja excluir este lançamento?")
                        st.write(f"**{st.session_state.entry_to_delete_label}**")
                        st.warning("⚠️ Esta ação não pode ser desfeita!")

                        col1, col2 = st.columns(2)

                        with col1:
                            if st.button("Sim, excluir", type="primary", use_container_width=True):
                                try:
                                    entry_use_cases.delete_entry(st.session_state.entry_to_delete_id)
                                    st.success("Lançamento excluído com sucesso!")
                                    del st.session_state.show_delete_modal
                                    del st.session_state.entry_to_delete_id
                                    del st.session_state.entry_to_delete_label
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao excluir: {str(e)}")

                        with col2:
                            if st.button("Cancelar", use_container_width=True):
                                del st.session_state.show_delete_modal
                                st.rerun()

                    confirm_delete_modal()

                st.subheader("Legenda de Modalidades", anchor=False)
                unique_modalities = {}
                for entry in entries:
                    # Usar a cor da modalidade atual, não a cor salva no entry
                    modality_name = modality_name_map.get(
                        entry.modality_id, entry.modality_name
                    )
                    modality_color = modality_color_map.get(
                        entry.modality_id, entry.modality_color
                    )
                    if modality_name not in unique_modalities:
                        unique_modalities[modality_name] = modality_color

                legend_html = "<div style='display: flex; flex-wrap: wrap; gap: 12px; margin-top: 8px;'>"
                for modality_name, color in sorted(unique_modalities.items()):
                    legend_html += (
                        f"<div style='display: flex; align-items: center; gap: 6px;'>"
                        f"<div style='width: 16px; height: 16px; background-color: {color}; "
                        f"border-radius: 3px; border: 1px solid #ccc;'></div>"
                        f"<span style='font-size: 14px;'>{modality_name}</span>"
                        f"</div>"
                    )
                legend_html += "</div>"
                st.markdown(legend_html, unsafe_allow_html=True)

                df_data = []
                entry_options = []
                entry_map = {}

                # Ordena por created_at decrescente para listagem de exclusão (mais recente primeiro no select)
                for entry in sorted(entries, key=lambda x: x.created_at or x.date, reverse=True):
                    # Usar o nome da modalidade atual, não o nome salvo no entry
                    modality_name = modality_name_map.get(
                        entry.modality_id, entry.modality_name
                    )

                    data_str = entry.date.strftime("%d/%m/%Y")
                    valor_str = f"R$ {entry.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    option_label = f"{data_str} - {modality_name} - {valor_str}"

                    df_data.append(
                        {
                            "Data": data_str,
                            "Valor": valor_str,
                            "Modalidade": modality_name,
                            "ID": entry.id,
                        }
                    )

                    entry_options.append(option_label)
                    entry_map[option_label] = entry.id

                st.subheader("Excluir Lançamento", anchor=False)
                entry_to_delete = st.selectbox(
                    "Selecione o lançamento para excluir",
                    options=entry_options,
                    key="delete_entry",
                )

                @st.dialog("Confirmar Exclusão")
                def confirm_delete_modal():
                    st.write("Tem certeza que deseja excluir este lançamento?")
                    st.write(f"**{entry_to_delete}**")
                    st.warning("⚠️ Esta ação não pode ser desfeita!")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(
                            "Sim, excluir", type="primary", use_container_width=True
                        ):
                            entry_id = entry_map[entry_to_delete]
                            try:
                                entry_use_cases.delete_entry(entry_id)
                                st.success("Lançamento excluído com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao excluir: {str(e)}")

                    with col2:
                        if st.button("Cancelar", use_container_width=True):
                            st.rerun()

                if st.button("Excluir", type="primary"):
                    confirm_delete_modal()

        except Exception as e:
            st.error(f"Erro ao carregar lançamentos: {str(e)}")

    except Exception as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        st.info(
            "Verifique se a URL da API está configurada corretamente no arquivo .env"
        )
