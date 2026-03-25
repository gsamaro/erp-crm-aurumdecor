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
)

configure_page("Relatórios", "📊")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Relatórios", "Indicadores e exportações.", breadcrumb="Relatórios")

render_kpi_row(
    [
        kpi_card("Relatórios", "12"),
        kpi_card("Última exportação", "Ontem"),
        kpi_card("Automatizações", "3"),
    ]
)

section_title("Filtros", "Selecione período e módulos para gerar relatórios.")
with card_container():
    filter_col1, filter_col2, filter_col3, _ = st.columns([2, 2, 2, 3])
    filter_col1.date_input("Período")
    filter_col2.selectbox("Módulo", ["Todos", "Financeiro", "Eventos", "Estoque"])
    filter_col3.selectbox("Formato", ["PDF", "CSV", "XLSX"])

section_title("Ações", "Gere relatórios com um clique.")
action_bar("Gerar relatório", "Exportar")

section_title("Relatórios", "Relatórios disponíveis.")
with card_container():
    render_table(
        [
            {
                "report": "Fluxo de caixa",
                "module": "Financeiro",
                "period": "Mar/2024",
            },
            {
                "report": "Lucro por evento",
                "module": "Eventos",
                "period": "Fev/2024",
            },
        ],
        columns=[
            ("Relatório", "report"),
            ("Módulo", "module"),
            ("Período", "period"),
        ],
        empty_message="Sem relatórios disponíveis.",
    )
