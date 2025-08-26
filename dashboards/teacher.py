import streamlit as st

def teacher_dashboard(username, logout_callback):
    st.title("Dashboard de Profesor")
    st.write(f"Bienvenido, {username}")
    if st.button("Cerrar sesión"):
        logout_callback()
