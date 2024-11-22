import streamlit as st
import pandas as pd
import datetime
import os

# Archivos para persistencia
USUARIOS_FILE = "usuarios.csv"
COMENTARIOS_FILE = "comentarios.csv"

# Departamentos disponibles
DEPARTAMENTOS = ["Dirección", "Originación de crédito", "Cobranza virtual",
                 "Cobranza campo", "Venta en tienda", "Sistemas",
                 "Desarrollo", "Riesgos", "Recursos humanos"]

# Cargar usuarios
def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        return pd.read_csv(USUARIOS_FILE)
    else:
        return pd.DataFrame(columns=["Usuario", "Contraseña", "Departamento"])

# Guardar usuarios
def guardar_usuarios(usuarios):
    usuarios.to_csv(USUARIOS_FILE, index=False)

# Cargar comentarios
def cargar_comentarios():
    if os.path.exists(COMENTARIOS_FILE):
        comentarios = pd.read_csv(COMENTARIOS_FILE)
        if "Estado" not in comentarios.columns:
            comentarios["Estado"] = "En espera de ser atendido"  # Estado por defecto
        if "Respuesta" not in comentarios.columns:
            comentarios["Respuesta"] = ""  # Respuesta vacía por defecto
        comentarios["Respuesta"] = comentarios["Respuesta"].fillna("Sin respuesta")  # Reemplazar NaN por "Sin respuesta"
        return comentarios
    else:
        return pd.DataFrame(columns=["Usuario", "Departamento", "Comentario", "FechaHora", "Foro", "Estado", "Respuesta"])

# Guardar comentarios
def guardar_comentarios(comentarios):
    comentarios.to_csv(COMENTARIOS_FILE, index=False)

# Pantalla de inicio
def pantalla_inicio():
    st.title("Torre de Control - Inicio de Sesión")
    usuarios = cargar_usuarios()

    opcion = st.radio("Selecciona una opción:", ["Iniciar sesión", "Registrarse"])

    if opcion == "Iniciar sesión":
        usuario = st.text_input("Usuario")
        contraseña = st.text_input("Contraseña", type="password")

        if st.button("Iniciar sesión"):
            if usuario in usuarios["Usuario"].values:
                datos_usuario = usuarios[usuarios["Usuario"] == usuario].iloc[0]
                if datos_usuario["Contraseña"] == contraseña:
                    st.session_state["usuario"] = usuario
                    st.session_state["departamento"] = datos_usuario["Departamento"]
                    st.session_state["autenticado"] = True
                else:
                    st.error("Contraseña incorrecta.")
            else:
                st.error("Usuario no encontrado.")
    elif opcion == "Registrarse":
        pantalla_registro()

# Pantalla de registro
def pantalla_registro():
    st.title("Registrar nueva cuenta")
    usuarios = cargar_usuarios()

    nuevo_usuario = st.text_input("Nombre de usuario")
    nueva_contraseña = st.text_input("Contraseña", type="password")
    departamento = st.selectbox("Selecciona tu departamento", DEPARTAMENTOS)
    master_key = st.text_input("Clave maestra", type="password")

    if st.button("Registrar"):
        if master_key != "soygay1":
            st.error("Clave maestra incorrecta. No puedes registrarte.")
        elif nuevo_usuario in usuarios["Usuario"].values:
            st.error("El usuario ya existe. Intenta con otro nombre.")
        else:
            nuevo_usuario_data = pd.DataFrame(
                [{"Usuario": nuevo_usuario, "Contraseña": nueva_contraseña, "Departamento": departamento}]
            )
            usuarios = pd.concat([usuarios, nuevo_usuario_data], ignore_index=True)
            guardar_usuarios(usuarios)
            st.success("¡Usuario registrado con éxito! Ahora puedes iniciar sesión.")

