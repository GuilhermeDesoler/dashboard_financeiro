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
                    markup_percentage=new_percentage  # Envia em % inteira, back divide por 100
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
        tab1, = st.tabs(["Calculadora de Markup"])

        with tab1:
            # Botão de configuração para admin ou super admin
            if is_admin or is_super_admin:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col3:
                    if st.button("⚙️ Configurações", use_container_width=True):
                        st.session_state.show_markup_config_modal = True

            # Inputs em grid 2x2
            col1, col2 = st.columns(2)

            with col1:
                valor_compra = st.number_input(
                    "Valor de Compra (V)",
                    min_value=0.01,
                    value=1.0,
                    step=0.01,
                    format="%.2f",
                    help="Valor de compra do produto",
                    key="calc_valor"
                )

                custo = st.number_input(
                    "Custo Adicional (C)",
                    min_value=0.0,
                    value=float(default_cost),
                    step=0.01,
                    format="%.2f",
                    help="Custo adicional fixo",
                    key="calc_custo"
                )

            with col2:
                markup = st.number_input(
                    "Markup (M)",
                    min_value=0.0,
                    value=float(default_markup) if default_markup > 0 else 2.0,
                    step=0.1,
                    format="%.2f",
                    help="Multiplicador de markup",
                    key="calc_markup"
                )

                percentual = st.number_input(
                    "Percentual de Aumento (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(default_percentage),
                    step=0.5,
                    format="%.2f",
                    help="Percentual de aumento",
                    key="calc_percentual"
                )

            # Validações e avisos
            warnings = []
            if default_markup > 0 and markup < default_markup:
                warnings.append(f"Markup ({markup:.2f}) está abaixo do padrão ({default_markup:.2f})")
            if default_cost > 0 and custo < default_cost:
                warnings.append(f"Custo ({custo:.2f}) está abaixo do padrão ({default_cost:.2f})")
            if default_percentage > 0 and percentual < default_percentage:
                warnings.append(f"Percentual ({percentual:.2f}%) está abaixo do padrão ({default_percentage:.2f}%)")

            # Mostrar avisos
            if warnings:
                for warning in warnings:
                    st.warning(f"⚠️ {warning}")

            # Calcular resultado
            A = 1 -(percentual / 100)
            preco_venda = (valor_compra * markup + custo) / A

            # Card com resultado
            preco_formatado = f"R$ {preco_venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            lucro_bruto = preco_venda - valor_compra
            lucro_fmt = f"R$ {lucro_bruto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            margem = ((preco_venda - valor_compra) / preco_venda * 100) if preco_venda > 0 else 0

            st.markdown(f"""
            <div style="border: 3px solid #9333EA; border-radius: 16px; padding: 30px; background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); text-align: center; margin: 20px 0;">
                <p style="margin: 0; font-size: 16px; color: #6b21a8; font-weight: 600;">PREÇO DE VENDA</p>
                <h1 style="margin: 15px 0; font-size: 48px; color: #9333EA;">{preco_formatado}</h1>
                <div style="display: flex; justify-content: center; gap: 40px; margin-top: 15px;">
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #6b21a8;">Lucro Bruto</p>
                        <p style="margin: 0; font-size: 18px; color: #10B981; font-weight: bold;">{lucro_fmt}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #6b21a8;">Margem</p>
                        <p style="margin: 0; font-size: 18px; color: #10B981; font-weight: bold;">{margem:.1f}%</p>
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
