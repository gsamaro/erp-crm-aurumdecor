import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import configure_page, page_header, render_sidebar, section_title

configure_page("Financeiro", "💳")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Financeiro", "Visão financeira e fluxo de caixa.", breadcrumb="Financeiro")
section_title("Indicadores", "Resumo do período.")
metric_cols = st.columns(4)
metric_cols[0].metric("Receita", "R$ 0,00")
metric_cols[1].metric("Despesas", "R$ 0,00")
metric_cols[2].metric("Saldo", "R$ 0,00")
metric_cols[3].metric("Previsto", "R$ 0,00")
section_title("Filtros", "Filtre por período e categoria.")
st.columns([2, 2, 2, 4])
section_title("Ações", "Registre contas a pagar e receber.")
st.columns([1, 1, 6])
section_title("Lançamentos", "Lista de lançamentos financeiros.")
st.info("Página em construção. Em breve você poderá gerenciar o financeiro aqui.")