# Mostrar la pantalla principal
def pantalla_principal():
    st.sidebar.title("TORRE DE CONTROL VB")
    st.sidebar.markdown(f"**Bienvenido, {st.session_state['usuario']}!**")
    pagina = st.sidebar.radio("Selecciona un departamento", DEPARTAMENTOS)
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["autenticado"] = False
        return

    if pagina == "Dirección":
        st.title("Resumen General - Dirección")
        st.metric("Indicador Global", "85%", "5%")
        st.metric("KPI Clave", "10,000 USD", "-500 USD")
    elif pagina == "Originación de crédito":
        st.title("KPIs - Originación de Crédito")
        st.metric("Créditos aprobados", "120", "+15")
        st.metric("Monto originado", "2,000,000 USD", "+200,000 USD")
    elif pagina == "Cobranza virtual":
        st.title("KPIs - Cobranza Virtual")
        st.metric("Cobros efectivos", "75%", "+5%")
        st.metric("Tiempo promedio de contacto", "1 min", "-10 sec")
    elif pagina == "Cobranza campo":
        st.title("KPIs - Cobranza Campo")
        st.metric("Recuperación", "90%", "+10%")
        st.metric("Visitas realizadas", "300", "+50")
        st.components.v1.iframe("https://lookerstudio.google.com/reporting/5d9046c5-a483-4e9e-8dce-0200342da70d", height=600)
    elif pagina == "Venta en tienda":
        st.title("KPIs - Venta en Tienda")
        st.metric("Ventas totales", "500,000 USD", "+50,000 USD")
        st.metric("Clientes atendidos", "5,000", "+500")
    elif pagina == "Sistemas":
        st.title("KPIs - Sistemas")
        st.metric("Tiempo de respuesta", "2 horas", "-30 min")
        st.metric("Tickets resueltos", "95%", "+5%")
    elif pagina == "Desarrollo":
        st.title("KPIs - Desarrollo")
        st.metric("Proyectos completados", "8", "+2")
        st.metric("Horas invertidas", "200 horas", "+20 horas")
    elif pagina == "Riesgos":
        st.title("KPIs - Riesgos")
        st.metric("Riesgos mitigados", "95%", "+10%")
        st.metric("Alertas activadas", "10", "-2")
    elif pagina == "Recursos humanos":
        st.title("KPIs - Recursos Humanos")
        st.metric("Contrataciones", "15", "+5")
        st.metric("Capacitaciones", "8", "+2")

    mostrar_foro(pagina)

# Función para mostrar el foro
def mostrar_foro(departamento):
    if f"mostrar_foro_{departamento}" not in st.session_state:
        st.session_state[f"mostrar_foro_{departamento}"] = False

    if st.button("Abrir/Cerrar foro"):
        st.session_state[f"mostrar_foro_{departamento}"] = not st.session_state[f"mostrar_foro_{departamento}"]

    if st.session_state[f"mostrar_foro_{departamento}"]:
        comentarios = cargar_comentarios()
        comentarios_departamento = comentarios[comentarios["Foro"] == departamento]

        st.title(f"Foro del departamento: {departamento}")
        for index, row in comentarios_departamento.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                indicador_estado = {
                    "Rechazado": "🔴",
                    "En proceso": "🟡",
                    "Resuelto": "🟢"
                }.get(row["Estado"], "⚪")
                st.markdown(
                    f"**{row['Usuario']} ({row['Departamento']})** - *{row['FechaHora']}*\n> {row['Comentario']}\n\n**Estado:** {indicador_estado} {row['Estado']}"
                )
                if f"ver_respuesta_{index}" not in st.session_state:
                    st.session_state[f"ver_respuesta_{index}"] = False
                if st.button("Ver respuesta", key=f"ver_respuesta_button_{index}"):
                    st.session_state[f"ver_respuesta_{index}"] = not st.session_state[f"ver_respuesta_{index}"]
                if st.session_state[f"ver_respuesta_{index}"]:
                    st.markdown(f"**Respuesta:** {row['Respuesta']}")
            with col2:
                if st.session_state["departamento"] == departamento:
                    nuevo_estado = st.selectbox(
                        "Cambiar estado",
                        ["En espera de ser atendido", "Rechazado", "En proceso", "Resuelto"],
                        index=["En espera de ser atendido", "Rechazado", "En proceso", "Resuelto"].index(row["Estado"]),
                        key=f"estado_{index}"
                    )
                    nueva_respuesta = st.text_area(
                        "Responder",
                        row["Respuesta"] if row["Respuesta"] != "Sin respuesta" else "",
                        key=f"respuesta_{index}"
                    )
                    if st.button("Actualizar", key=f"actualizar_{index}"):
                        comentarios.loc[index, "Estado"] = nuevo_estado
                        comentarios.loc[index, "Respuesta"] = nueva_respuesta if nueva_respuesta.strip() else "Sin respuesta"
                        guardar_comentarios(comentarios)
                        st.experimental_rerun()

        nuevo_comentario = st.text_area("Añade un comentario:", key=f"nuevo_comentario_{departamento}")
        if st.button("Enviar comentario", key=f"enviar_comentario_{departamento}"):
            if nuevo_comentario.strip():
                nuevo_comentario_data = pd.DataFrame(
                    [{
                        "Usuario": st.session_state["usuario"],
                        "Departamento": st.session_state["departamento"],
                        "Comentario": nuevo_comentario.strip(),
                        "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Foro": departamento,
                        "Estado": "En espera de ser atendido",
                        "Respuesta": "Sin respuesta"
                    }]
                )
                comentarios = pd.concat([comentarios, nuevo_comentario_data], ignore_index=True)
                guardar_comentarios(comentarios)
                st.success("Comentario enviado.")
                st.experimental_rerun()

# Main
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    pantalla_inicio()
else:
    pantalla_principal()
