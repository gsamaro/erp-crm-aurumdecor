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
    render_kanban,
    render_kpi_row,
    render_sidebar,
    render_table,
    section_title,
    status_tag,
)

configure_page("Orçamentos", "🧾")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Orçamentos", "Gestão de orçamentos e propostas.", breadcrumb="Orçamentos")

render_kpi_row(
    [
        kpi_card("Orçamentos ativos", "12"),
        kpi_card("Enviados", "6"),
        kpi_card("Aprovados", "3"),
        kpi_card("Taxa de conversão", "38%"),
    ]
)

section_title("Filtros", "Filtre por cliente, status e período.")
with card_container():
    filter_col1, filter_col2, filter_col3, _ = st.columns([2, 2, 2, 3])
    filter_col1.text_input("Cliente", placeholder="Buscar por nome")
    filter_col2.selectbox("Status", ["Todos", "Em elaboração", "Enviado", "Aprovado"])
    filter_col3.date_input("Período")

section_title("Ações", "Crie e envie orçamentos.")
action_bar("Novo orçamento", "Enviar")

section_title("Cadastro", "Monte um novo orçamento.")
with card_container():
    with st.form("orcamento"):
        form_col1, form_col2 = st.columns(2)
        form_col1.text_input("Cliente")
        form_col1.date_input("Data")
        form_col2.number_input("Valor total", min_value=0.0, step=500.0)
        form_col2.selectbox("Status", ["Em elaboração", "Enviado", "Aprovado"])
        st.text_area("Observações")
        st.form_submit_button("Salvar")

section_title("Pipeline", "Acompanhe o status dos orçamentos.")
render_kanban(
    [
        {
            "title": "Em elaboração",
            "items": [
                {"title": "Evento corporate", "subtitle": "R$ 8.500"},
                {"title": "Casamento Silva", "subtitle": "R$ 14.000"},
            ],
        },
        {
            "title": "Enviado",
            "items": [{"title": "Aniversário 30 anos", "subtitle": "R$ 6.200"}],
        },
        {
            "title": "Aprovado",
            "items": [{"title": "Evento premium", "subtitle": "R$ 22.000"}],
        },
    ]
)

section_title("Orçamentos", "Lista de orçamentos cadastrados.")
with card_container():
    render_table(
        [
            {
                "client": "Casamento Silva",
                "status": status_tag("Enviado", "info"),
                "value": "R$ 14.000",
                "date": "05/04/2024",
            },
            {
                "client": "Evento Corporate",
                "status": status_tag("Aprovado", "success"),
                "value": "R$ 8.500",
                "date": "02/04/2024",
            },
        ],
        columns=[
            ("Cliente", "client"),
            ("Status", "status"),
            ("Valor", "value"),
            ("Data", "date"),
        ],
        empty_message="Sem orçamentos cadastrados.",
    )
