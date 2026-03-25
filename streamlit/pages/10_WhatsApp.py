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

configure_page("WhatsApp", "💬")
render_sidebar(__file__)

if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

page_header("WhatsApp", "Integrações e conversas.", breadcrumb="Integração / WhatsApp")

render_kpi_row(
    [
        kpi_card("Conversas", "124"),
        kpi_card("Mensagens hoje", "38"),
        kpi_card("Leads", "16"),
        kpi_card("Tempo médio", "12 min"),
    ]
)

section_title("Status", "Monitoramento das integrações.")
with card_container():
    st.warning("Integração pendente. Configure o webhook para ativar este módulo.")

section_title("Ações", "Gerencie mensagens e integrações.")
action_bar("Nova mensagem", "Sincronizar")

section_title("Conversas", "Histórico de conversas.")
with card_container():
    render_table(
        [
            {
                "client": "Ana Oliveira",
                "last": "Hoje 10:40",
                "status": status_tag("Em andamento", "info"),
                "channel": "WhatsApp",
            },
            {
                "client": "Bruno Silva",
                "last": "Ontem 17:20",
                "status": status_tag("Finalizado", "success"),
                "channel": "WhatsApp",
            },
        ],
        columns=[
            ("Cliente", "client"),
            ("Última mensagem", "last"),
            ("Status", "status"),
            ("Canal", "channel"),
        ],
        empty_message="Sem conversas registradas.",
    )
