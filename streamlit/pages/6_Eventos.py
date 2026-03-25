import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import configure_page, page_header, render_sidebar, section_title

configure_page("Eventos", "📅")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Eventos", "Agenda e custos por evento.", breadcrumb="Eventos")
section_title("Filtros", "Filtre eventos por data, cliente e status.")
st.columns([2, 2, 2, 4])
section_title("Ações", "Crie novos eventos e associe produtos.")
st.columns([1, 1, 6])
section_title("Eventos", "Lista de eventos cadastrados.")
st.info("Página em construção. Em breve você poderá gerenciar eventos aqui.")
