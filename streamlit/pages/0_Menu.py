import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import (
    card_container,
    configure_page,
    kpi_card,
    page_header,
    render_kpi_row,
    render_sidebar,
    section_title,
)

configure_page("Menu", "📋")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Menu", "Selecione uma opção para continuar.", breadcrumb="Início")

render_kpi_row(
    [
        kpi_card("Módulos ativos", "8"),
        kpi_card("Usuários", "1"),
        kpi_card("Atualizações", "Próxima fase"),
    ]
)

section_title("Administração")
with card_container():
    st.page_link(
        resolve_page_path("2_Usuarios.py", __file__), label="Usuários", icon="👤"
    )

section_title("CRM e Atendimento")
with card_container():
    col1, col2 = st.columns(2)
    with col1:
        st.page_link(
            resolve_page_path("3_Clientes.py", __file__), label="Clientes", icon="🧑‍💼"
        )
    with col2:
        st.page_link(
            resolve_page_path("10_WhatsApp.py", __file__), label="WhatsApp", icon="💬"
        )

section_title("Operações")
with card_container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.page_link(
            resolve_page_path("4_Produtos.py", __file__), label="Produtos", icon="📦"
        )
        st.page_link(
            resolve_page_path("5_Estoque.py", __file__), label="Estoque", icon="📦"
        )
    with col2:
        st.page_link(
            resolve_page_path("6_Eventos.py", __file__), label="Eventos", icon="📅"
        )
        st.page_link(
            resolve_page_path("7_Orcamentos.py", __file__),
            label="Orçamentos",
            icon="🧾",
        )
    with col3:
        st.page_link(
            resolve_page_path("8_Financeiro.py", __file__),
            label="Financeiro",
            icon="💳",
        )
        st.page_link(
            resolve_page_path("9_Relatorios.py", __file__),
            label="Relatórios",
            icon="📊",
        )
