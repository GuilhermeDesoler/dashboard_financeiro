"""
Credit Purchase (Crediário) Management View
"""
import streamlit as st
from datetime import datetime, date, timedelta
from dependencies import get_container


def render():
    """Main Crediário page"""

    container = get_container()
    credit_use_cases = container.credit_purchase_use_cases

    st.title("Crediário")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Compras", "Nova Compra"])

    # TAB 1: Dashboard
    with tab1:
        render_dashboard(credit_use_cases)

    # TAB 2: Lista de Compras
    with tab2:
        render_purchases_list(credit_use_cases)

    # TAB 3: Nova Compra
    with tab3:
        render_new_purchase_form(credit_use_cases)


def render_dashboard(credit_use_cases):
    """Dashboard with installments by date"""
    st.subheader("Parcelas do Período", divider=False)

    # Date filters
    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input(
            "Data Inicial",
            value=date.today().replace(day=1),
            key="dashboard_start_date"
        )

    with col2:
        end_date = st.date_input(
            "Data Final",
            value=date.today() + timedelta(days=30),
            key="dashboard_end_date"
        )

    with col3:
        status_filter = st.selectbox(
            "Status",
            options=["Todos", "Pendente", "Pago", "Atrasado"],
            key="dashboard_status"
        )

    try:
        # Convert dates to datetime
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        # Get dashboard data
        status_param = None if status_filter == "Todos" else status_filter.lower()

        dashboard_data = credit_use_cases.get_dashboard_by_date(
            start_date=start_datetime,
            end_date=end_datetime,
            status=status_param
        )

        # Summary cards
        summary = dashboard_data["summary"]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Parcelas",
                f"{summary.get('total_parcelas', 0)}",
                f"R$ {summary.get('total_valor', 0.0):,.2f}"
            )

        with col2:
            st.metric(
                "Pagas",
                f"{summary.get('parcelas_pagas', 0)}",
                f"R$ {summary.get('valor_pago', 0.0):,.2f}"
            )

        with col3:
            st.metric(
                "Pendentes",
                f"{summary.get('parcelas_pendentes', 0)}",
                f"R$ {summary.get('valor_pendente', 0.0):,.2f}"
            )

        with col4:
            st.metric(
                "Atrasadas",
                f"{summary.get('parcelas_atrasadas', 0)}",
                f"R$ {summary.get('valor_atrasado', 0.0):,.2f}"
            )

        st.markdown("---")

        # Installments by date
        if dashboard_data["installments_by_date"]:
            for date_group in dashboard_data["installments_by_date"]:
                # Count by status
                installments = date_group["installments"]
                paid_count = sum(1 for inst in installments if inst.status == "pago")
                overdue_count = sum(1 for inst in installments if inst.status == "atrasado")
                pending_count = sum(1 for inst in installments if inst.status == "pendente")

                status_info = []
                if paid_count > 0:
                    status_info.append(f"✅ {paid_count} paga(s)")
                if pending_count > 0:
                    status_info.append(f"⏳ {pending_count} pendente(s)")
                if overdue_count > 0:
                    status_info.append(f"⚠️ {overdue_count} atrasada(s)")

                status_text = " | ".join(status_info) if status_info else ""

                with st.expander(
                    f"📅 {date_group['data_vencimento']} - R$ {date_group['total_dia']:,.2f} ({date_group['quantidade_parcelas']} parcela(s)) - {status_text}",
                    expanded=False
                ):
                    for inst in installments:
                        render_installment_card(inst, credit_use_cases)
        else:
            st.info("Nenhuma parcela encontrada no período selecionado")

    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {str(e)}")


