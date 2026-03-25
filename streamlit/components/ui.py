from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import html
from typing import Iterable, Sequence

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
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap');
        :root {
            --color-primary: #6B8E23;
            --color-secondary: #E8E3D9;
            --color-accent: #D4A5A5;
            --color-bg: #FAFAF9;
            --color-card: #FFFFFF;
            --color-border: #E5E7EB;
            --color-text: #2F2F2F;
            --color-text-muted: #6B7280;
            --color-success: #22C55E;
            --color-warning: #F59E0B;
            --color-danger: #EF4444;
            --shadow-soft: 0 12px 30px rgba(17, 24, 39, 0.08);
        }
        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif;
            color: var(--color-text);
        }
        body {
            font-size: 15px;
        }
        .stApp {
            background: var(--color-bg);
        }
        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }
        [data-testid="stSidebar"] {
            background: var(--color-card);
            border-right: 1px solid var(--color-border);
        }
        [data-testid="stSidebar"] * {
            color: var(--color-text) !important;
        }
        .panel-card {
            background: transparent;
            border: none;
            border-top: 1px solid #111111;
            border-radius: 0;
            padding: 1.25rem 0 0;
            box-shadow: none;
            margin: 1.25rem 0;
        }
        .kpi-card {
            background: var(--color-card);
            border: 1px solid var(--color-border);
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            box-shadow: var(--shadow-soft);
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            min-height: 110px;
        }
        .kpi-card .kpi-label {
            color: var(--color-text-muted);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .kpi-card .kpi-value {
            font-size: 1.7rem;
            font-weight: 700;
        }
        .kpi-card .kpi-delta {
            font-size: 0.85rem;
            color: var(--color-text-muted);
        }
        .status-tag {
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }
        .status-success { background: rgba(34, 197, 94, 0.16); color: var(--color-success); }
        .status-warning { background: rgba(245, 158, 11, 0.16); color: var(--color-warning); }
        .status-danger { background: rgba(239, 68, 68, 0.16); color: var(--color-danger); }
        .status-info { background: rgba(212, 165, 165, 0.18); color: #9B6E6E; }
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--color-card);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: var(--shadow-soft);
        }
        .custom-table thead th {
            text-align: left;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--color-text-muted);
            background: #F4F3EF;
            padding: 0.9rem 1rem;
        }
        .custom-table tbody td {
            padding: 0.95rem 1rem;
            border-top: 1px solid var(--color-border);
            font-size: 0.92rem;
        }
        .custom-table tbody tr:hover {
            background: rgba(107, 142, 35, 0.06);
        }
        .action-pill {
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(107, 142, 35, 0.12);
            color: var(--color-primary);
            font-size: 0.75rem;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
        }
        div.stButton > button {
            border-radius: 10px;
            border: 1px solid var(--color-border);
            background: var(--color-secondary);
            color: var(--color-text);
            padding: 0.6rem 1.1rem;
            font-weight: 600;
        }
        div.stButton > button[kind="primary"] {
            background: var(--color-primary);
            color: #FFFFFF;
            border: none;
        }
        div.stButton > button:hover {
            filter: brightness(0.98);
        }
        .stMarkdown, .stCaption, .stTextInput label, .stSelectbox label,
        .stTextArea label, .stNumberInput label, .stDateInput label {
            color: var(--color-text) !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: var(--color-text) !important;
        }
        a, a:visited {
            color: var(--color-text) !important;
        }
        [data-testid="stPageLink"],
        [data-testid="stPageLink"] span,
        [data-testid="stSidebar"] a,
        [data-testid="stSidebar"] span {
            color: var(--color-text) !important;
        }
        [data-testid="stSidebar"] svg {
            fill: var(--color-text) !important;
            color: var(--color-text) !important;
        }
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary span {
            color: var(--color-text) !important;
        }
        .stCaption {
            color: var(--color-text-muted) !important;
            font-size: 1.15rem;
            line-height: 1.55;
            font-weight: 500;
        }
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea,
        div[data-baseweb="select"] > div {
            background: var(--color-card) !important;
            color: var(--color-text) !important;
            border: 1px solid var(--color-border) !important;
            border-radius: 10px !important;
        }
        div[data-baseweb="input"] input::placeholder,
        div[data-baseweb="textarea"] textarea::placeholder {
            color: var(--color-text-muted) !important;
        }
        div[data-baseweb="select"] > div > div {
            color: var(--color-text) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(current_file: str) -> None:
    st.sidebar.title("ERP Aurum Decor")
    st.sidebar.caption("Painel de gestão")
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
    if secondary_label:
        spacer, secondary_col, primary_col = st.columns([6, 1.2, 1.2])
        secondary = secondary_col.button(secondary_label)
        primary = primary_col.button(primary_label, type="primary")
        return primary, secondary
    _, primary_col = st.columns([8, 1.2])
    primary = primary_col.button(primary_label, type="primary")
    return primary, False


@dataclass(frozen=True)
class HtmlBlock:
    value: str


def status_tag(label: str, tone: str = "info") -> HtmlBlock:
    tone_class = {
        "success": "status-success",
        "warning": "status-warning",
        "danger": "status-danger",
        "info": "status-info",
    }.get(tone, "status-info")
    return HtmlBlock(
        f'<span class="status-tag {tone_class}">{html.escape(label)}</span>'
    )


def action_pill(label: str) -> HtmlBlock:
    return HtmlBlock(f'<span class="action-pill">{html.escape(label)}</span>')


def kpi_card(label: str, value: str, delta: str | None = None) -> HtmlBlock:
    delta_html = f'<div class="kpi-delta">{html.escape(delta)}</div>' if delta else ""
    return HtmlBlock(
        """
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta}
        </div>
        """.format(
            label=html.escape(label),
            value=html.escape(value),
            delta=delta_html,
        )
    )


def render_kpi_row(items: Sequence[HtmlBlock]) -> None:
    if not items:
        return
    cols = st.columns(len(items))
    for col, item in zip(cols, items, strict=False):
        col.markdown(item.value, unsafe_allow_html=True)


@contextmanager
def card_container() -> Iterable[None]:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    yield
    st.markdown("</div>", unsafe_allow_html=True)


def render_table(
    data: Sequence[dict],
    columns: Sequence[tuple[str, str]],
    empty_message: str = "Sem dados para exibir.",
) -> None:
    if not data:
        st.info(empty_message)
        return

    header_cells = "".join(f"<th>{html.escape(label)}</th>" for label, _ in columns)
    rows_html: list[str] = []
    for row in data:
        cells = []
        for _, key in columns:
            value = row.get(key, "-")
            if isinstance(value, HtmlBlock):
                cell = value.value
            else:
                cell = html.escape(str(value))
            cells.append(f"<td>{cell}</td>")
        rows_html.append(f"<tr>{''.join(cells)}</tr>")

    table_html = f"""
    <table class="custom-table">
        <thead><tr>{header_cells}</tr></thead>
        <tbody>{''.join(rows_html)}</tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)


def render_timeline(items: Sequence[dict]) -> None:
    if not items:
        st.info("Sem interacoes registradas.")
        return
    timeline_items = []
    for item in items:
        title = html.escape(str(item.get("title", "Interacao")))
        date = html.escape(str(item.get("date", "")))
        description = html.escape(str(item.get("description", "")))
        timeline_items.append(
            f"""
            <div style="display:flex; gap:0.75rem; margin-bottom:1rem;">
                <div style="width:10px; height:10px; background:var(--color-primary); border-radius:50%; margin-top:0.35rem;"></div>
                <div>
                    <div style="font-weight:600;">{title}</div>
                    <div style="color:var(--color-text-muted); font-size:0.85rem;">{date}</div>
                    <div style="margin-top:0.3rem;">{description}</div>
                </div>
            </div>
            """
        )
    st.markdown("".join(timeline_items), unsafe_allow_html=True)


def render_kanban(columns: Sequence[dict]) -> None:
    try:
        from streamlit_elements import elements, mui

        with elements("kanban"):
            with mui.Stack(direction="row", spacing=2, alignItems="flex-start"):
                for column in columns:
                    with mui.Box(
                        sx={
                            "minWidth": 240,
                            "backgroundColor": "#F4F3EF",
                            "borderRadius": "16px",
                            "padding": "16px",
                        }
                    ):
                        mui.Typography(
                            column.get("title", ""),
                            sx={"fontWeight": 700, "marginBottom": "12px"},
                        )
                        for card in column.get("items", []):
                            with mui.Paper(
                                elevation=0,
                                sx={
                                    "padding": "12px",
                                    "borderRadius": "12px",
                                    "border": "1px solid #E5E7EB",
                                    "marginBottom": "10px",
                                    "backgroundColor": "#FFFFFF",
                                },
                            ):
                                mui.Typography(card.get("title", ""))
                                if card.get("subtitle"):
                                    mui.Typography(
                                        card.get("subtitle", ""),
                                        sx={"color": "#6B7280", "fontSize": "0.8rem"},
                                    )
        return
    except Exception:
        pass

    cols = st.columns(len(columns))
    for col, column in zip(cols, columns, strict=False):
        with col:
            st.markdown(
                f"<div class=\"panel-card\"><strong>{html.escape(column.get('title', ''))}</strong>",
                unsafe_allow_html=True,
            )
            for card in column.get("items", []):
                st.markdown(
                    f'<div class="kpi-card" style="margin-top:0.75rem;">'
                    f"<div class=\"kpi-label\">{html.escape(card.get('subtitle', ''))}</div>"
                    f"<div class=\"kpi-value\" style=\"font-size:1rem;\">{html.escape(card.get('title', ''))}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)
