import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import configure_page, page_header, render_sidebar, section_title

configure_page("Estoque", "📦")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Estoque", "Controle de estoque e movimentações.", breadcrumb="Estoque / Movimentações")
section_title("Filtros", "Filtre por produto, status e período.")
st.columns([2, 2, 2, 4])
section_title("Ações", "Registre movimentações de estoque.")
st.columns([1, 1, 6])
section_title("Movimentações", "Histórico de movimentações.")
st.info("Página em construção. Em breve você poderá controlar o estoque aqui.")
