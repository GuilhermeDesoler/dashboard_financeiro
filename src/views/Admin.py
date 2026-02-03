"""
Admin page - Company management, user creation, and impersonate
"""

import streamlit as st
from dependencies import get_container
from datetime import datetime


def Admin():
    """Admin page for super admins only"""

    container = get_container()
    admin_use_cases = container.admin_use_cases
    auth_use_cases = container.auth_use_cases
    http_client = container.http_client

    current_user = st.session_state.get("current_user")
    if not current_user or not current_user.is_super_admin:
        st.error("Acesso negado. Apenas super admins podem acessar esta página.")
        st.stop()

    st.title("Painel Administrativo")

    tab1, tab2, tab3 = st.tabs(["Empresas", "Criar Usuário", "Criar Empresa"])

    with tab1:
        st.subheader("Empresas Cadastradas", divider=False)

        col_filter1, col_filter2 = st.columns([3, 1])
        with col_filter1:
            search_company = st.text_input(
                "Buscar empresa",
                placeholder="Digite o nome da empresa...",
                label_visibility="collapsed",
            )
        with col_filter2:
            show_inactive = st.checkbox("Mostrar inativas", value=False)

        try:
            companies = admin_use_cases.get_all_companies(only_active=not show_inactive)

            if search_company:
                companies = [
                    c
                    for c in companies
                    if search_company.lower() in c.name.lower()
                    or (c.cnpj and search_company in c.cnpj)
                ]

            if not companies:
                st.info("Nenhuma empresa encontrada")
            else:
                st.markdown(f"**{len(companies)} empresa(s) encontrada(s)**")
                st.markdown("---")

                for i in range(0, len(companies), 2):
                    cols = st.columns(2)

                    for idx, col in enumerate(cols):
                        if i + idx < len(companies):
                            company = companies[i + idx]

                            with col:
                                card_color = (
                                    "#E8F5E9" if company.is_active else "#FFEBEE"
                                )
                                status_text = (
                                    "Ativa" if company.is_active else "Inativa"
                                )

                                plan_colors = {
                                    "basic": "#2196F3",
                                    "premium": "#9C27B0",
                                    "enterprise": "#FF9800",
                                }
                                plan_color = plan_colors.get(company.plan, "#757575")

                                st.markdown(
                                    f"""
                                    <div style="
                                        background-color: {card_color};
                                        padding: 20px;
                                        border-radius: 10px;
                                        border-left: 5px solid {plan_color};
                                        margin-bottom: 15px;
                                        min-height: 200px;
                                    ">
                                        <h3 style="margin: 0; color: #333;">{company.name}</h3>
                                        <strong>Status:</strong>{status_text}<br>
                                        <p style="margin: 5px 0; color: #666;">
                                            <strong>CNPJ:</strong> {company.cnpj or "Não informado"}<br>
                                            <strong>Telefone:</strong> {company.phone or "Não informado"}<br>
                                            <strong>Usuários:</strong> {company.users_count}
                                        </p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                                # Custom CSS for purple button styling
                                st.markdown(
                                    """
                                    <style>
                                    /* Primary button - Purple background with white text */
                                    div[data-testid="stButton"] button[kind="primary"] p {
                                        color: white !important;
                                    }
                                    div[data-testid="stButton"] button[kind="primary"] {
                                        background-color: #9C27B0 !important;
                                        color: white !important;
                                        border: none !important;
                                    }
                                    div[data-testid="stButton"] button[kind="primary"]:hover {
                                        background-color: #7B1FA2 !important;
                                        color: white !important;
                                    }
                                    div[data-testid="stButton"] button[kind="primary"]:hover p {
                                        color: white !important;
                                    }

                                    /* Secondary button - Transparent with purple border and text */
                                    div[data-testid="stButton"] button[kind="secondary"] {
                                        background-color: transparent !important;
                                        color: #9C27B0 !important;
                                        border: 2px solid #9C27B0 !important;
                                    }
                                    div[data-testid="stButton"] button[kind="secondary"] p {
                                        color: #9C27B0 !important;
                                    }
                                    div[data-testid="stButton"] button[kind="secondary"]:hover {
                                        background-color: rgba(156, 39, 176, 0.1) !important;
                                        border-color: #7B1FA2 !important;
                                        color: #7B1FA2 !important;
                                    }
                                    div[data-testid="stButton"] button[kind="secondary"]:hover p {
                                        color: #7B1FA2 !important;
                                    }
                                    </style>
                                """,
                                    unsafe_allow_html=True,
                                )

                                # Impersonate button
                                if company.is_active:
                                    if st.button(
                                        "🎭 Impersonate",
                                        key=f"impersonate_{company.id}",
                                        use_container_width=True,
                                        type="primary",
                                    ):
                                        try:
                                            with st.spinner(
                                                f"Acessando {company.name}..."
                                            ):
                                                # Get impersonate token
                                                impersonate_token = (
                                                    auth_use_cases.impersonate_company(
                                                        company.id,
                                                        st.session_state.access_token,
                                                    )
                                                )

                                                # Store impersonate info
                                                st.session_state.impersonate_token = (
                                                    impersonate_token.token
                                                )
                                                st.session_state.impersonating_company = (
                                                    company.name
                                                )

                                                # Set token in HTTP client
                                                http_client.set_auth_token(
                                                    impersonate_token.token
                                                )

                                                # Redirect to Dashboard
                                                st.session_state.current_page = (
                                                    "Dashboard"
                                                )

                                                st.success(
                                                    f"{impersonate_token.message}\n\n"
                                                    f"Token válido por {impersonate_token.expires_in_hours} horas"
                                                )
                                                st.rerun()

                                        except Exception as e:
                                            st.error(f"Erro ao impersonate: {str(e)}")
                                else:
                                    st.button(
                                        "Empresa Inativa",
                                        key=f"inactive_{company.id}",
                                        use_container_width=True,
                                        disabled=True,
                                    )

        except Exception as e:
            st.error(f"Erro ao carregar empresas: {str(e)}")

    # TAB 2: Create User
    with tab2:
        st.subheader("Criar Novo Usuário", divider=False)

        # Fetch companies for dropdown (outside form to avoid error feedback loop)
        try:
            companies_for_user = admin_use_cases.get_all_companies(only_active=True)
            company_options = {c.name: c.id for c in companies_for_user}
        except Exception as e:
            company_options = {}
            st.error(f"Erro ao carregar empresas: {str(e)}")

        with st.form("create_user_form", clear_on_submit=True):
            user_company = st.selectbox(
                "Empresa *",
                options=list(company_options.keys()) if company_options else [],
                help="Selecione a empresa do usuário",
            )

            col1, col2 = st.columns(2)

            with col1:
                user_name = st.text_input("Nome Completo *", placeholder="João Silva")

            with col2:
                user_email = st.text_input("Email *", placeholder="joao@empresa.com")

            col3, col4 = st.columns(2)

            with col3:
                user_password = st.text_input(
                    "Senha *", type="password", placeholder="Mínimo 6 caracteres"
                )

            with col4:
                user_is_super_admin = st.checkbox(
                    "Super Admin",
                    value=False,
                    help="Marque para criar um super administrador",
                )

            st.markdown("**Campos marcados com * são obrigatórios**")

            submit_user = st.form_submit_button(
                "Criar Usuário", use_container_width=True, type="primary"
            )

        if submit_user:
            if not all([user_company, user_name, user_email, user_password]):
                st.error("Por favor, preencha todos os campos obrigatórios")
            elif len(user_password) < 6:
                st.error("A senha deve ter no mínimo 6 caracteres")
            else:
                try:
                    with st.spinner("Criando usuário..."):
                        company_id = company_options[user_company]

                        created_user = admin_use_cases.create_user(
                            email=user_email,
                            password=user_password,
                            name=user_name,
                            company_id=company_id,
                            is_super_admin=user_is_super_admin,
                        )

                        st.success(
                            f"✅ Usuário criado com sucesso!\n\n"
                            f"**Nome:** {created_user.name}\n\n"
                            f"**Email:** {created_user.email}\n\n"
                            f"**Empresa:** {user_company}\n\n"
                            f"**Super Admin:** {'Sim' if user_is_super_admin else 'Não'}"
                        )

                        # Aguardar um momento para o usuário ver a mensagem
                        import time
                        time.sleep(1.5)
                        st.rerun()

                except Exception as e:
                    error_msg = str(e)
                    if "409" in error_msg or "já existe" in error_msg.lower():
                        st.error("Email já cadastrado no sistema")
                    else:
                        st.error(f"Erro ao criar usuário: {error_msg}")

    # TAB 3: Create Company
    with tab3:
        st.subheader("Criar Nova Empresa", divider=False)

        with st.form("create_company_form", clear_on_submit=True):
            company_name = st.text_input(
                "Nome da Empresa *", placeholder="Empresa ABC Ltda"
            )

            col1, col2 = st.columns(2)

            with col1:
                company_cnpj = st.text_input(
                    "CNPJ", placeholder="12.345.678/0001-90", help="Opcional"
                )

            with col2:
                company_phone = st.text_input(
                    "Telefone", placeholder="(11) 98765-4321", help="Opcional"
                )

            company_plan = st.selectbox(
                "Plano *",
                options=["basic", "premium", "enterprise"],
                index=0,
                format_func=lambda x: {
                    "basic": "Basic",
                    "premium": "Premium",
                    "enterprise": "Enterprise",
                }.get(x, x),
            )

            st.markdown("**Campos marcados com * são obrigatórios**")

            submit_company = st.form_submit_button(
                "Criar Empresa", use_container_width=True, type="primary"
            )

        if submit_company:
            if not company_name:
                st.error("Por favor, preencha o nome da empresa")
            else:
                try:
                    with st.spinner("Criando empresa..."):
                        created_company = admin_use_cases.create_company(
                            name=company_name,
                            cnpj=company_cnpj if company_cnpj else None,
                            phone=company_phone if company_phone else None,
                            plan=company_plan,
                        )

                        st.success(
                            f"✅ Empresa criada com sucesso!\n\n"
                            f"**Nome:** {created_company.name}\n\n"
                            f"**CNPJ:** {created_company.cnpj or 'Não informado'}\n\n"
                            f"**Plano:** {created_company.plan.upper()}\n\n"
                            f"**ID:** {created_company.id}\n\n"
                            f"💡 Agora você pode criar usuários para esta empresa na aba 'Criar Usuário'"
                        )

                        # Aguardar um momento para o usuário ver a mensagem
                        import time
                        time.sleep(1.5)
                        st.rerun()

                except Exception as e:
                    error_msg = str(e)
                    if "409" in error_msg or "já existe" in error_msg.lower():
                        st.error("Empresa com este CNPJ já cadastrada")
                    else:
                        st.error(f"Erro ao criar empresa: {error_msg}")

    # Show impersonate info if active with exit button
    if st.session_state.get("impersonate_token"):
        st.warning(
            f"🎭 **Modo Impersonate Ativo**\n\n"
            f"Você está visualizando a empresa: **{st.session_state.get('impersonating_company')}**"
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(
                "🔙 Sair do Impersonate", use_container_width=True, type="primary"
            ):
                # Clear impersonate data
                del st.session_state.impersonate_token
                del st.session_state.impersonating_company

                # Restore super admin token
                http_client.set_auth_token(st.session_state.access_token)

                # Stay on Admin page
                st.session_state.current_page = "Admin"

                st.success("Modo impersonate desativado")
                st.rerun()
