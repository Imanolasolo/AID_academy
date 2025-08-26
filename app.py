import streamlit as st
import sqlite3
from dashboards.admin import admin_dashboard
from dashboards.teacher import teacher_dashboard
from dashboards.parents import parents_dashboard
from dashboards.student import student_dashboard
from packages.auth.service import authenticate_user, get_role_by_username, init_db

st.set_page_config(page_title="AID Academy", page_icon=":book:", layout="wide")

# Inicializar la base de datos al arrancar la app
init_db()

def login_screen():
    col1,col2 = st.columns([1,3])
    with col1:
        st.image("assets/aid_academy_logo.png", width=200)
    with col2:
        st.title("Bienvenidos a la plataforma virtual de :red[AID academy]"
        "")
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        st.image("assets/girl_studying.jpg", width=300)
        with st.expander("Sobre AID academy"):
            st.write("AID Academy es una plataforma de aprendizaje en línea que ofrece cursos y recursos educativos para estudiantes de todas las edades.")
    with col2:
        col1,col2 = st.columns([1,3])
        with col2:
            st.image("assets/login_image.jpg", width=285, )
        with st.expander("Iniciar sesión"):
            if 'login_error' in st.session_state:
                st.error(st.session_state['login_error'])
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            if st.button("Iniciar sesión"):
                token = authenticate_user(username, password)
                if token:
                    st.session_state['username'] = username
                    st.session_state['token'] = token
                    st.session_state['role'] = get_role_by_username(username)
                    st.session_state['login_error'] = ''
                    st.session_state['logged_in'] = True
                else:
                    st.session_state['login_error'] = "Credenciales inválidas"
            # Botón de registro vía WhatsApp
            wa_url = "https://wa.me/593993513082?text=Quiero%20registrarme"
            st.markdown(
                f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366;color:white;padding:8px 16px;border:none;border-radius:4px;">Registrarme vía WhatsApp</button></a>',
                unsafe_allow_html=True
            )
    with col3:
        st.image("assets/follow_steps.jpg", width=300)
        with st.expander("Instrucciones de uso de la app"):
            st.markdown("""
                        1. Para utilizar esta aplicación, inicie sesión con sus credenciales.
                        2. Una vez que haya iniciado sesión, podrá acceder a los recursos y herramientas disponibles según su rol.
                        3. Puede registrarse en la app via WhatsApp con el botón de la pestaña "iniciar sesión".
                        """)

def logout():
    for key in ['username', 'role', 'logged_in', 'login_error', 'token']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def main():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login_screen()
    else:
        role = st.session_state.get('role')
        if role == 'admin':
            admin_dashboard(st.session_state.get('username'), logout)
        elif role == 'teacher':
            teacher_dashboard(st.session_state.get('username'), logout)
        elif role == 'parent':
            parents_dashboard(st.session_state.get('username'), logout)
        elif role == 'student':
            student_dashboard(st.session_state.get('username'), logout)
        else:
            st.error("Rol desconocido")
            logout()

if __name__ == "__main__":
    main()
    # Footer centrado
    st.markdown(
        """
        <div style="text-align: center; margin-top: 3em; color: #888;">
            <small>Proudly created by <strong>CodeCodix 2025</strong></small>
        </div>
        """,
        unsafe_allow_html=True
    )