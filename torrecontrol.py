import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la aplicación
st.set_page_config(
    page_title="Torre de Control - Empresa",
    layout="wide",
)

# Título principal
st.title("Torre de Control Empresarial")
st.markdown("Bienvenido a la torre de control. Aquí puedes monitorear los principales KPIs de cada departamento de tu empresa.")

# Barra lateral para navegación
departamento = st.sidebar.radio(
    "Selecciona un departamento:",
    [
        "Resumen General",
        "Originación de Crédito",
        "Cobranza Virtual",
        "Cobranza Campo",
        "Venta en Tienda",
        "Sistemas",
        "Desarrollo",
        "Riesgos",
        "Recursos Humanos",
    ],
)

# Función para gráficos de ejemplo
def generar_grafico_ejemplo(titulo, x, y):
    fig, ax = plt.subplots()
    ax.bar(x, y, alpha=0.7, color="skyblue")
    ax.set_title(titulo)
    ax.set_ylabel("Valor")
    ax.set_xlabel("Categoría")
    st.pyplot(fig)

# Función para tablas de ejemplo
def mostrar_tabla_ejemplo(titulo, datos):
    st.subheader(titulo)
    st.dataframe(datos)

# Resumen General
if departamento == "Resumen General":
    st.subheader("Resumen General de la Empresa")
    st.markdown("Este panel muestra un resumen consolidado de los indicadores clave de cada departamento.")
    
    # Indicadores de ejemplo
    kpis = {
        "Originación de Crédito": np.random.randint(50, 100),
        "Cobranza Virtual": np.random.randint(70, 100),
        "Cobranza Campo": np.random.randint(60, 90),
        "Venta en Tienda": np.random.randint(80, 120),
        "Sistemas": np.random.randint(20, 50),
        "Desarrollo": np.random.randint(10, 40),
        "Riesgos": np.random.randint(5, 15),
        "Recursos Humanos": np.random.randint(40, 80),
    }

    # KPIs como tarjetas
    cols = st.columns(len(kpis))
    for idx, (key, value) in enumerate(kpis.items()):
        with cols[idx]:
            st.metric(label=key, value=f"{value}%")
    
    # Gráfico consolidado
    generar_grafico_ejemplo(
        "Consolidado de Desempeño",
        list(kpis.keys()),
        list(kpis.values()),
    )

# Originación de Crédito
elif departamento == "Originación de Crédito":
    st.subheader("Originación de Crédito")
    st.markdown("Monitoreo de solicitudes y tiempos de aprobación.")

    # Tabla de ejemplo
    datos_credito = pd.DataFrame({
        "Fecha": pd.date_range(start="2023-11-01", periods=10),
        "Solicitudes Recibidas": np.random.randint(100, 200, size=10),
        "Aprobaciones": np.random.randint(50, 150, size=10),
        "Tasa de Aprobación (%)": np.random.randint(40, 80, size=10),
    })
    mostrar_tabla_ejemplo("Resumen de Solicitudes", datos_credito)

    # Gráfico
    generar_grafico_ejemplo(
        "Solicitudes y Aprobaciones",
        datos_credito["Fecha"].dt.strftime("%d-%b"),
        datos_credito["Solicitudes Recibidas"],
    )

# Cobranza Virtual
elif departamento == "Cobranza Virtual":
    st.subheader("Cobranza Virtual")
    st.markdown("Seguimiento a la recuperación virtual de pagos.")

    # Indicadores y gráfico de ejemplo
    datos_cobranza = pd.DataFrame({
        "Mes": ["Enero", "Febrero", "Marzo", "Abril"],
        "Cuentas Gestionadas": np.random.randint(1000, 2000, size=4),
        "Pagos Realizados": np.random.randint(500, 1500, size=4),
    })
    mostrar_tabla_ejemplo("Gestión de Cuentas", datos_cobranza)

    generar_grafico_ejemplo(
        "Pagos Realizados por Mes",
        datos_cobranza["Mes"],
        datos_cobranza["Pagos Realizados"],
    )

# Cobranza Campo
elif departamento == "Cobranza Campo":
    st.subheader("Cobranza en Campo")
    st.markdown("Rutas y visitas realizadas para cobranza.")

    # Tabla de rutas y KPI de éxito
    datos_rutas = pd.DataFrame({
        "Ruta": [f"Ruta {i}" for i in range(1, 6)],
        "Visitas Programadas": np.random.randint(50, 100, size=5),
        "Visitas Completadas": np.random.randint(40, 90, size=5),
        "Efectividad (%)": np.random.randint(60, 90, size=5),
    })
    mostrar_tabla_ejemplo("Estatus de Rutas", datos_rutas)

    generar_grafico_ejemplo(
        "Efectividad por Ruta",
        datos_rutas["Ruta"],
        datos_rutas["Efectividad (%)"],
    )

# Venta en Tienda
elif departamento == "Venta en Tienda":
    st.subheader("Venta en Tienda")
    st.markdown("Métricas de ventas e inventarios.")

    # Tabla de ventas por tienda
    datos_ventas = pd.DataFrame({
        "Tienda": [f"Tienda {i}" for i in range(1, 6)],
        "Ventas (USD)": np.random.randint(5000, 20000, size=5),
        "Inventario Restante": np.random.randint(200, 1000, size=5),
    })
    mostrar_tabla_ejemplo("Desempeño por Tienda", datos_ventas)

    generar_grafico_ejemplo(
        "Ventas por Tienda",
        datos_ventas["Tienda"],
        datos_ventas["Ventas (USD)"],
    )

# Sistemas
elif departamento == "Sistemas":
    st.subheader("Sistemas")
    st.markdown("Seguimiento de tickets y proyectos de tecnología.")

    # Tabla de tickets
    datos_tickets = pd.DataFrame({
        "Prioridad": ["Alta", "Media", "Baja", "Alta", "Media"],
        "Tickets Abiertos": np.random.randint(10, 50, size=5),
        "Tickets Resueltos": np.random.randint(5, 30, size=5),
    })
    mostrar_tabla_ejemplo("Estatus de Tickets", datos_tickets)

# Desarrollo, Riesgos y Recursos Humanos
elif departamento in ["Desarrollo", "Riesgos", "Recursos Humanos"]:
    st.subheader(f"{departamento}")
    st.markdown(f"Próximamente se implementarán métricas específicas para el departamento de {departamento}.")
