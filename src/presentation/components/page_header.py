import streamlit as st


def render_page_header(page_title: str = None):
    """
    Renders a page header with company name and optional page title.

    Args:
        page_title: Optional page title to display alongside company name
    """
    company_name = None

    if "impersonating_company" in st.session_state:
        company_name = st.session_state.impersonating_company
    else:
        if "company_name" not in st.session_state:
            try:
                from dependencies import get_container

                current_user = st.session_state.get("current_user")

                if current_user and not current_user.is_super_admin:
                    container = get_container()
                    admin_use_cases = container.admin_use_cases
                    company = admin_use_cases.get_company(current_user.company_id)
                    if company:
                        st.session_state.company_name = company.name
                        company_name = company.name
            except Exception:
                pass
        else:
            company_name = st.session_state.company_name

    if company_name:
        if page_title:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 0px 30px 20px 30px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                    <h1 style="
                        color: white;
                        margin: 0;
                        font-size: 32px;
                        font-weight: 700;
                    ">{company_name}</h1>
                    <p style="
                        color: rgba(255, 255, 255, 0.9);
                        margin: 5px 0 0 0;
                        font-size: 16px;
                    ">{page_title}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px 30px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                    <h1 style="
                        color: white;
                        margin: 0;
                        font-size: 32px;
                        font-weight: 700;
                    ">{company_name}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif page_title:
        st.title(page_title)
