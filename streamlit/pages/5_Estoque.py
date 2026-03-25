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

configure_page("Estoque", "📦")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header(
    "Estoque",
    "Controle de estoque e movimentações.",
    breadcrumb="Estoque / Movimentações",
)

render_kpi_row(
    [
        kpi_card("Itens em estoque", "92"),
        kpi_card("Movimentações", "28"),
        kpi_card("Baixas", "6"),
        kpi_card("Reposições", "12"),
    ]
)

section_title("Filtros", "Filtre por produto, status e período.")
with card_container():
    filter_col1, filter_col2, filter_col3, _ = st.columns([2, 2, 2, 3])
    filter_col1.text_input("Produto", placeholder="Buscar por nome")
    filter_col2.selectbox("Tipo", ["Todos", "Entrada", "Saída", "Ajuste"])
    filter_col3.date_input("Período")

section_title("Ações", "Registre movimentações de estoque.")
action_bar("Nova movimentação", "Exportar")

section_title("Registro", "Lance entradas e saídas de estoque.")
with card_container():
    with st.form("estoque"):
        form_col1, form_col2, form_col3 = st.columns(3)
        form_col1.text_input("Produto")
        form_col2.number_input("Quantidade", min_value=1, step=1)
        form_col3.selectbox("Tipo", ["Entrada", "Saída", "Ajuste"])
        st.text_area("Observações")
        st.form_submit_button("Salvar")

section_title("Movimentações", "Histórico de movimentações.")
with card_container():
    render_table(
        [
            {
                "product": "Arranjo Verde Oliva",
                "type": "Entrada",
                "date": "Hoje",
                "status": status_tag("Confirmado", "success"),
            },
            {
                "product": "Painel Floral",
                "type": "Saída",
                "date": "Ontem",
                "status": status_tag("Pendente", "warning"),
            },
        ],
        columns=[
            ("Produto", "product"),
            ("Tipo", "type"),
            ("Data", "date"),
            ("Status", "status"),
        ],
        empty_message="Sem movimentações registradas.",
    )
