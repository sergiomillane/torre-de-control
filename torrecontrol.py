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

ALERTAS_FILE = "alertas.csv"

# Cargar alertas
def cargar_alertas():
    if os.path.exists(ALERTAS_FILE):
        return pd.read_csv(ALERTAS_FILE)
    else:
        return pd.DataFrame(columns=["Departamento", "Descripción", "Estado", "FechaHora", "Respuesta"])

# Guardar alertas
def guardar_alertas(alertas):
    alertas.to_csv(ALERTAS_FILE, index=False)

# Función para contar alertas activas
def contar_detallado_alertas(departamento):
    alertas = cargar_alertas()
    estados = alertas[alertas["Departamento"] == departamento]["Estado"].value_counts().to_dict()
    return {
        "Nueva": estados.get("Nueva", 0),
        "En proceso": estados.get("En proceso", 0),
        "Resuelta": estados.get("Resuelta", 0),
    }

def contar_detallado_tickets(departamento):
    tickets = cargar_comentarios()
    estados = tickets[tickets["Foro"] == departamento]["Estado"].value_counts().to_dict()
    return {
        "En espera de ser atendido": estados.get("En espera de ser atendido", 0),
        "Rechazado": estados.get("Rechazado", 0),
        "En proceso": estados.get("En proceso", 0),
        "Resuelto": estados.get("Resuelto", 0),
    }

