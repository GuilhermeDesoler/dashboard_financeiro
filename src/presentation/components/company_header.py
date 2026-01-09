"""
Company Header Component
Displays the company name and page title at the top of each page
"""
import streamlit as st


def render_company_header(page_title: str = ""):
    """
    Render company header with company name and page title
    Shows impersonated company name if in impersonate mode, otherwise shows user's company

    Args:
        page_title: The title of the current page to display
    """
    # Check if impersonating
    if st.session_state.get("impersonating_company"):
        company_name = st.session_state.get("company_name", "Empresa não identificada")
        is_impersonating = True
    else:
        # Get company name from current user
        current_user = st.session_state.get("current_user")

        # Super admin should not display company header
        if current_user and hasattr(current_user, 'is_super_admin') and current_user.is_super_admin:
            # Super admin without impersonation - skip rendering company header
            return

        if current_user and hasattr(current_user, 'company_id') and current_user.company_id:
            # Try to get company name from session state
            company_name = st.session_state.get("company_name")
            if not company_name:
                # If not in session state, fetch it from API
                try:
                    from dependencies import get_container
                    container = get_container()
                    admin_use_cases = container.admin_use_cases
                    company = admin_use_cases.get_company(current_user.company_id)
                    if company:
                        st.session_state.company_name = company.name
                        company_name = company.name
                    else:
                        company_name = f"Empresa ID: {current_user.company_id}"
                except Exception as e:
                    # Log error for debugging
                    import traceback
                    print(f"Error fetching company: {str(e)}")
                    print(traceback.format_exc())
                    company_name = f"Empresa ID: {current_user.company_id}"
        else:
            company_name = "Empresa não identificada"
        is_impersonating = False

    # Render header with company name and page title
    # Build page title HTML if provided
    page_title_html = ""
    if page_title:
        page_title_html = f'<p style="margin: 8px 0 0 0; font-size: 18px; color: rgba(255, 255, 255, 0.9); font-weight: 500;">{page_title}</p>'

    if is_impersonating:
        html_content = f"""<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 20px 25px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"><div style="display: flex; align-items: center; justify-content: space-between;"><div style="flex: 1;"><p style="margin: 0; font-size: 12px; color: rgba(255, 255, 255, 0.8); font-weight: 500; text-transform: uppercase; letter-spacing: 1px;">🔄 Modo Impersonalização</p><h2 style="margin: 5px 0 0 0; font-size: 28px; color: white; font-weight: 700;">{company_name}</h2>{page_title_html}</div><div style="background: rgba(255, 255, 255, 0.2); border-radius: 8px; padding: 8px 16px;"><p style="margin: 0; font-size: 11px; color: white; font-weight: 600;">IMPERSONANDO</p></div></div></div>"""
        st.markdown(html_content, unsafe_allow_html=True)
    else:
        html_content = f"""<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 20px 25px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"><p style="margin: 0; font-size: 12px; color: rgba(255, 255, 255, 0.8); font-weight: 500; text-transform: uppercase; letter-spacing: 1px;">🏢 Empresa</p><h2 style="margin: 5px 0 0 0; font-size: 28px; color: white; font-weight: 700;">{company_name}</h2>{page_title_html}</div>"""
        st.markdown(html_content, unsafe_allow_html=True)
