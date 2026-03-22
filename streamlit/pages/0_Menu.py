import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.navigation import resolve_page_path
from components.session import enforce_session

st.set_page_config(page_title="Menu", page_icon="📋")

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))

st.title("Menu")
st.caption("Selecione uma opção")

st.page_link(resolve_page_path("2_Usuarios.py", __file__), label="Usuários", icon="👤")
st.page_link(
    resolve_page_path("3_Clientes.py", __file__), label="Clientes", icon="🧑‍💼"
)
