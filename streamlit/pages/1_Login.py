import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.api import request
from components.navigation import resolve_page_path
from components.session import enforce_session, refresh_session
from components.ui import configure_page, page_header, render_sidebar, section_title

configure_page("Login", "🔐")
render_sidebar(__file__)
page_header("Login", "Acesse o painel administrativo", breadcrumb="Início / Login")

if enforce_session(st.session_state):
    st.switch_page(resolve_page_path("0_Menu.py", __file__))

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    submitted = st.form_submit_button("Entrar")

login_ok = False
if submitted:
    try:
        response = request(
            "POST", "/auth/login", json={"email": email, "password": password}
        )
        st.session_state["access_token"] = response["access_token"]
        refresh_session(st.session_state)
        st.success("Login realizado")
        login_ok = True
    except Exception as exc:
        st.error(f"Erro ao autenticar: {exc}")

if login_ok:
    st.switch_page(resolve_page_path("0_Menu.py", __file__))

bootstrap_allowed = False
try:
    status = request("GET", "/auth/bootstrap/status")
    bootstrap_allowed = status.get("allowed", False)
except Exception:
    bootstrap_allowed = False

if bootstrap_allowed:
    st.divider()
    section_title(
        "Primeiro acesso (bootstrap)",
        "Crie o primeiro admin caso ainda não exista nenhum usuário.",
    )

    with st.form("bootstrap_form"):
        name = st.text_input("Nome", key="boot_name")
        boot_email = st.text_input("Email", key="boot_email")
        boot_password = st.text_input("Senha", type="password", key="boot_password")
        boot_submit = st.form_submit_button("Criar admin")

    if boot_submit:
        try:
            request(
                "POST",
                "/auth/bootstrap",
                json={"name": name, "email": boot_email, "password": boot_password},
            )
            st.success("Admin criado. Faça login acima.")
        except Exception as exc:
            st.error(f"Erro no bootstrap: {exc}")
