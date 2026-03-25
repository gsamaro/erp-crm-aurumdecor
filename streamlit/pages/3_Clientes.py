import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.api import request
from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import (
    action_bar,
    configure_page,
    page_header,
    render_sidebar,
    section_title,
)

configure_page("Clientes", "🧑‍💼")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header(
    "Clientes",
    "Cadastro e gestão de clientes do CRM.",
    breadcrumb="CRM / Clientes",
)

section_title("Filtros", "Refine a lista de clientes.")
filter_col1, filter_col2, filter_col3, _ = st.columns([2, 2, 2, 3])
filter_name = filter_col1.text_input("Nome", placeholder="Buscar por nome")
filter_email = filter_col2.text_input("Email", placeholder="Buscar por email")
filter_status = filter_col3.selectbox(
    "Status", options=["Todos", "active", "inactive"], index=0
)

section_title("Ações", "Cadastre novos clientes.")
create_clicked, _ = action_bar("Novo cliente")

with st.form("create_client"):
    form_col1, form_col2 = st.columns(2)
    name = form_col1.text_input("Nome")
    phone = form_col1.text_input("Telefone")
    email = form_col2.text_input("Email")
    status = form_col2.selectbox("Status", options=["active", "inactive"], index=0)
    notes = st.text_area("Observações")
    submitted = st.form_submit_button("Salvar")

if submitted:
    try:
        token = st.session_state.get("access_token")
        request(
            "POST",
            "/clients",
            json={
                "name": name,
                "phone": phone or None,
                "email": email or None,
                "status": status,
                "notes": notes or None,
            },
            token=token,
        )
        st.toast("Cliente cadastrado", icon="✅")
    except Exception as exc:
        st.error(f"Erro ao cadastrar: {exc}")

st.divider()

section_title("Clientes", "Lista atual de clientes cadastrados.")
try:
    token = st.session_state.get("access_token")
    clients = request("GET", "/clients", token=token)
except Exception as exc:
    st.error(f"Erro ao carregar clientes: {exc}")
    clients = []

if clients:
    if filter_name:
        clients = [c for c in clients if filter_name.lower() in c["name"].lower()]
    if filter_email:
        clients = [
            c for c in clients if filter_email.lower() in (c.get("email") or "").lower()
        ]
    if filter_status != "Todos":
        clients = [c for c in clients if c.get("status") == filter_status]

    for client in clients:
        with st.expander(f"{client['name']} ({client.get('status', 'active')})"):
            st.write(f"**Telefone:** {client.get('phone') or '-'}")
            st.write(f"**Email:** {client.get('email') or '-'}")
            st.write(f"**Observações:** {client.get('notes') or '-'}")

            with st.form(f"edit_client_{client['id']}"):
                edit_name = st.text_input("Nome", value=client["name"])
                edit_phone = st.text_input("Telefone", value=client.get("phone") or "")
                edit_email = st.text_input("Email", value=client.get("email") or "")
                edit_status = st.selectbox(
                    "Status",
                    options=["active", "inactive"],
                    index=0 if client.get("status") == "active" else 1,
                )
                edit_notes = st.text_area(
                    "Observações", value=client.get("notes") or ""
                )
                updated = st.form_submit_button("Atualizar")

            if updated:
                try:
                    token = st.session_state.get("access_token")
                    request(
                        "PUT",
                        f"/clients/{client['id']}",
                        json={
                            "name": edit_name,
                            "phone": edit_phone or None,
                            "email": edit_email or None,
                            "status": edit_status,
                            "notes": edit_notes or None,
                        },
                        token=token,
                    )
                    st.toast("Cliente atualizado", icon="✅")
                except Exception as exc:
                    st.error(f"Erro ao atualizar: {exc}")
else:
    st.info("Nenhum cliente cadastrado ainda.")