def render_installment_card(installment, credit_use_cases):
    """Render a single installment card"""
    status_icons = {
        "pago": "✅",
        "pendente": "🕐",
        "atrasado": "⚠️",
        "cancelado": "🚫"
    }

    status_colors = {
        "pago": "#E8F5E9",
        "pendente": "#FFF9C4",
        "atrasado": "#FFEBEE",
        "cancelado": "#F5F5F5"
    }

    icon = status_icons.get(installment.status, "")
    color = status_colors.get(installment.status, "#FFFFFF")

    # Card HTML
    st.markdown(
        f"""
        <div style="
            background-color: {color};
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid {'#4CAF50' if installment.status == 'pago' else '#F44336' if installment.status == 'atrasado' else '#FFC107'};
            margin-bottom: 10px;
        ">
            <strong>{icon} {installment.pagante_nome}</strong> - {installment.descricao_compra}<br>
            <strong>Parcela:</strong> {installment.numero_parcela} •
            <strong>Valor:</strong> R$ {installment.valor_total:,.2f} •
            <strong>Status:</strong> {installment.status.capitalize()}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Actions
    if installment.status in ["pendente", "atrasado"]:
        col1, col2, col3 = st.columns([2, 1, 1])

        with col2:
            if st.button(
                "💰 Registrar Pagamento",
                key=f"pay_{installment.id}",
                use_container_width=True,
                type="primary"
            ):
                st.session_state[f"show_payment_modal_{installment.id}"] = True
                st.rerun()

        with col3:
            if st.button(
                "Ver Detalhes",
                key=f"details_{installment.id}",
                use_container_width=True
            ):
                st.session_state["selected_purchase_id"] = installment.credit_purchase_id
                st.rerun()

        # Payment modal
        if st.session_state.get(f"show_payment_modal_{installment.id}"):
            render_payment_modal(installment, credit_use_cases)


def render_payment_modal(installment, credit_use_cases):
    """Modal for registering payment"""

    st.markdown("### Registrar Pagamento")

    with st.form(key=f"payment_form_{installment.id}"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Cliente:** {installment.pagante_nome}")
            st.markdown(f"**Parcela:** {installment.numero_parcela}")
            st.markdown(f"**Valor original:** R$ {installment.valor_parcela:,.2f}")

        with col2:
            payment_date = st.date_input(
                "Data do Pagamento",
                value=date.today(),
                key=f"payment_date_{installment.id}"
            )

        # Get modalities
        container = get_container()
        modalities = container.payment_modality_use_cases.list_active_modalities()
        modality_options = {m.name: m.id for m in modalities}

        modality_name = st.selectbox(
            "Forma de Pagamento",
            options=list(modality_options.keys()),
            key=f"modality_{installment.id}"
        )

        col1, col2 = st.columns(2)

        with col1:
            juros = st.number_input(
                "Juros (R$)",
                min_value=0.0,
                value=0.0,
                step=0.01,
                key=f"juros_{installment.id}"
            )

        with col2:
            multa = st.number_input(
                "Multa (R$)",
                min_value=0.0,
                value=0.0,
                step=0.01,
                key=f"multa_{installment.id}"
            )

        total = installment.valor_parcela + juros + multa
        st.markdown(f"### Total a pagar: R$ {total:,.2f}")

        observacao = st.text_area(
            "Observação",
            key=f"obs_{installment.id}"
        )

        # Submit button
        submitted = st.form_submit_button("💰 Confirmar Pagamento", use_container_width=True, type="primary")

        if submitted:
            try:
                payment_datetime = datetime.combine(payment_date, datetime.now().time())

                credit_use_cases.pay_installment(
                    purchase_id=installment.credit_purchase_id,
                    installment_id=installment.id,
                    data_pagamento=payment_datetime,
                    modality_id=modality_options[modality_name],
                    valor_juros=juros,
                    valor_multa=multa,
                    observacao=observacao
                )

                st.success("Pagamento registrado com sucesso!")
                del st.session_state[f"show_payment_modal_{installment.id}"]
                st.rerun()

            except Exception as e:
                st.error(f"Erro ao registrar pagamento: {str(e)}")

    # Cancel button outside the form
    if st.button("❌ Cancelar", use_container_width=True, key=f"cancel_payment_{installment.id}"):
        del st.session_state[f"show_payment_modal_{installment.id}"]
        st.rerun()


def render_purchase_details(credit_use_cases, purchase_id):
    """Render detailed view of a credit purchase"""

    # Back button
    if st.button("← Voltar para lista"):
        del st.session_state["selected_purchase_id"]
        st.rerun()

    try:
        # Get purchase details with all installments
        purchase = credit_use_cases.get_purchase_details(purchase_id)

        st.subheader(f"Detalhes da Compra - {purchase.pagante_nome}", divider=True)

        # Purchase information
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 📋 Informações Gerais")
            st.markdown(f"**Cliente:** {purchase.pagante_nome}")
            if purchase.pagante_telefone:
                st.markdown(f"**Telefone:** {purchase.pagante_telefone}")
            if purchase.pagante_documento:
                st.markdown(f"**CPF/CNPJ:** {purchase.pagante_documento}")
            st.markdown(f"**Descrição:** {purchase.descricao_compra}")

        with col2:
            st.markdown("### 💰 Valores")
            st.markdown(f"**Valor Total:** R$ {purchase.valor_total:,.2f}")
            st.markdown(f"**Entrada:** R$ {purchase.valor_entrada:,.2f}")
            st.markdown(f"**Total Pago:** R$ {purchase.total_pago or 0:,.2f}")
            st.markdown(f"**Total Pendente:** R$ {purchase.total_pendente or 0:,.2f}")

        with col3:
            st.markdown("### 📊 Status")
            st.markdown(f"**Status:** {purchase.status.capitalize()}")
            st.markdown(f"**Total de Parcelas:** {purchase.numero_parcelas}")
            st.markdown(f"**Parcelas Pagas:** {purchase.parcelas_pagas or 0}/{purchase.numero_parcelas}")
            st.markdown(f"**Parcelas Atrasadas:** {purchase.parcelas_atrasadas or 0}")
            progress = purchase.percentual_pago if purchase.percentual_pago else 0
            st.progress(progress / 100, text=f"{progress:.1f}% Concluído")

        st.divider()

        # Installments grouped by date
        st.markdown("### 📅 Parcelas")

        if purchase.installments:
            # Group installments by due date
            from collections import defaultdict
            installments_by_date = defaultdict(list)

            for installment in purchase.installments:
                date_str = installment.data_vencimento.strftime("%d/%m/%Y")
                installments_by_date[date_str].append(installment)

            # Sort dates
            sorted_dates = sorted(installments_by_date.keys(), key=lambda x: datetime.strptime(x, "%d/%m/%Y"))

            for date_str in sorted_dates:
                installments = installments_by_date[date_str]
                total_date = sum(inst.valor_total for inst in installments)

                # Count by status
                paid_count = sum(1 for inst in installments if inst.status == "pago")
                overdue_count = sum(1 for inst in installments if inst.status == "atrasado")
                pending_count = sum(1 for inst in installments if inst.status == "pendente")

                status_info = []
                if paid_count > 0:
                    status_info.append(f"✅ {paid_count} paga(s)")
                if pending_count > 0:
                    status_info.append(f"⏳ {pending_count} pendente(s)")
                if overdue_count > 0:
                    status_info.append(f"⚠️ {overdue_count} atrasada(s)")

                status_text = " | ".join(status_info) if status_info else ""

                with st.expander(
                    f"📅 {date_str} - R$ {total_date:,.2f} ({len(installments)} parcela(s)) - {status_text}",
                    expanded=False
                ):
                    for installment in sorted(installments, key=lambda x: x.numero_parcela):
                        render_installment_card(installment, credit_use_cases)
        else:
            st.info("Nenhuma parcela encontrada")

    except Exception as e:
        st.error(f"Erro ao carregar detalhes: {str(e)}")
        if st.button("Voltar"):
            del st.session_state["selected_purchase_id"]
            st.rerun()


def render_purchases_list(credit_use_cases):
    """List of all credit purchases"""

    # Check if a purchase is selected for details
    if st.session_state.get("selected_purchase_id"):
        render_purchase_details(credit_use_cases, st.session_state["selected_purchase_id"])
        return

    st.subheader("Compras no Crediário", divider=False)

    # Filters
    col1, col2 = st.columns([3, 1])

    with col1:
        search_name = st.text_input(
            "Buscar por nome",
            placeholder="Digite o nome do cliente...",
            key="search_purchases"
        )

    with col2:
        status_filter = st.selectbox(
            "Status",
            options=["Todos", "Ativo", "Concluído", "Cancelado"],
            key="purchases_status"
        )

    try:
        status_param = None if status_filter == "Todos" else status_filter.lower()

        purchases_data = credit_use_cases.get_all_purchases(
            status=status_param,
            pagante_nome=search_name if search_name else None,
            page=1,
            per_page=50
        )

        if purchases_data["items"]:
            st.markdown(f"**{purchases_data['total']} compra(s) encontrada(s)**")
            st.markdown("---")

            for purchase in purchases_data["items"]:
                render_purchase_card(purchase, credit_use_cases)
        else:
            st.info("Nenhuma compra encontrada")

    except Exception as e:
        st.error(f"Erro ao carregar compras: {str(e)}")


def render_purchase_card(purchase, credit_use_cases):
    """Render a purchase card"""
    status_icons = {
        "ativo": "🟢",
        "concluido": "✅",
        "cancelado": "🚫"
    }

    status_colors = {
        "ativo": "#E8F5E9",
        "concluido": "#E3F2FD",
        "cancelado": "#F5F5F5"
    }

    icon = status_icons.get(purchase.status, "")
    color = status_colors.get(purchase.status, "#FFFFFF")

    # Progress bar
    progress = purchase.percentual_pago if purchase.percentual_pago else 0

    st.markdown(
        f"""
        <div style="
            background-color: {color};
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #9C27B0;
            margin-bottom: 15px;
        ">
            <h3 style="margin: 0;">{icon} {purchase.pagante_nome}</h3>
            <p style="margin: 5px 0; color: #666;">
                <strong>Descrição:</strong> {purchase.descricao_compra}<br>
                <strong>Valor Total:</strong> R$ {purchase.valor_total:,.2f} •
                <strong>Entrada:</strong> R$ {purchase.valor_entrada:,.2f}<br>
                <strong>Parcelas:</strong> {purchase.numero_parcelas}x •
                <strong>Pagas:</strong> {purchase.parcelas_pagas or 0}/{purchase.numero_parcelas}<br>
                <strong>Progresso:</strong> {progress:.1f}% •
                <strong>Status:</strong> {purchase.status.capitalize()}
            </p>
            <div style="background-color: #E0E0E0; border-radius: 5px; height: 10px; margin: 10px 0;">
                <div style="background-color: #9C27B0; height: 100%; width: {progress}%; border-radius: 5px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "Ver Detalhes",
            key=f"view_purchase_{purchase.id}",
            use_container_width=True,
            type="primary"
        ):
            st.session_state["selected_purchase_id"] = purchase.id
            st.rerun()

    with col2:
        if purchase.status == "ativo" and st.button(
            "Cancelar",
            key=f"cancel_purchase_{purchase.id}",
            use_container_width=True
        ):
            if st.session_state.get(f"confirm_cancel_{purchase.id}"):
                try:
                    credit_use_cases.cancel_purchase(purchase.id)
                    st.success("Compra cancelada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao cancelar: {str(e)}")
            else:
                st.session_state[f"confirm_cancel_{purchase.id}"] = True
                st.warning("Clique novamente para confirmar o cancelamento")


