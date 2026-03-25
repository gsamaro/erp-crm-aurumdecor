import streamlit as st

from components.ui import (
    action_bar,
    card_container,
    configure_page,
    kpi_card,
    page_header,
    render_kpi_row,
    render_sidebar,
    section_title,
)

configure_page("Home", "🏠")
render_sidebar(__file__)
page_header("ERP Aurum Decor", "Painel administrativo", breadcrumb="Home")

render_kpi_row(
    [
        kpi_card("Eventos do mês", "12"),
        kpi_card("Orçamentos ativos", "8", "+2"),
        kpi_card("Clientes", "328"),
        kpi_card("Receita prevista", "R$ 86k"),
    ]
)

section_title("Ações rápidas", "Inicie o trabalho com poucos cliques.")
action_bar("Novo orçamento", "Novo cliente")

with card_container():
    st.markdown("### Bem-vindo")
    st.write("Use o menu lateral para navegar pelas seções do ERP.")
