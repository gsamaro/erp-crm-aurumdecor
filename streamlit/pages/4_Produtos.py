import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import (
    action_bar,
    card_container,
    configure_page,
    kpi_card,
    page_header,
    render_kpi_row,
    render_sidebar,
    render_table,
    section_title,
    status_tag,
)

configure_page("Produtos", "📦")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header(
    "Produtos", "Cadastro e gestão de produtos.", breadcrumb="Estoque / Produtos"
)

render_kpi_row(
    [
        kpi_card("Produtos", "128"),
        kpi_card("Em estoque", "92"),
        kpi_card("Amortizando", "36"),
        kpi_card("Custos mês", "R$ 18k"),
    ]
)

section_title("Filtros", "Filtre produtos por nome, status ou categoria.")
with card_container():
    filter_col1, filter_col2, filter_col3, _ = st.columns([2, 2, 2, 3])
    filter_col1.text_input("Produto", placeholder="Buscar por nome")
    filter_col2.selectbox(
        "Categoria", ["Todas", "Decoração", "Estrutura", "Iluminação"]
    )
    filter_col3.selectbox("Status", ["Todos", "Ativo", "Inativo"])

section_title("Ações", "Configure novos produtos e amortização.")
action_bar("Novo produto", "Importar")

section_title("Cadastro", "Registre novos produtos e custos.")
with card_container():
    with st.form("produto"):
        form_col1, form_col2 = st.columns(2)
        form_col1.text_input("Nome do produto")
        form_col1.number_input("Quantidade", min_value=0, step=1)
        form_col2.text_input("Categoria")
        form_col2.number_input("Custo total", min_value=0.0, step=100.0)
        st.text_input("Vida útil (eventos)")
        st.form_submit_button("Salvar")

section_title("Produtos", "Lista atual de produtos cadastrados.")
with card_container():
    render_table(
        [
            {
                "name": "Arranjo Verde Oliva",
                "category": "Decoração",
                "stock": "18",
                "status": status_tag("Ativo", "success"),
            },
            {
                "name": "Painel Floral",
                "category": "Estrutura",
                "stock": "6",
                "status": status_tag("Ativo", "success"),
            },
        ],
        columns=[
            ("Produto", "name"),
            ("Categoria", "category"),
            ("Estoque", "stock"),
            ("Status", "status"),
        ],
        empty_message="Sem produtos cadastrados.",
    )
