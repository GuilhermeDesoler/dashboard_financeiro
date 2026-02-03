import streamlit as st
from dependencies import get_container
from presentation.components.page_header import render_page_header


@st.dialog("Configurações Padrão")
def _render_config_modal(platform_settings_use_cases, settings):
    """Modal para configurações de markup"""
    st.info("Defina os valores padrão de markup para esta empresa.")

    col1, col2 = st.columns(2)

    with col1:
        new_markup = st.number_input(
            "Markup Padrão (M)",
            min_value=0.0,
            value=float(settings.markup_default),
            step=0.01,
            format="%.2f",
            help="Valor de markup padrão",
            key="config_markup"
        )

        new_cost = st.number_input(
            "Custo Adicional (C)",
            min_value=0.0,
            value=float(settings.markup_cost),
            step=0.01,
            format="%.2f",
            help="Constante de custo adicional",
            key="config_cost"
        )

    with col2:
        new_percentage = st.number_input(
            "Percentual de Aumento (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(settings.markup_percentage),
            step=0.5,
            format="%.2f",
            help="Percentual de aumento sobre o total (ex: 5 = 5%)",
            key="config_percentage"
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancelar", use_container_width=True):
            st.session_state.show_markup_config_modal = False
            st.rerun()

    with col2:
        if st.button("Salvar", type="primary", use_container_width=True):
            try:
                platform_settings_use_cases.update_markup_settings(
                    markup_default=new_markup,
                    markup_cost=new_cost,
                    markup_percentage=new_percentage
                )
                st.session_state.show_markup_config_modal = False
                st.success("Configurações salvas com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {str(e)}")


def render():
    render_page_header("Utilitários")

    container = get_container()
    platform_settings_use_cases = container.platform_settings_use_cases

    try:
        # Buscar configurações
        settings = platform_settings_use_cases.get_settings()

        # Verificar se usuário é admin ou super admin
        current_user = st.session_state.get("current_user")
        is_admin = st.session_state.get("user_role") == "admin"
        is_super_admin = current_user and current_user.is_super_admin if current_user else False

        # Configurações padrão
        default_markup = settings.markup_default
        default_cost = settings.markup_cost
        default_percentage = settings.markup_percentage

        # Tabs
        tab1, tab2, tab3 = st.tabs(["💰 Calcular Preço de Venda", "🛒 Calcular Preço de Compra", "🎯 Calcular Markup"])

        # ===========================
        # TAB 1: Calcular Preço de Venda
        # ===========================
        with tab1:
            # Botão de configuração para admin ou super admin
            if is_admin or is_super_admin:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col3:
                    if st.button("⚙️ Configurações", use_container_width=True, key="config_btn_tab1"):
                        st.session_state.show_markup_config_modal = True

            # Inputs em grid 2x2
            col1, col2 = st.columns(2)

            with col1:
                valor_compra_tab1 = st.number_input(
                    "Valor de Compra (V)",
                    min_value=0.0,
                    value=100.0,
                    step=0.01,
                    format="%.2f",
                    help="Valor de compra do produto",
                    key="tab1_valor"
                )

                markup_tab1 = st.number_input(
                    "Markup (M)",
                    min_value=0.0,
                    value=float(default_markup) if default_markup > 0 else 2.0,
                    step=0.1,
                    format="%.2f",
                    help="Multiplicador de markup",
                    key="tab1_markup"
                )

            with col2:
                custo_tab1 = st.number_input(
                    "Custo Adicional (C)",
                    min_value=0.0,
                    value=float(default_cost),
                    step=0.01,
                    format="%.2f",
                    help="Custo adicional fixo",
                    key="tab1_custo"
                )

                percentual_tab1 = st.number_input(
                    "Percentual de Aumento (%)",
                    min_value=0.0,
                    max_value=99.9,
                    value=float(default_percentage),
                    step=0.5,
                    format="%.2f",
                    help="Percentual de aumento",
                    key="tab1_percentual"
                )

            # Validações e avisos
            warnings = []
            if default_markup > 0 and markup_tab1 < default_markup:
                warnings.append(f"Markup ({markup_tab1:.2f}) está abaixo do padrão ({default_markup:.2f})")
            if default_cost > 0 and custo_tab1 < default_cost:
                warnings.append(f"Custo ({custo_tab1:.2f}) está abaixo do padrão ({default_cost:.2f})")
            if default_percentage > 0 and percentual_tab1 < default_percentage:
                warnings.append(f"Percentual ({percentual_tab1:.2f}%) está abaixo do padrão ({default_percentage:.2f}%)")

            if warnings:
                for warning in warnings:
                    st.warning(f"⚠️ {warning}")

            # Calcular preço de venda
            A_tab1 = 1 - (percentual_tab1 / 100)
            preco_venda_tab1 = (valor_compra_tab1 * markup_tab1 + custo_tab1) / A_tab1 if A_tab1 > 0 else 0

            # Calcular métricas
            lucro_bruto_tab1 = preco_venda_tab1 - valor_compra_tab1
            margem_tab1 = ((preco_venda_tab1 - valor_compra_tab1) / preco_venda_tab1 * 100) if preco_venda_tab1 > 0 else 0

            # Formatações
            preco_venda_fmt = f"R$ {preco_venda_tab1:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            lucro_fmt = f"R$ {lucro_bruto_tab1:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # Card com resultado
            st.markdown(f"""
            <div style="border: 3px solid #9333EA; border-radius: 16px; padding: 30px; background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); text-align: center; margin: 20px 0;">
                <p style="margin: 0; font-size: 16px; color: #6b21a8; font-weight: 600;">PREÇO DE VENDA</p>
                <h1 style="margin: 15px 0; font-size: 48px; color: #9333EA;">{preco_venda_fmt}</h1>
                <div style="display: flex; justify-content: center; gap: 40px; margin-top: 15px;">
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #6b21a8;">Lucro Bruto</p>
                        <p style="margin: 0; font-size: 18px; color: #10B981; font-weight: bold;">{lucro_fmt}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #6b21a8;">Margem</p>
                        <p style="margin: 0; font-size: 18px; color: #10B981; font-weight: bold;">{margem_tab1:.1f}%</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ===========================
        # TAB 2: Calcular Preço de Compra
        # ===========================
        with tab2:
            # Botão de configuração para admin ou super admin
            if is_admin or is_super_admin:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col3:
                    if st.button("⚙️ Configurações", use_container_width=True, key="config_btn_tab2"):
                        st.session_state.show_markup_config_modal = True

            # Inputs em grid 2x2
            col1, col2 = st.columns(2)

            with col1:
                preco_venda_tab2 = st.number_input(
                    "Preço de Venda (P)",
                    min_value=0.01,
                    value=250.0,
                    step=0.01,
                    format="%.2f",
                    help="Preço de venda praticado",
                    key="tab2_preco_venda"
                )

                markup_tab2 = st.number_input(
                    "Markup (M)",
                    min_value=0.01,
                    value=float(default_markup) if default_markup > 0 else 2.0,
                    step=0.1,
                    format="%.2f",
                    help="Multiplicador de markup",
                    key="tab2_markup"
                )

            with col2:
                custo_tab2 = st.number_input(
                    "Custo Adicional (C)",
                    min_value=0.0,
                    value=float(default_cost),
                    step=0.01,
                    format="%.2f",
                    help="Custo adicional fixo",
                    key="tab2_custo"
                )

                percentual_tab2 = st.number_input(
                    "Percentual de Aumento (%)",
                    min_value=0.0,
                    max_value=99.9,
                    value=float(default_percentage),
                    step=0.5,
                    format="%.2f",
                    help="Percentual de aumento",
                    key="tab2_percentual"
                )

            # Calcular preço de compra
            # Fórmula: V = (P * A - C) / M, onde A = 1 - (percentual/100)
            A_tab2 = 1 - (percentual_tab2 / 100)
            preco_compra_calculado = (preco_venda_tab2 * A_tab2 - custo_tab2) / markup_tab2 if markup_tab2 > 0 and A_tab2 > 0 else 0

            # Calcular métricas
            lucro_bruto_tab2 = preco_venda_tab2 - preco_compra_calculado
            margem_tab2 = ((preco_venda_tab2 - preco_compra_calculado) / preco_venda_tab2 * 100) if preco_venda_tab2 > 0 else 0

            # Formatações
            preco_compra_fmt = f"R$ {preco_compra_calculado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            preco_venda_fmt2 = f"R$ {preco_venda_tab2:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            lucro_fmt2 = f"R$ {lucro_bruto_tab2:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # Validações e avisos
            warnings2 = []
            if default_markup > 0 and markup_tab2 < default_markup:
                warnings2.append(f"Markup ({markup_tab2:.2f}) está abaixo do padrão ({default_markup:.2f})")
            if default_cost > 0 and custo_tab2 < default_cost:
                warnings2.append(f"Custo ({custo_tab2:.2f}) está abaixo do padrão ({default_cost:.2f})")
            if default_percentage > 0 and percentual_tab2 < default_percentage:
                warnings2.append(f"Percentual ({percentual_tab2:.2f}%) está abaixo do padrão ({default_percentage:.2f}%)")

            if warnings2:
                for warning in warnings2:
                    st.warning(f"⚠️ {warning}")

            # Card com resultado
            st.markdown(f"""
            <div style="border: 3px solid #10B981; border-radius: 16px; padding: 30px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); text-align: center; margin: 20px 0;">
                <p style="margin: 0; font-size: 16px; color: #047857; font-weight: 600;">PREÇO DE COMPRA MÁXIMO</p>
                <h1 style="margin: 15px 0; font-size: 48px; color: #10B981;">{preco_compra_fmt}</h1>
                <div style="display: flex; justify-content: center; gap: 40px; margin-top: 15px;">
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #047857;">Preço de Venda</p>
                        <p style="margin: 0; font-size: 18px; color: #9333EA; font-weight: bold;">{preco_venda_fmt2}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #047857;">Lucro Bruto</p>
                        <p style="margin: 0; font-size: 18px; color: #10B981; font-weight: bold;">{lucro_fmt2}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #047857;">Margem</p>
                        <p style="margin: 0; font-size: 18px; color: #F59E0B; font-weight: bold;">{margem_tab2:.1f}%</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ===========================
        # TAB 3: Calcular Markup
        # ===========================
        with tab3:
            # Botão de configuração para admin ou super admin
            if is_admin or is_super_admin:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col3:
                    if st.button("⚙️ Configurações", use_container_width=True, key="config_btn_tab3"):
                        st.session_state.show_markup_config_modal = True

            # Inputs em grid 2x2
            col1, col2 = st.columns(2)

            with col1:
                valor_compra_tab3 = st.number_input(
                    "Valor de Compra (V)",
                    min_value=0.01,
                    value=100.0,
                    step=0.01,
                    format="%.2f",
                    help="Valor de compra do produto",
                    key="tab3_valor"
                )

                preco_venda_tab3 = st.number_input(
                    "Preço de Venda Desejado (P)",
                    min_value=0.01,
                    value=250.0,
                    step=0.01,
                    format="%.2f",
                    help="Preço de venda que você deseja alcançar",
                    key="tab3_preco_venda"
                )

            with col2:
                custo_tab3 = st.number_input(
                    "Custo Adicional (C)",
                    min_value=0.0,
                    value=float(default_cost),
                    step=0.01,
                    format="%.2f",
                    help="Custo adicional fixo",
                    key="tab3_custo"
                )

                percentual_tab3 = st.number_input(
                    "Percentual de Aumento (%)",
                    min_value=0.0,
                    max_value=99.9,
                    value=float(default_percentage),
                    step=0.5,
                    format="%.2f",
                    help="Percentual de aumento",
                    key="tab3_percentual"
                )

            # Calcular markup necessário
            # Fórmula: M = (P * A - C) / V, onde A = 1 - (percentual/100)
            A_tab3 = 1 - (percentual_tab3 / 100)
            markup_calculado = (preco_venda_tab3 * A_tab3 - custo_tab3) / valor_compra_tab3 if valor_compra_tab3 > 0 and A_tab3 > 0 else 0

            # Calcular métricas
            lucro_bruto_tab3 = preco_venda_tab3 - valor_compra_tab3
            margem_tab3 = ((preco_venda_tab3 - valor_compra_tab3) / preco_venda_tab3 * 100) if preco_venda_tab3 > 0 else 0

            # Formatações
            preco_venda_fmt3 = f"R$ {preco_venda_tab3:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            lucro_fmt3 = f"R$ {lucro_bruto_tab3:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # Validações e avisos
            warnings3 = []
            if default_markup > 0 and markup_calculado < default_markup:
                warnings3.append(f"Markup calculado ({markup_calculado:.2f}) está abaixo do padrão ({default_markup:.2f})")
            if default_cost > 0 and custo_tab3 < default_cost:
                warnings3.append(f"Custo ({custo_tab3:.2f}) está abaixo do padrão ({default_cost:.2f})")
            if default_percentage > 0 and percentual_tab3 < default_percentage:
                warnings3.append(f"Percentual ({percentual_tab3:.2f}%) está abaixo do padrão ({default_percentage:.2f}%)")

            if warnings3:
                for warning in warnings3:
                    st.warning(f"⚠️ {warning}")

            # Card com resultado
            st.markdown(f"""
            <div style="border: 3px solid #F59E0B; border-radius: 16px; padding: 30px; background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); text-align: center; margin: 20px 0;">
                <p style="margin: 0; font-size: 16px; color: #92400E; font-weight: 600;">MARKUP NECESSÁRIO</p>
                <h1 style="margin: 15px 0; font-size: 48px; color: #F59E0B;">{markup_calculado:.2f}x</h1>
                <div style="display: flex; justify-content: center; gap: 40px; margin-top: 15px;">
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #92400E;">Preço de Venda</p>
                        <p style="margin: 0; font-size: 18px; color: #9333EA; font-weight: bold;">{preco_venda_fmt3}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #92400E;">Lucro Bruto</p>
                        <p style="margin: 0; font-size: 18px; color: #10B981; font-weight: bold;">{lucro_fmt3}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #92400E;">Margem</p>
                        <p style="margin: 0; font-size: 18px; color: #10B981; font-weight: bold;">{margem_tab3:.1f}%</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Modal de configuração
        if st.session_state.get("show_markup_config_modal", False):
            _render_config_modal(platform_settings_use_cases, settings)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
