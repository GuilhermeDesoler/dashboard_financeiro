"""
Authentication Persistence Module
Handles saving and loading authentication tokens using localStorage
"""
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import json


def save_auth_to_session_state(access_token: str, refresh_token: str, user):
    """
    Save authentication data to session state and localStorage for persistence

    Args:
        access_token: JWT access token
        refresh_token: JWT refresh token
        user: User object
    """
    st.session_state.access_token = access_token
    st.session_state.refresh_token = refresh_token
    st.session_state.current_user = user
    st.session_state.is_authenticated = True
    st.session_state.auth_timestamp = datetime.now().isoformat()

    # Persist to localStorage
    _save_to_local_storage(access_token, refresh_token, user)


def restore_auth_if_exists():
    """
    Check if authentication exists in session state or localStorage
    If refresh token exists, try to refresh the access token
    """
    from dependencies import get_container

    # If already authenticated, nothing to do
    if st.session_state.get("is_authenticated", False):
        return True

    # Try to load from localStorage first
    if "refresh_token" not in st.session_state:
        # Note: localStorage loading via components.html is async and complex
        # For now, we rely on session_state persistence
        pass

    # Check if we have a refresh token
    if "refresh_token" in st.session_state and st.session_state.refresh_token:
        try:
            container = get_container()
            auth_use_cases = container.auth_use_cases
            http_client = container.http_client

            # Try to refresh the token
            auth_token = auth_use_cases.refresh_token(st.session_state.refresh_token)

            # Update session state with new tokens
            save_auth_to_session_state(
                auth_token.token,
                auth_token.refresh_token,
                auth_token.user
            )

            # Set token in HTTP client
            http_client.set_auth_token(auth_token.token)

            return True

        except Exception:
            # Refresh failed, clear invalid session
            clear_auth_session()
            return False

    return False


def clear_auth_session():
    """
    Clear authentication session from session state and localStorage
    """
    keys_to_clear = [
        "access_token",
        "refresh_token",
        "current_user",
        "is_authenticated",
        "auth_timestamp",
        "impersonate_token",
        "impersonating_company",
        "company_name"
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    # Clear localStorage
    _clear_local_storage()


def _save_to_local_storage(access_token: str, refresh_token: str, user):
    """
    Save authentication data to browser localStorage

    Args:
        access_token: JWT access token
        refresh_token: JWT refresh token
        user: User object
    """
    user_dict = {
        "email": user.email,
        "name": user.name,
        "company_id": user.company_id,
        "is_super_admin": user.is_super_admin,
        "is_active": user.is_active,
        "role_ids": user.role_ids or [],
        "features": user.features or [],
        "id": getattr(user, "id", None)
    }

    auth_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_dict,
        "timestamp": datetime.now().isoformat()
    }

    js_code = f"""
    <script>
        localStorage.setItem('dashboard_auth', JSON.stringify({json.dumps(auth_data)}));
    </script>
    """
    components.html(js_code, height=0)


def _load_from_local_storage():
    """
    Load authentication data from browser localStorage

    Returns:
        Dict with auth data or None if not found
    """
    js_code = """
    <script>
        const authData = localStorage.getItem('dashboard_auth');
        if (authData) {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: JSON.parse(authData)
            }, '*');
        } else {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: null
            }, '*');
        }
    </script>
    """
    return components.html(js_code, height=0)


def _clear_local_storage():
    """
    Clear authentication data from browser localStorage
    """
    js_code = """
    <script>
        localStorage.removeItem('dashboard_auth');
    </script>
    """
    components.html(js_code, height=0)
