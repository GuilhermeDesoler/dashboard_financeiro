"""
Authentication Persistence Module
Handles saving and loading authentication tokens using query parameters
"""
import streamlit as st
from datetime import datetime
import json


def save_auth_to_session_state(access_token: str, refresh_token: str, user):
    """
    Save authentication data to session state with persistence flag

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


def restore_auth_if_exists():
    """
    Check if authentication exists in session state and is still valid
    If refresh token exists, try to refresh the access token
    """
    from dependencies import get_container

    # If already authenticated, nothing to do
    if st.session_state.get("is_authenticated", False):
        return True

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
    Clear authentication session from session state
    """
    keys_to_clear = [
        "access_token",
        "refresh_token",
        "current_user",
        "is_authenticated",
        "auth_timestamp",
        "impersonate_token",
        "impersonating_company",
        "impersonate_start_time",
        "company_name"
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
