import streamlit as st

from components.ui import configure_page, page_header, render_sidebar

configure_page("Home", "🏠")
render_sidebar(__file__)
page_header("ERP Aurum Decor", "Painel administrativo", breadcrumb="Home")
st.info("Use o menu lateral para navegar pelas seções do ERP.")
