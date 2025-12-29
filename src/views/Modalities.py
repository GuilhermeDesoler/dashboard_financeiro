import streamlit as st
from dependencies import get_container


def render():
    st.title("Modalidades de Pagamento", anchor=False)

    container = get_container()
    use_cases = container.payment_modality_use_cases

    tab1, tab2 = st.tabs(["Lista de Modalidades", "Nova Modalidade"])

    with tab1:
        _render_modalities_list(use_cases)

    with tab2:
        _render_create_modality(use_cases)


def _render_modalities_list(use_cases):
    st.subheader("Modalidades Cadastradas", anchor=False)

    try:
        modalities = use_cases.list_modalities()

        if not modalities:
            st.info("Nenhuma modalidade cadastrada ainda.")
            return

        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("Buscar", placeholder="Digite para filtrar...")
        with col2:
            show_filter = st.selectbox(
                "Exibir", options=["Todos", "Ativos", "Inativos"], index=0
            )

        filtered_modalities = modalities
        if search:
            filtered_modalities = [
                m for m in filtered_modalities if search.lower() in m.name.lower()
            ]

        if show_filter == "Ativos":
            filtered_modalities = [m for m in filtered_modalities if m.is_active]
        elif show_filter == "Inativos":
            filtered_modalities = [m for m in filtered_modalities if not m.is_active]

        st.markdown(f"**Total:** {len(filtered_modalities)} modalidade(s)")
        st.divider()

        if not filtered_modalities:
            st.warning("Nenhuma modalidade encontrada com os filtros aplicados.")
            return

        for modality in sorted(filtered_modalities, key=lambda x: x.name):
            with st.container():
                col1, col2 = st.columns([5, 1])

                with col1:
                    # Nome com indicador de cor
                    st.markdown(
                        f"<div style='display: flex; align-items: center; gap: 10px;'>"
                        f"<div style='width: 20px; height: 20px; background-color: {modality.color}; "
                        f"border-radius: 4px; border: 1px solid #ccc;'></div>"
                        f"<h3 style='margin: 0;'>{modality.name}</h3>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    status_text = "Ativo" if modality.is_active else "Inativo"
                    status_color = "green" if modality.is_active else "red"
                    st.markdown(
                        f"<div style='padding: 4px 8px; background-color: {status_color}20; "
                        f"border-radius: 8px; text-align: center; display: inline-block; margin-top: 8px;'>"
                        f"<span style='color: {status_color}; font-weight: bold;'>{status_text}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                with col2:
                    toggle_label = "Desativar" if modality.is_active else "Ativar"
                    if st.button(
                        toggle_label,
                        key=f"toggle_{modality.id}",
                        use_container_width=True,
                    ):
                        try:
                            use_cases.toggle_modality(modality.id)
                            st.success(
                                f"Modalidade {'desativada' if modality.is_active else 'ativada'} com sucesso!"
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao alterar status: {str(e)}")

                    if st.button(
                        "Editar",
                        key=f"edit_{modality.id}",
                        use_container_width=True,
                    ):
                        st.session_state[f"editing_{modality.id}"] = True
                        st.rerun()

                if st.session_state.get(f"editing_{modality.id}", False):
                    with st.form(key=f"edit_form_{modality.id}"):
                        new_name = st.text_input(
                            "Nome da Modalidade",
                            value=modality.name,
                            key=f"name_{modality.id}",
                        )
                        new_color = st.color_picker(
                            "Cor",
                            value=modality.color,
                            key=f"color_{modality.id}",
                        )
                        new_status = st.checkbox(
                            "Ativa",
                            value=modality.is_active,
                            key=f"status_{modality.id}",
                        )

                        col_save, col_delete, col_cancel = st.columns(3)

                        with col_save:
                            if st.form_submit_button("Salvar", use_container_width=True):
                                try:
                                    use_cases.update_modality(
                                        modality.id, new_name, new_color, new_status
                                    )
                                    st.success("Modalidade atualizada com sucesso!")
                                    st.session_state[f"editing_{modality.id}"] = False
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao atualizar: {str(e)}")

                        with col_delete:
                            if st.form_submit_button(
                                "Excluir", use_container_width=True
                            ):
                                try:
                                    use_cases.delete_modality(modality.id)
                                    st.success("Modalidade excluída com sucesso!")
                                    st.session_state[f"editing_{modality.id}"] = False
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao excluir: {str(e)}")

                        with col_cancel:
                            if st.form_submit_button(
                                "Cancelar", use_container_width=True
                            ):
                                st.session_state[f"editing_{modality.id}"] = False
                                st.rerun()

                st.divider()

    except Exception as e:
        st.error(f"Erro ao carregar modalidades: {str(e)}")
        st.info("Verifique se a URL da API está configurada corretamente no arquivo .env")


def _render_create_modality(use_cases):
    st.subheader("Cadastrar Nova Modalidade", anchor=False)

    with st.form("create_modality_form", clear_on_submit=True):
        name = st.text_input(
            "Nome da Modalidade",
            placeholder="Ex: Cartão de Crédito, PIX, Dinheiro...",
            max_chars=100,
        )

        color = st.color_picker("Cor", value="#9333EA")

        is_active = st.checkbox("Ativa", value=True)

        st.markdown("---")

        col1, col2 = st.columns([1, 3])
        with col1:
            submitted = st.form_submit_button(
                "Cadastrar", use_container_width=True, type="primary"
            )

        if submitted:
            if not name or not name.strip():
                st.error("Por favor, informe o nome da modalidade.")
            else:
                try:
                    use_cases.create_modality(name=name.strip(), color=color, is_active=is_active)
                    st.success(f"Modalidade '{name}' cadastrada com sucesso!")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao cadastrar modalidade: {str(e)}")

    st.markdown("---")
    st.info(
        "**Dica:** Modalidades inativas não aparecerão como opção "
        "ao criar novos lançamentos financeiros."
    )
