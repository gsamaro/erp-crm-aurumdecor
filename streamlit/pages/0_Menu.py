import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import configure_page, page_header, render_sidebar, section_title

configure_page("Menu", "📋")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Menu", "Selecione uma opção para continuar.", breadcrumb="Início")

section_title("Administração")

st.page_link(resolve_page_path("2_Usuarios.py", __file__), label="Usuários", icon="👤")
section_title("CRM")
st.page_link(
    resolve_page_path("3_Clientes.py", __file__), label="Clientes", icon="🧑‍💼"
)
