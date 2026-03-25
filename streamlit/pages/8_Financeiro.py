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

configure_page("Financeiro", "💳")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("Financeiro", "Visão financeira e fluxo de caixa.", breadcrumb="Financeiro")

render_kpi_row(
    [
        kpi_card("Receita", "R$ 42.300"),
        kpi_card("Despesas", "R$ 18.900"),
        kpi_card("Saldo", "R$ 23.400"),
        kpi_card("Previsto", "R$ 9.200"),
    ]
)

section_title("Filtros", "Filtre por período e categoria.")
with card_container():
    filter_col1, filter_col2, filter_col3, _ = st.columns([2, 2, 2, 3])
    filter_col1.date_input("Período")
    filter_col2.selectbox("Categoria", ["Todas", "Receitas", "Despesas", "Eventos"])
    filter_col3.selectbox("Status", ["Todos", "Pago", "Pendente"])

section_title("Ações", "Registre contas a pagar e receber.")
action_bar("Novo lançamento", "Exportar")

section_title("Cadastro", "Inclua um novo lançamento financeiro.")
with card_container():
    with st.form("financeiro"):
        form_col1, form_col2 = st.columns(2)
        form_col1.text_input("Descrição")
        form_col1.number_input("Valor", min_value=0.0, step=100.0)
        form_col2.selectbox("Tipo", ["Receita", "Despesa"])
        form_col2.date_input("Vencimento")
        st.text_area("Observações")
        st.form_submit_button("Salvar")

section_title("Lançamentos", "Lista de lançamentos financeiros.")
with card_container():
    render_table(
        [
            {
                "description": "Pagamento evento corporate",
                "type": "Receita",
                "value": "R$ 8.500",
                "status": status_tag("Pago", "success"),
            },
            {
                "description": "Compra de flores",
                "type": "Despesa",
                "value": "R$ 1.200",
                "status": status_tag("Pendente", "warning"),
            },
        ],
        columns=[
            ("Descrição", "description"),
            ("Tipo", "type"),
            ("Valor", "value"),
            ("Status", "status"),
        ],
        empty_message="Sem lançamentos cadastrados.",
    )
