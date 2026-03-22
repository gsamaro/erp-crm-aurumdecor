import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.api import request
from components.navigation import resolve_page_path
from components.session import enforce_session

st.set_page_config(page_title="Clientes", page_icon="🧑‍💼")

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

st.title("Clientes")

st.subheader("Cadastrar cliente")
with st.form("create_client"):
    name = st.text_input("Nome")
    phone = st.text_input("Telefone")
    email = st.text_input("Email")
    status = st.selectbox("Status", options=["active", "inactive"], index=0)
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
        st.success("Cliente cadastrado")
    except Exception as exc:
        st.error(f"Erro ao cadastrar: {exc}")

st.divider()

st.subheader("Lista de clientes")
try:
    token = st.session_state.get("access_token")
    clients = request("GET", "/clients", token=token)
except Exception as exc:
    st.error(f"Erro ao carregar clientes: {exc}")
    clients = []

if clients:
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
                    st.success("Cliente atualizado")
                except Exception as exc:
                    st.error(f"Erro ao atualizar: {exc}")
else:
    st.info("Nenhum cliente cadastrado ainda.")
