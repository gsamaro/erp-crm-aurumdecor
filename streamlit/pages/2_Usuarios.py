import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.api import request
from components.navigation import resolve_page_path
from components.session import enforce_session

st.set_page_config(page_title="Usuários", page_icon="👤")

st.title("Usuários")

token = st.session_state.get("access_token")
if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

token = st.session_state.get("access_token")

st.subheader("Novo usuário")
st.caption("Apenas admins podem criar usuários.")
with st.form("create_user"):
    name = st.text_input("Nome")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    submitted = st.form_submit_button("Criar")

if submitted:
    try:
        request(
            "POST",
            "/auth/register",
            json={"name": name, "email": email, "password": password},
            token=token,
        )
        st.success("Usuário criado")
    except Exception as exc:
        st.error(f"Erro ao criar usuário: {exc}")

st.subheader("Lista de usuários")
try:
    users = request("GET", "/users", token=token)
    st.dataframe(users)
except Exception as exc:
    st.error(f"Erro ao carregar usuários: {exc}")
