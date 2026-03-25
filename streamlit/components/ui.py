from __future__ import annotations

import streamlit as st

from components.navigation import resolve_page_path

NAV_ITEMS = [
    ("Menu", "0_Menu.py", "📋"),
    ("Usuarios", "2_Usuarios.py", "👤"),
    ("Clientes", "3_Clientes.py", "🧑‍💼"),
    ("Produtos", "4_Produtos.py", "📦"),
    ("Estoque", "5_Estoque.py", "📦"),
    ("Eventos", "6_Eventos.py", "📅"),
    ("Orcamentos", "7_Orcamentos.py", "🧾"),
    ("Financeiro", "8_Financeiro.py", "💳"),
    ("Relatorios", "9_Relatorios.py", "📊"),
    ("WhatsApp", "10_WhatsApp.py", "💬"),
]


def configure_page(title: str, icon: str) -> None:
    st.set_page_config(
        page_title=f"ERP Aurum Decor • {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        .block-container {padding-top: 2rem; padding-bottom: 2rem;}
        .stDataFrame {border-radius: 8px;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(current_file: str) -> None:
    st.sidebar.title("ERP Aurum Decor")
    st.sidebar.caption("Painel de gestao")
    for label, filename, icon in NAV_ITEMS:
        st.sidebar.page_link(
            resolve_page_path(filename, current_file), label=label, icon=icon
        )


def page_header(title: str, description: str, breadcrumb: str | None = None) -> None:
    if breadcrumb:
        st.caption(breadcrumb)
    st.title(title)
    st.write(description)


def section_title(title: str, description: str | None = None) -> None:
    st.subheader(title)
    if description:
        st.caption(description)


def action_bar(primary_label: str, secondary_label: str | None = None):
    columns = st.columns([1, 1, 6])
    primary = columns[0].button(primary_label, type="primary")
    secondary = False
    if secondary_label:
        secondary = columns[1].button(secondary_label)
    return primary, secondary
