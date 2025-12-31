import streamlit as st
from datetime import datetime
from dependencies import get_container
from presentation.components.page_header import render_page_header


def render():
    render_page_header("Registrar Lançamento")

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

        with st.form("database_form"):
            col1, col2 = st.columns(2)

            with col1:
                date = st.date_input("Data", format="DD/MM/YYYY", value=datetime.now())

            with col2:
                value = st.number_input("Valor (R$)", min_value=0.0, step=0.01)

            modality_options = {m.name: m for m in modalities}
            selected_name = st.selectbox("Modalidade", options=list(modality_options.keys()))
            selected_modality = modality_options[selected_name]

            submitted = st.form_submit_button("Salvar", use_container_width=True, type="primary")

            if submitted:
                try:
                    entry_datetime = datetime.combine(date, datetime.min.time())
                    entry_use_cases.create_entry(
                        value=value,
                        date=entry_datetime,
                        modality_id=selected_modality.id,
                        modality_name=selected_modality.name,
                        modality_color=selected_modality.color,
                    )
                    st.success("Lançamento salvo com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")

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
                datetime.combine(start_date, datetime.min.time()) if start_date else None
            )
            end_datetime = (
                datetime.combine(end_date, datetime.max.time()) if end_date else None
            )

            entries = entry_use_cases.list_entries(start_datetime, end_datetime)

            # Criar mapeamento de modality_id para cor e nome
            modality_color_map = {m.id: m.color for m in modalities}
            modality_name_map = {m.id: m.name for m in modalities}

            if not entries:
                st.info("Nenhum lançamento encontrado no período selecionado.")
            else:
                total = entry_use_cases.get_total_by_period(start_datetime, end_datetime)
                st.markdown(f"### Total Geral: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                st.divider()

                entries_by_date = {}
                for entry in sorted(entries, key=lambda x: x.date, reverse=True):
                    date_str = entry.date.strftime("%d/%m/%Y")
                    if date_str not in entries_by_date:
                        entries_by_date[date_str] = []
                    entries_by_date[date_str].append(entry)

                max_entries = max(len(date_entries) for date_entries in entries_by_date.values())

                dates_sorted = sorted(entries_by_date.keys(), reverse=True)

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
                    header_label = f"{date_str} - Total: R$ {daily_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    html_content += f"<th colspan='2' style='background-color: #f0f0f0; padding: 12px; text-align: center; border: 1px solid #ddd; font-weight: bold;'>{header_label}</th>"
                html_content += "</tr></thead>"

                html_content += "<tbody>"
                for i in range(max_entries):
                    html_content += "<tr>"
                    for date_str in dates_sorted:
                        date_entries = entries_by_date[date_str]
                        if i < len(date_entries):
                            entry = date_entries[i]
                            value_formatted = f"R$ {entry.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                            # Usar a cor da modalidade atual, não a cor salva no entry
                            modality_color = modality_color_map.get(entry.modality_id, entry.modality_color)
                            modality_name = modality_name_map.get(entry.modality_id, entry.modality_name)

                            html_content += f"<td style='padding: 10px; text-align: right; border: 1px solid #ddd; min-width: 180px; white-space: nowrap;'>{value_formatted}</td>"

                            html_content += (
                                f"<td style='padding: 10px; text-align: center; border: 1px solid #ddd; min-width: 180px; white-space: nowrap; "
                                f"background-color: {modality_color}; color: white; font-weight: bold;'>"
                                f"{modality_name}</td>"
                            )
                        else:
                            html_content += "<td style='padding: 10px; border: 1px solid #ddd; min-width: 180px;'></td>"
                            html_content += "<td style='padding: 10px; border: 1px solid #ddd; min-width: 180px;'></td>"
                    html_content += "</tr>"
                html_content += "</tbody></table>"
                html_content += "</div>"

                st.markdown(html_content, unsafe_allow_html=True)

                st.subheader("Legenda de Modalidades", anchor=False)
                unique_modalities = {}
                for entry in entries:
                    # Usar a cor da modalidade atual, não a cor salva no entry
                    modality_name = modality_name_map.get(entry.modality_id, entry.modality_name)
                    modality_color = modality_color_map.get(entry.modality_id, entry.modality_color)
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
                for entry in sorted(entries, key=lambda x: x.date, reverse=True):
                    # Usar o nome da modalidade atual, não o nome salvo no entry
                    modality_name = modality_name_map.get(entry.modality_id, entry.modality_name)
                    df_data.append(
                        {
                            "Data": entry.date.strftime("%d/%m/%Y"),
                            "Valor": f"R$ {entry.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                            "Modalidade": modality_name,
                            "ID": entry.id,
                        }
                    )

                st.subheader("Excluir Lançamento", anchor=False)
                entry_to_delete = st.selectbox(
                    "Selecione o lançamento para excluir",
                    options=[f"{e['Data']} - {e['Modalidade']} - {e['Valor']}" for e in df_data],
                    key="delete_entry",
                )

                @st.dialog("Confirmar Exclusão")
                def confirm_delete_modal():
                    st.write("⚠️ Tem certeza que deseja excluir este lançamento?")
                    st.write(f"**{entry_to_delete}**")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Sim, excluir", type="primary", use_container_width=True):
                            idx = [f"{e['Data']} - {e['Modalidade']} - {e['Valor']}" for e in df_data].index(
                                entry_to_delete
                            )
                            entry_id = df_data[idx]["ID"]
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
        st.info("Verifique se a URL da API está configurada corretamente no arquivo .env")
