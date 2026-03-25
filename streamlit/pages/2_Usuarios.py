import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from components.api import request
from components.navigation import resolve_page_path
from components.session import enforce_session
from components.ui import (
    action_bar,
    action_pill,
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

configure_page("Usuários", "👤")
render_sidebar(__file__)
page_header(
    "Usuários",
    "Gerencie os usuários administrativos do sistema.",
    breadcrumb="Admin / Usuários",
)

token = st.session_state.get("access_token")
if not enforce_session(st.session_state):
    st.switch_page(resolve_page_path("1_Login.py", __file__))
    st.stop()

token = st.session_state.get("access_token")
try:
    users = request("GET", "/users", token=token)
except Exception as exc:
    st.error(f"Erro ao carregar usuários: {exc}")
    users = []

render_kpi_row(
    [
        kpi_card("Usuários", str(len(users))),
        kpi_card("Perfil", "Admin"),
        kpi_card("Última atualização", "Hoje"),
    ]
)

section_title("Filtros", "Refine a lista por nome ou email.")
with card_container():
    filter_col1, filter_col2, _ = st.columns([2, 2, 3])
    filter_name = filter_col1.text_input("Nome", placeholder="Buscar por nome")
    filter_email = filter_col2.text_input("Email", placeholder="Buscar por email")

section_title("Ações", "Crie novos usuários com permissões de admin.")
action_bar("Novo usuário")

section_title("Cadastro", "Inclua um novo usuário administrador.")
with card_container():
    with st.form("create_user"):
        form_col1, form_col2 = st.columns(2)
        name = form_col1.text_input("Nome")
        email = form_col2.text_input("Email")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Salvar")

if submitted:
    try:
        request(
            "POST",
            "/auth/register",
            json={"name": name, "email": email, "password": password},
            token=token,
        )
        st.toast("Usuário criado", icon="✅")
    except Exception as exc:
        st.error(f"Erro ao criar usuário: {exc}")

section_title("Usuários", "Lista atual de usuários cadastrados.")
if filter_name:
    users = [u for u in users if filter_name.lower() in u["name"].lower()]
if filter_email:
    users = [u for u in users if filter_email.lower() in u["email"].lower()]

table_rows = [
    {
        "name": user.get("name", "-"),
        "email": user.get("email", "-"),
        "status": status_tag("Ativo", "success"),
        "actions": action_pill("Editar"),
    }
    for user in users
]

with card_container():
    render_table(
        table_rows,
        columns=[
            ("Nome", "name"),
            ("Email", "email"),
            ("Status", "status"),
            ("Ações", "actions"),
        ],
        empty_message="Nenhum usuário cadastrado ainda.",
    )
