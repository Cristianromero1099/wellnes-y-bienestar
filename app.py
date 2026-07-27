import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# ---------------------------------------------------------
# Configuración de página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Wellness & Performance",
    page_icon="⚽",
    layout="wide"
)

# Inicializar estado de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

# ---------------------------------------------------------
# Login / Autenticación
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.title("⚽ Portal del Equipo")
    st.subheader("Control de Bienestar y Rendimiento")
    
    with st.card if hasattr(st, "card") else st.container():
        usuario = st.text_input("Nombre / Nombre de usuario")
        rol = st.selectbox("Rol", ["Jugadora", "Entrenadora"])
        
        if st.button("Ingresar", type="primary"):
            if usuario.strip():
                st.session_state.logged_in = True
                st.session_state.role = rol
                st.session_state.username = usuario.strip()
                st.rerun()
            else:
                st.error("Por favor ingresa un nombre válido.")

else:
    # Sidebar común
    st.sidebar.title("⚽ Control de Sesión")
    st.sidebar.write(f"**Usuario:** {st.session_state.username}")
    st.sidebar.write(f"**Rol:** {st.session_state.role}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = ""
        st.rerun()

    # ---------------------------------------------------------
    # Vista 1: JUGADORA (Cuestionario)
    # ---------------------------------------------------------
    if st.session_state.role == "Jugadora":
        st.title("📝 Cuestionario Diario de Wellness")
        st.caption(f"Registro para hoy: {date.today().strftime('%d/%m/%Y')}")
        st.write(f"Hola **{st.session_state.username}**, completa tu reporte antes del entrenamiento.")

        with st.form("wellness_form", clear_on_submit=True):
            sueño = st.slider("Calidad de sueño", 1, 5, 3, help="1: Muy mala - 5: Excelente")
            horas_sueño = st.number_input("Horas dormidas", min_value=0.0, max_value=14.0, value=7.5, step=0.5)
            fatiga = st.slider("Nivel de fatiga", 1, 5, 3, help="1: Exhausta - 5: Fresca / Sin fatiga")
            estres = st.slider("Carga de estrés", 1, 5, 3, help="1: Estrés alto - 5: Muy relajada")
            dolor = st.slider("Dolor muscular / Agujetas", 1, 5, 3, help="1: Mucho dolor - 5: Sin dolor")
            
            molestia = st.text_area("¿Alguna molestia física o nota específica?")

            enviado = st.form_submit_button("Guardar respuesta diario", type="primary")
            
            if enviado:
                # Confirmación inmediata
                st.success("¡Respuestas registradas correctamente! Que tengas un excelente entrenamiento.")

    # ---------------------------------------------------------
    # Vista 2: ENTRENADORA (Dashboard)
    # ---------------------------------------------------------
    elif st.session_state.role == "Entrenadora":
        st.title("📊 Dashboard de Bienestar - Plantilla")
        st.caption(f"Fecha: {date.today().strftime('%d/%m/%Y')}")

        # Datos de demostración
        np.random.seed(42)
        plantilla = ["Ana G.", "María L.", "Sofía R.", "Carla M.", "Elena P.", "Lucía V."]
        datos = pd.DataFrame({
            "Jugadora": plantilla,
            "Sueño (1-5)": np.random.randint(2, 6, size=len(plantilla)),
            "Horas Sueño": np.random.choice([6.0, 7.0, 7.5, 8.0, 8.5], size=len(plantilla)),
            "Fatiga (1-5)": np.random.randint(1, 6, size=len(plantilla)),
            "Estrés (1-5)": np.random.randint(2, 6, size=len(plantilla)),
            "Dolor Muscular": np.random.randint(1, 6, size=len(plantilla)),
        })
        datos["Score Promedio"] = datos[["Sueño (1-5)", "Fatiga (1-5)", "Estrés (1-5)", "Dolor Muscular"]].mean(axis=1).round(2)

        # Métricas resumidas
        col1, col2, col3 = st.columns(3)
        col1.metric("Promedio Bienestar", f"{datos['Score Promedio'].mean():.2f} / 5")
        col2.metric("En Riesgo (Score < 2.5)", len(datos[datos["Score Promedio"] < 2.5]))
        col3.metric("Respuestas Recibidas", f"{len(datos)} / {len(plantilla)}")

        st.divider()

        # Tabla y Gráficos
        st.subheader("Estado actual de la plantilla")
        st.dataframe(datos, use_container_width=True)

        st.subheader("Comparativa de métricas clave")
        st.bar_chart(datos.set_index("Jugadora")[["Sueño (1-5)", "Fatiga (1-5)", "Dolor Muscular"]])
