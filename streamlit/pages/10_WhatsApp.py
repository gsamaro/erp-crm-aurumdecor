import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import configure_page, page_header, render_sidebar, section_title

configure_page("WhatsApp", "💬")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("WhatsApp", "Integrações e conversas.", breadcrumb="Integração / WhatsApp")
section_title("Status", "Monitoramento das integrações.")
st.warning("Integração pendente. Configure o webhook para ativar este módulo.")
section_title("Conversas", "Histórico de conversas.")
st.info("Página em construção. Em breve você poderá gerenciar conversas aqui.")