def mostrar_indicador_superior(detallado_alertas, detallado_tickets):
    alertas_html = (
        f"{detallado_alertas['Nueva']} 🔴 "
        f"{detallado_alertas['En proceso']} 🟡 "
        f"{detallado_alertas['Resuelta']} 🟢"
    )
    tickets_html = (
        f"{detallado_tickets['En espera de ser atendido']} ⚪ "
        f"{detallado_tickets['Rechazado']} 🔴 "
        f"{detallado_tickets['En proceso']} 🟡 "
        f"{detallado_tickets['Resuelto']} 🟢"
    )
    
    st.markdown(
        f"""
        <style>
            .indicadores-superiores {{
                position: fixed;
                top: 70px;
                right: 10px;
                display: flex;
                gap: 15px;
                z-index: 1000;
            }}
            .indicador {{
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: bold;
                color: white;
                font-size: 14px;
                text-align: center;
            }}
            .alertas {{
                background-color: #ff4d4d;
            }}
            .tickets {{
                background-color: #4da6ff;
            }}
        </style>
        <div class="indicadores-superiores">
            <div class="indicador alertas">
                <b>Alertas:</b> {alertas_html}
            </div>
            <div class="indicador tickets">
                <b>Tickets:</b> {tickets_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



# Función para generar alertas automáticas
def generar_alertas(departamento):
    alertas = cargar_alertas()

    # Verificar condiciones específicas para cada departamento
    if departamento == "Originación de crédito":
        if 120 > 100:  # Ejemplo: Créditos aprobados sobre umbral
            descripcion = "Altos índices de rechazo en créditos."
            if not ((alertas["Departamento"] == departamento) & (alertas["Descripción"] == descripcion)).any():
                nueva_alerta = {
                    "Departamento": departamento,
                    "Descripción": descripcion,
                    "Estado": "Nueva",
                    "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Respuesta": "Sin respuesta"
                }
                alertas = pd.concat([alertas, pd.DataFrame([nueva_alerta])], ignore_index=True)

    elif departamento == "Cobranza virtual":
        if 75 < 80:  # Ejemplo: Cobros efectivos por debajo del objetivo
            descripcion = "Cobros efectivos por debajo del objetivo."
            if not ((alertas["Departamento"] == departamento) & (alertas["Descripción"] == descripcion)).any():
                nueva_alerta = {
                    "Departamento": departamento,
                    "Descripción": descripcion,
                    "Estado": "Nueva",
                    "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Respuesta": "Sin respuesta"
                }
                alertas = pd.concat([alertas, pd.DataFrame([nueva_alerta])], ignore_index=True)

    elif departamento == "Cobranza campo":
        if 90 < 95:  # Ejemplo: Recuperación por debajo del umbral
            descripcion = "Recuperación por debajo del umbral esperado."
            if not ((alertas["Departamento"] == departamento) & (alertas["Descripción"] == descripcion)).any():
                nueva_alerta = {
                    "Departamento": departamento,
                    "Descripción": descripcion,
                    "Estado": "Nueva",
                    "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Respuesta": "Sin respuesta"
                }
                alertas = pd.concat([alertas, pd.DataFrame([nueva_alerta])], ignore_index=True)

    elif departamento == "Venta en tienda":
        if 500000 < 550000:  # Ejemplo: Ventas totales bajas
            descripcion = "Ventas totales menores al objetivo semanal."
            if not ((alertas["Departamento"] == departamento) & (alertas["Descripción"] == descripcion)).any():
                nueva_alerta = {
                    "Departamento": departamento,
                    "Descripción": descripcion,
                    "Estado": "Nueva",
                    "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Respuesta": "Sin respuesta"
                }
                alertas = pd.concat([alertas, pd.DataFrame([nueva_alerta])], ignore_index=True)

    elif departamento == "Sistemas":
        if 95 < 98:  # Ejemplo: Tickets resueltos por debajo del estándar
            descripcion = "Tickets resueltos por debajo del estándar."
            if not ((alertas["Departamento"] == departamento) & (alertas["Descripción"] == descripcion)).any():
                nueva_alerta = {
                    "Departamento": departamento,
                    "Descripción": descripcion,
                    "Estado": "Nueva",
                    "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Respuesta": "Sin respuesta"
                }
                alertas = pd.concat([alertas, pd.DataFrame([nueva_alerta])], ignore_index=True)

    elif departamento == "Desarrollo":
        if 8 < 10:  # Ejemplo: Proyectos completados por debajo del objetivo
            descripcion = "Proyectos completados menores al objetivo."
            if not ((alertas["Departamento"] == departamento) & (alertas["Descripción"] == descripcion)).any():
                nueva_alerta = {
                    "Departamento": departamento,
                    "Descripción": descripcion,
                    "Estado": "Nueva",
                    "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Respuesta": "Sin respuesta"
                }
                alertas = pd.concat([alertas, pd.DataFrame([nueva_alerta])], ignore_index=True)

    elif departamento == "Riesgos":
        if 10 > 5:  # Ejemplo: Alertas activadas por encima del límite
            descripcion = "Altas alertas activadas en el sistema."
            if not ((alertas["Departamento"] == departamento) & (alertas["Descripción"] == descripcion)).any():
                nueva_alerta = {
                    "Departamento": departamento,
                    "Descripción": descripcion,
                    "Estado": "Nueva",
                    "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Respuesta": "Sin respuesta"
                }
                alertas = pd.concat([alertas, pd.DataFrame([nueva_alerta])], ignore_index=True)

    elif departamento == "Recursos humanos":
        if 15 < 20:  # Ejemplo: Contrataciones por debajo del objetivo
            descripcion = "Contrataciones por debajo del objetivo mensual."
            if not ((alertas["Departamento"] == departamento) & (alertas["Descripción"] == descripcion)).any():
                nueva_alerta = {
                    "Departamento": departamento,
                    "Descripción": descripcion,
                    "Estado": "Nueva",
                    "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Respuesta": "Sin respuesta"
                }
                alertas = pd.concat([alertas, pd.DataFrame([nueva_alerta])], ignore_index=True)

    guardar_alertas(alertas)

# Mostrar alertas activas
# Mostrar alertas activas
def mostrar_alertas(departamento):
    alertas = cargar_alertas()
    alertas_departamento = alertas[alertas["Departamento"] == departamento]
    st.subheader("Alertas Activas")

    for index, row in alertas_departamento.iterrows():
        # Cambiar color de fondo según estado
        color_estado = {
            "Nueva": "red",
            "En proceso": "#FFD700",  # Amarillo más tenue
            "Resuelta": "green"
        }.get(row["Estado"], "white")

        # Mostrar la alerta con colores
        st.markdown(
            f"<div style='background-color: {color_estado}; padding: 10px; border-radius: 5px;'>"
            f"**{row['Descripción']}** - *Estado: {row['Estado']}*"
            f"</div>",
            unsafe_allow_html=True
        )

        # Mostrar respuesta actual si existe
        if row["Respuesta"] and row["Respuesta"] != "Sin respuesta":
            st.markdown(f"**Respuesta:** {row['Respuesta']}")

        # Si el usuario pertenece al departamento, permitir actualizar la alerta
        if st.session_state["departamento"] == departamento:
            nueva_respuesta = st.text_area(
                "Añadir o actualizar respuesta", 
                value=row["Respuesta"] if row["Respuesta"] != "Sin respuesta" else "", 
                key=f"respuesta_alerta_{index}"
            )
            nuevo_estado = st.selectbox(
                "Actualizar estado",
                ["Nueva", "En proceso", "Resuelta"],
                index=["Nueva", "En proceso", "Resuelta"].index(row["Estado"]),
                key=f"estado_alerta_{index}"
            )
            if st.button("Actualizar alerta", key=f"actualizar_alerta_{index}"):
                alertas.loc[index, "Respuesta"] = nueva_respuesta if nueva_respuesta.strip() else "Sin respuesta"
                alertas.loc[index, "Estado"] = nuevo_estado
                guardar_alertas(alertas)
                st.success("Alerta actualizada correctamente.")
                # Manejo del reinicio para evitar el error visible
                try:
                    st.experimental_rerun()
                except Exception:
                    pass  # Ignorar cualquier excepción causada por la recarga





# Cargar comentarios
def cargar_comentarios():
    if os.path.exists(COMENTARIOS_FILE):
        comentarios = pd.read_csv(COMENTARIOS_FILE)
        if "Estado" not in comentarios.columns:
            comentarios["Estado"] = "En espera de ser atendido"
        if "Respuesta" not in comentarios.columns:
            comentarios["Respuesta"] = ""
        comentarios["Respuesta"] = comentarios["Respuesta"].fillna("Sin respuesta")
        return comentarios
    else:
        return pd.DataFrame(columns=["Usuario", "Departamento", "Comentario", "FechaHora", "Foro", "Estado", "Respuesta"])

# Guardar comentarios
def guardar_comentarios(comentarios):
    comentarios.to_csv(COMENTARIOS_FILE, index=False)

# Pantalla de inicio
def pantalla_inicio():
    # Agregar el logo en la pantalla de inicio de sesión
    st.image("logo.png", width=200)  # Reemplaza "logo.png" con la ruta de tu logo si es diferente

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
# Pantalla principal
# Mostrar los KPIs o contenido según el departamento seleccionado
# Mostrar la pantalla principal
def pantalla_principal():
    st.sidebar.title("TORRE DE CONTROL VB")
    
    # Agrega una imagen (puede ser local o desde un enlace)
    st.sidebar.image("logo.png", width=200)
    
    # Mensaje de bienvenida
    st.sidebar.markdown(f"**¡Bienvenido, {st.session_state['usuario']}!**")
    
    # Menú principal
    pagina = st.sidebar.radio("Selecciona un departamento", DEPARTAMENTOS)

    # Botón de cerrar sesión
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["autenticado"] = False
        # Manejo del reinicio para evitar el error visible
        try:
            st.experimental_rerun()
        except Exception:
            pass  # Ignorar cualquier excepción causada por la recarga

    # Obtener contadores de alertas y tickets detallados
    detallado_alertas = contar_detallado_alertas(pagina)
    detallado_tickets = contar_detallado_tickets(pagina)

    # Mostrar los indicadores superiores
    mostrar_indicador_superior(detallado_alertas, detallado_tickets)

    # Mostrar los KPIs o contenido según el departamento seleccionado
    if pagina == "Dirección":
        st.title("Resumen General - Dirección")
        st.metric("Incidencias Totales", "45", "-5 desde ayer")
        st.metric("Proyectos en curso", "12", "+1 desde la semana pasada")
        st.metric("Eficiencia Operativa", "85%", "+3%")
        st.line_chart({"Progreso": [70, 75, 80, 85, 90]})
        generar_alertas("Dirección")
        mostrar_alertas("Dirección")

    elif pagina == "Originación de crédito":
        st.title("KPIs - Originación de Crédito")
        st.metric("Créditos aprobados", "120", "+15")
        st.metric("Monto originado", "2,000,000 USD", "+200,000 USD")
        st.bar_chart({"Créditos por día": [20, 25, 22, 30, 35]})
        generar_alertas("Originación de crédito")
        mostrar_alertas("Originación de crédito")

    elif pagina == "Cobranza virtual":
        st.title("KPIs - Cobranza Virtual")
        st.metric("Cobros efectivos", "75%", "+5%")
        st.metric("Tiempo promedio de contacto", "1 min", "-10 seg")
        st.line_chart({"Evolución de Cobros": [60, 65, 70, 75, 80]})
        generar_alertas("Cobranza virtual")
        mostrar_alertas("Cobranza virtual")

    elif pagina == "Cobranza campo":
        st.title("KPIs - Cobranza Campo")
        st.metric("Recuperación", "90%", "+10%")
        st.metric("Visitas realizadas", "300", "+50")
        st.area_chart({"Progreso semanal": [50, 100, 150, 250, 300]})
        generar_alertas("Cobranza campo")
        mostrar_alertas("Cobranza campo")

    elif pagina == "Venta en tienda":
        st.title("KPIs - Venta en Tienda")
        st.metric("Ventas totales", "500,000 USD", "+50,000 USD")
        st.metric("Clientes atendidos", "5,000", "+500")
        st.line_chart({"Ventas por semana": [100000, 120000, 130000, 150000, 160000]})
        generar_alertas("Venta en tienda")
        mostrar_alertas("Venta en tienda")

    elif pagina == "Sistemas":
        st.title("KPIs - Sistemas")
        st.metric("Tiempo de respuesta", "2 horas", "-30 min")
        st.metric("Tickets resueltos", "95%", "+5%")
        st.bar_chart({"Tickets por día": [50, 45, 60, 55, 65]})
        generar_alertas("Sistemas")
        mostrar_alertas("Sistemas")

    elif pagina == "Desarrollo":
        st.title("KPIs - Desarrollo")
        st.metric("Proyectos completados", "8", "+2")
        st.metric("Horas invertidas", "200 horas", "+20 horas")
        st.line_chart({"Progreso de Proyectos": [40, 60, 70, 80, 100]})
        generar_alertas("Desarrollo")
        mostrar_alertas("Desarrollo")

    elif pagina == "Riesgos":
        st.title("KPIs - Riesgos")
        st.metric("Riesgos mitigados", "95%", "+10%")
        st.metric("Alertas activadas", "10", "-2")
        st.bar_chart({"Riesgos por semana": [5, 8, 6, 10, 4]})
        generar_alertas("Riesgos")
        mostrar_alertas("Riesgos")

    elif pagina == "Recursos humanos":
        st.title("KPIs - Recursos Humanos")
        st.metric("Contrataciones", "15", "+5")
        st.metric("Capacitaciones", "8", "+2")
        st.line_chart({"Crecimiento del equipo": [50, 55, 60, 65, 70]})
        generar_alertas("Recursos humanos")
        mostrar_alertas("Recursos humanos")

    # Mostrar tickets del departamento
    mostrar_tickets(pagina)







# Función para mostrar el foro
# Función para mostrar el foro
# Función para mostrar los tickets
def mostrar_tickets(departamento):
    if f"mostrar_tickets_{departamento}" not in st.session_state:
        st.session_state[f"mostrar_tickets_{departamento}"] = False

    if st.button("Abrir/Cerrar tickets"):
        st.session_state[f"mostrar_tickets_{departamento}"] = not st.session_state[f"mostrar_tickets_{departamento}"]

    if st.session_state[f"mostrar_tickets_{departamento}"]:
        tickets = cargar_comentarios()  # Renombramos "comentarios" a "tickets" internamente
        tickets_departamento = tickets[tickets["Foro"] == departamento]

        st.title(f"Tickets del departamento: {departamento}")
        for index, row in tickets_departamento.iterrows():
            with st.container():
                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                with col1:
                    indicador_estado = {
                        "Rechazado": "🔴",
                        "En proceso": "🟡",
                        "Resuelto": "🟢"
                    }.get(row["Estado"], "⚪")
                    st.markdown(
                        f"### {row['Titulo']}\n"
                        f"**{row['Usuario']} ({row['Departamento']})** - *{row['FechaHora']}*\n\n"
                        f"> {row['Comentario']}\n\n"
                        f"**Estado:** {indicador_estado} {row['Estado']}"
                    )
                    if st.button("Ver respuesta", key=f"ver_respuesta_button_{index}"):
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
                            tickets.loc[index, "Estado"] = nuevo_estado
                            tickets.loc[index, "Respuesta"] = nueva_respuesta if nueva_respuesta.strip() else "Sin respuesta"
                            guardar_comentarios(tickets)
                            st.success("Ticket actualizado correctamente.")
                            # Manejo del reinicio para evitar el error visible
                            try:
                                st.experimental_rerun()
                            except Exception:
                                pass  # Ignorar cualquier excepción causada por la recarga

        nuevo_titulo = st.text_input("Título del ticket:", key=f"nuevo_titulo_{departamento}")
        nuevo_ticket = st.text_area("Descripción del ticket:", key=f"nuevo_ticket_{departamento}")
        if st.button("Enviar ticket", key=f"enviar_ticket_{departamento}"):
            if nuevo_titulo.strip() and nuevo_ticket.strip():
                nuevo_ticket_data = pd.DataFrame(
                    [{
                        "Usuario": st.session_state["usuario"],
                        "Departamento": st.session_state["departamento"],
                        "Titulo": nuevo_titulo.strip(),
                        "Comentario": nuevo_ticket.strip(),
                        "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Foro": departamento,
                        "Estado": "En espera de ser atendido",
                        "Respuesta": "Sin respuesta"
                    }]
                )
                tickets = pd.concat([tickets, nuevo_ticket_data], ignore_index=True)
                guardar_comentarios(tickets)
                st.success("Ticket enviado.")
                # Manejo del reinicio para evitar el error visible
                try:
                    st.experimental_rerun()
                except Exception:
                    pass  # Ignorar cualquier excepción causada por la recarga
            else:
                st.error("Por favor completa ambos campos: Título y Descripción del ticket.")


# Cargar comentarios actualizado
def cargar_comentarios():
    if os.path.exists(COMENTARIOS_FILE):
        comentarios = pd.read_csv(COMENTARIOS_FILE)
        if "Estado" not in comentarios.columns:
            comentarios["Estado"] = "En espera de ser atendido"
        if "Respuesta" not in comentarios.columns:
            comentarios["Respuesta"] = ""
        if "Titulo" not in comentarios.columns:
            comentarios["Titulo"] = ""
        comentarios["Respuesta"] = comentarios["Respuesta"].fillna("Sin respuesta")
        comentarios["Titulo"] = comentarios["Titulo"].fillna("Sin título")
        return comentarios
    else:
        return pd.DataFrame(columns=["Usuario", "Departamento", "Titulo", "Comentario", "FechaHora", "Foro", "Estado", "Respuesta"])

# Main
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    pantalla_inicio()
else:
    pantalla_principal()