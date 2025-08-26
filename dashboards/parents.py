import streamlit as st

def parents_dashboard(username, logout_callback):
    st.title("Dashboard de Padres")
    st.write(f"Bienvenido, {username}")
    if st.button("Cerrar sesión"):
        logout_callback()
