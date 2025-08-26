import streamlit as st

def student_dashboard(username, logout_callback):
    st.title("Dashboard de Estudiante")
    st.write(f"Bienvenido, {username}")
    if st.button("Cerrar sesión"):
        logout_callback()
