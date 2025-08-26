import streamlit as st
from packages.crud.users import get_all_users, get_all_roles, create_user, update_user, delete_user

def admin_dashboard(username, logout_callback):
    st.title("Dashboard de Administrador")
    st.write(f"Bienvenido, {username}")

    st.header("Gestión de usuarios")

    users = get_all_users()
    roles = get_all_roles()
    role_options = {r[1]: r[0] for r in roles}

    st.subheader("Usuarios existentes")
    st.table([{'ID': u[0], 'Usuario': u[1], 'Rol': u[2]} for u in users])

    action = st.selectbox("Acción", ["Crear usuario", "Editar usuario", "Eliminar usuario"])

    if action == "Crear usuario":
        with st.form("create_user_form"):
            new_username = st.text_input("Nuevo usuario")
            new_password = st.text_input("Contraseña", type="password")
            new_role = st.selectbox("Rol", list(role_options.keys()))
            submitted = st.form_submit_button("Crear")
            if submitted:
                if new_username and new_password:
                    success = create_user(new_username, new_password, role_options[new_role])
                    if success:
                        st.success("Usuario creado correctamente")
                        st.rerun()
                    else:
                        st.error("No se pudo crear el usuario (¿usuario ya existe?)")
                else:
                    st.warning("Completa todos los campos")

    elif action == "Editar usuario":
        user_ids = [str(u[0]) for u in users]
        if user_ids:
            selected_id = st.selectbox("Selecciona ID de usuario", user_ids, key="edit_select_id")
            selected_user = next((u for u in users if str(u[0]) == selected_id), None)
            if selected_user:
                with st.form("edit_user_form"):
                    edit_username = st.text_input("Editar usuario", value=selected_user[1])
                    edit_password = st.text_input("Nueva contraseña (opcional)", type="password")
                    edit_role = st.selectbox("Editar rol", list(role_options.keys()), index=list(role_options.keys()).index(selected_user[2]))
                    submitted = st.form_submit_button("Actualizar")
                    if submitted:
                        update_user(int(selected_id), edit_username, edit_password, role_options[edit_role])
                        st.success("Usuario actualizado")
                        st.rerun()
        else:
            st.info("No hay usuarios para editar.")

    elif action == "Eliminar usuario":
        user_ids = [str(u[0]) for u in users]
        if user_ids:
            selected_id = st.selectbox("Selecciona ID de usuario", user_ids, key="delete_select_id")
            selected_user = next((u for u in users if str(u[0]) == selected_id), None)
            if selected_user:
                st.write(f"Usuario: {selected_user[1]}, Rol: {selected_user[2]}")
                if st.button("Eliminar usuario"):
                    delete_user(int(selected_id))
                    st.success("Usuario eliminado")
                    st.rerun()
        else:
            st.info("No hay usuarios para eliminar.")

    if st.button("Cerrar sesión"):
        logout_callback()