def render_new_purchase_form(credit_use_cases):
    """Form to create new credit purchase"""
    st.subheader("Nova Compra no Crediário", divider=False)

    with st.form("new_purchase_form", clear_on_submit=True):
        st.markdown("#### Dados do Cliente")

        col1, col2 = st.columns(2)

        with col1:
            pagante_nome = st.text_input(
                "Nome Completo *",
                placeholder="João Silva"
            )

        with col2:
            pagante_telefone = st.text_input(
                "Telefone",
                placeholder="(11) 98765-4321"
            )

        pagante_documento = st.text_input(
            "CPF/CNPJ",
            placeholder="123.456.789-00"
        )

        st.markdown("#### Dados da Compra")

        descricao_compra = st.text_area(
            "Descrição da Compra *",
            placeholder="Ex: Geladeira Brastemp 450L"
        )

        col1, col2 = st.columns(2)

        with col1:
            valor_total = st.number_input(
                "Valor Total (R$) *",
                min_value=0.01,
                value=1000.0,
                step=0.01
            )

        with col2:
            valor_entrada = st.number_input(
                "Valor da Entrada (R$)",
                min_value=0.0,
                value=0.0,
                step=0.01
            )

        st.markdown("#### Parcelamento")

        col1, col2, col3 = st.columns(3)

        with col1:
            numero_parcelas = st.number_input(
                "Número de Parcelas *",
                min_value=1,
                max_value=120,
                value=10
            )

        with col2:
            intervalo_dias = st.number_input(
                "Intervalo (dias)",
                min_value=1,
                value=30
            )

        with col3:
            data_inicio = st.date_input(
                "Primeiro Vencimento *",
                value=date.today() + timedelta(days=30)
            )

        taxa_juros = st.number_input(
            "Taxa de Juros Mensal (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1
        )

        st.markdown("**Campos marcados com * são obrigatórios**")

        submitted = st.form_submit_button(
            "Criar Compra",
            use_container_width=True,
            type="primary"
        )

    if submitted:
        if not pagante_nome or not descricao_compra:
            st.error("Preencha todos os campos obrigatórios")
        else:
            try:
                with st.spinner("Criando compra..."):
                    data_inicio_datetime = datetime.combine(data_inicio, datetime.min.time())

                    result = credit_use_cases.create_purchase(
                        pagante_nome=pagante_nome,
                        descricao_compra=descricao_compra,
                        valor_total=valor_total,
                        numero_parcelas=numero_parcelas,
                        data_inicio_pagamento=data_inicio_datetime,
                        valor_entrada=valor_entrada,
                        intervalo_dias=intervalo_dias,
                        taxa_juros_mensal=taxa_juros / 100,
                        pagante_documento=pagante_documento if pagante_documento else None,
                        pagante_telefone=pagante_telefone if pagante_telefone else None
                    )

                    st.success(
                        f"Compra criada com sucesso!\n\n"
                        f"Cliente: {result['credit_purchase'].pagante_nome}\n\n"
                        f"{numero_parcelas} parcelas geradas"
                    )

            except Exception as e:
                st.error(f"Erro ao criar compra: {str(e)}")
