import streamlit as st

st.set_page_config(page_title="Aurum Decor Admin", page_icon="✨")

st.title("Aurum Decor Admin")
st.caption("Use o menu lateral para navegar.")

st.page_link("pages/1_Login.py", label="Login", icon="🔐")
st.page_link("pages/0_Menu.py", label="Menu", icon="📋")
st.page_link("pages/2_Usuarios.py", label="Usuários", icon="👤")
