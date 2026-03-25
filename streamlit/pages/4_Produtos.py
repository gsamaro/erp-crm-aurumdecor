import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import configure_page, page_header, render_sidebar, section_title

configure_page("Produtos", "📦")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Produtos", "Cadastro e gestão de produtos.", breadcrumb="Estoque / Produtos")
section_title("Filtros", "Filtre produtos por nome, status ou categoria.")
st.columns([2, 2, 2, 4])
section_title("Ações", "Configure novos produtos e amortização.")
st.columns([1, 1, 6])
section_title("Produtos", "Lista atual de produtos cadastrados.")
st.info("Página em construção. Em breve você poderá gerenciar produtos aqui.")
