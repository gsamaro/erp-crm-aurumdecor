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

configure_page("Eventos", "📅")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Eventos", "Agenda e custos por evento.", breadcrumb="Eventos")

render_kpi_row(
    [
        kpi_card("Eventos do mês", "12"),
        kpi_card("Aprovados", "7"),
        kpi_card("Em produção", "3"),
        kpi_card("Lucro médio", "R$ 4,2k"),
    ]
)

section_title("Filtros", "Filtre eventos por data, cliente e status.")
with card_container():
    filter_col1, filter_col2, filter_col3, _ = st.columns([2, 2, 2, 3])
    filter_col1.text_input("Cliente", placeholder="Buscar por nome")
    filter_col2.date_input("Data")
    filter_col3.selectbox("Status", ["Todos", "Planejado", "Confirmado", "Concluído"])

section_title("Ações", "Crie novos eventos e associe produtos.")
action_bar("Novo evento", "Exportar")

section_title("Cadastro", "Registre novos eventos e custos.")
with card_container():
    with st.form("evento"):
        form_col1, form_col2 = st.columns(2)
        form_col1.text_input("Cliente")
        form_col1.date_input("Data do evento")
        form_col2.text_input("Local")
        form_col2.number_input("Orçamento", min_value=0.0, step=500.0)
        st.text_area("Observações")
        st.form_submit_button("Salvar")

section_title("Eventos", "Lista de eventos cadastrados.")
with card_container():
    render_table(
        [
            {
                "event": "Casamento Oliveira",
                "date": "12/04/2024",
                "status": status_tag("Confirmado", "success"),
                "value": "R$ 12.000",
            },
            {
                "event": "Aniversário 30 anos",
                "date": "20/04/2024",
                "status": status_tag("Planejado", "warning"),
                "value": "R$ 6.800",
            },
        ],
        columns=[
            ("Evento", "event"),
            ("Data", "date"),
            ("Status", "status"),
            ("Valor", "value"),
        ],
        empty_message="Sem eventos cadastrados.",
    )
