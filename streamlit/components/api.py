import os

import httpx
import streamlit as st


def get_api_base_url() -> str:
    secrets_url = None
    try:
        secrets_url = st.secrets.get("API_BASE_URL")
    except Exception:
        secrets_url = None
    return secrets_url or os.getenv("API_BASE_URL", "http://localhost:8000")


def get_token() -> str | None:
    return st.session_state.get("access_token")


def request(method: str, path: str, token: str | None = None, **kwargs):
    base_url = get_api_base_url()
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with httpx.Client(base_url=base_url, timeout=10) as client:
        response = client.request(method, path, headers=headers, **kwargs)
    response.raise_for_status()
    return response.json()
