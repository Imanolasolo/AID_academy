# AID Academy

AID Academy es una plataforma de aprendizaje en línea desarrollada con Streamlit y SQLite, que permite la gestión de usuarios y dashboards personalizados según el rol (admin, teacher, student, parent).

## Características

- Login seguro con contraseñas encriptadas y autenticación JWT.
- Gestión de usuarios (CRUD) desde el dashboard de administrador.
- Dashboards personalizados para cada tipo de usuario.
- Registro de nuevos usuarios vía WhatsApp.
- Interfaz moderna y responsiva.

## Requisitos

- Python 3.8+
- pip

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tu_usuario/aid_academy.git
   cd aid_academy/edu_domain
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Inicializa la base de datos:
   ```
   python db_setup.py
   ```

## Uso

1. Ejecuta la aplicación:
   ```
   streamlit run app.py
   ```

2. Accede a la interfaz web que se abrirá en tu navegador.

3. Inicia sesión con:
   - Usuario: `admin`
   - Contraseña: `adminpass`

4. Para registrar nuevos usuarios, usa el botón de WhatsApp en la pantalla de login.

## Estructura del proyecto

- `app.py`: Aplicación principal Streamlit.
- `db_setup.py`: Script para inicializar la base de datos.
- `dashboards/`: Dashboards para cada tipo de usuario.
- `packages/auth/`: Servicios de autenticación y gestión de usuarios.
- `packages/crud/`: Funciones CRUD para usuarios y roles.

## Licencia

Proudly created by **CodeCodix 2025**
