import streamlit as st
from datetime import date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente Becas IDH - UAGRM", page_icon="🎓")

st.title("🎓 Asistente Virtual de Becas IDH - UAGRM")
st.markdown("---")
st.info("Este es un prototipo lógico para validar requisitos de postulación. Basado en la Convocatoria Gestión 2025.")

# --- BARRA LATERAL: SELECCIÓN DE BECA ---
st.sidebar.header("1. ¿Qué beca te interesa?")
tipo_beca = st.sidebar.selectbox(
    "Selecciona la modalidad:",
    ["Beca Alimentación", "Beca Estudio", "Beca Investigación", "Beca Interacción Social"]
)

# --- LÓGICA DE FECHAS (Extraído de imagen_08d9ff.png) ---
# Definimos las fechas límite según el documento
hoy = date.today()
limite_alimentacion = date(2025, 3, 7) # 7 de Marzo
inicio_otras = date(2025, 3, 24)       # 24 de Marzo

st.header(f"Requisitos para: {tipo_beca}")

# Validación de Fechas
if tipo_beca == "Beca Alimentación":
    st.warning(f"📅 PLAZO DE ENTREGA: Del 24 de Febrero al 07 de Marzo.")
else:
    st.warning(f"📅 PLAZO DE ENTREGA: Del 24 de Marzo al 04 de Abril.")

st.markdown("---")

# --- PASO 1: FILTROS "FATALES" (Extraído de image_08da02.png) ---
st.subheader("Paso 1: Requisitos Generales")
col1, col2 = st.columns(2)

with col1:
    nacionalidad = st.radio("¿Tienes nacionalidad boliviana?", ("Sí", "No"))
    regular = st.radio("¿Eres estudiante regular en tu carrera de origen?", ("Sí", "No"))

with col2:
    deuda = st.radio("¿Tienes deudas pendientes con la universidad?", ("No", "Sí"))
    doble_beneficio = st.radio("¿Tienes otro beneficio económico (Comedor, etc.)?", ("No", "Sí"))

# Lógica de descalificación inmediata
if nacionalidad == "No" or regular == "No" or deuda == "Sí" or doble_beneficio == "Sí":
    st.error("❌ NO HABILITADO: No cumples con los requisitos generales (Art. Requisitos a, b, f).")
    st.stop() # Detiene el código aquí si falla
else:
    st.success("✅ Requisitos generales cumplidos.")

st.markdown("---")

# --- PASO 2: TIPO DE ESTUDIANTE (El Corazón del Árbol de Decisión) ---
st.subheader("Paso 2: Condición Académica")

tipo_estudiante = st.selectbox(
    "¿Cuál es tu situación actual?",
    ["Selecciona una opción...", "Estudiante Nuevo (1er año/semestre)", "Estudiante Antiguo"]
)

resultado = "PENDIENTE"

if tipo_estudiante == "Estudiante Nuevo (1er año/semestre)":
    # Regla Inciso E (image_08da02.png)
    st.markdown("**Regla para Nuevos:** Se valora la condición socio-económica.")
    puntaje = st.number_input("Ingresa tu puntaje de la Ficha Socioeconómica:", min_value=0, max_value=100)
    
    if puntaje >= 35:
        resultado = "APROBADO"
    else:
        resultado = "RECHAZADO_PUNTAJE"

elif tipo_estudiante == "Estudiante Antiguo":
    # Regla Inciso D (image_08da02.png) y Art 48 (image_08d9ff.png)
    st.markdown("**Regla para Antiguos:** Rendimiento académico del periodo anterior.")
    materias_inscritas = st.number_input("¿Cuántas materias inscribiste el semestre anterior?", min_value=1, step=1)
    materias_aprobadas = st.number_input("¿Cuántas materias APROBASTE el semestre anterior?", min_value=0, step=1)
    
    # Cálculo de la mitad más uno
    mitad_mas_uno = (materias_inscritas / 2) + 0.5 
    # Ajuste matemático: Si inscribió 5, mitad es 2.5, +0.5 = 3. Debe aprobar 3.
    # Si inscribió 4, mitad es 2, +1 (valor entero mayor) = 3.
    
    # Lógica simplificada de "Mitad más uno (valor entero mayor)"
    import math
    minimo_necesario = math.floor(materias_inscritas / 2) + 1
    
    st.info(f"Para cumplir, debiste aprobar al menos {minimo_necesario} materias.")
    
    if materias_aprobadas >= minimo_necesario:
        resultado = "APROBADO"
    else:
        resultado = "RECHAZADO_ACADEMICO"

# --- PASO 3: RESULTADO FINAL Y SALIDA (OUTPUT) ---
st.markdown("---")
st.subheader("Resultado del Análisis")

# --- PASO 3: RESULTADO FINAL Y SALIDA (OUTPUT) ---
st.markdown("---")
st.subheader("Resultado del Análisis")

# --- PASO 3: RESULTADO FINAL Y SALIDA (OUTPUT) ---
st.markdown("---")
st.subheader("Resultado del Análisis")

if resultado == "APROBADO":
    st.balloons()
    st.success(f"🎉 ¡FELICIDADES! Eres apto para postular a la {tipo_beca}.")
    
    # --- LÓGICA DE DOCUMENTOS (INTEGRACIÓN VIDEO + REGLAMENTO) ---
    
    st.markdown("### 📂 ¿Qué debo presentar?")
    st.warning("⚠️ IMPORTANTE: Presentar todo en Folder Amarillo tamaño carta con Nepaco.")

    tab1, tab2 = st.tabs(["📄 Requisitos Generales (Todos)", "🔍 Requisitos Específicos"])
    
    with tab1:
        st.write("""
        **Todo estudiante debe tener estos 11 documentos en orden:**
        1. **Ficha Socioeconómica:** Rellenada con lapicero azul (descargar de perfil o web).
        2. **Ficha Social:** Impresa desde tu perfil web.
        3. **Croquis de Vivienda:** Dibujo a mano o impresión de Google Maps (con flecha indicando casa).
        4. **Fotocopia de Carnet:** 2 copias vigentes.
        5. **Certificado de Nacimiento:** 1 fotocopia.
        6. **Boleta de Inscripción:** Del semestre actual (semestre 1-2025).
        7. **Histórico Académico:** Imprimir desde tu perfil.
        8. **Respaldo de Vivienda:** Aviso de luz/agua (si es propia/cedida) o Recibo de alquiler/Contrato.
        9. **Respaldo de Ingresos:** Boleta de pago (padres/tuyo) o Certificado de gremio/sindicato (si es informal).
        10. **Folder Amarillo:** Rotulado en la tapa con tus datos.
        """)
        st.info("💡 Tip: Si eres de PROVINCIA, añade tu Certificado de Comunidad o Barrio.")

    with tab2:
        if tipo_beca == "Beca Alimentación":
            st.markdown(f"**PARA {tipo_beca.upper()}:**")
            st.write("- 🆔 Documento de identidad original (para firmar planilla).")
            st.write("- 🍽️ Asistir al comedor asignado para la habilitación.")
            
        elif "Estudio" in tipo_beca:
            st.markdown(f"**PARA {tipo_beca.upper()}:**")
            st.write("- 📝 Formulario de informe mensual.")
            st.write("- 📄 Carta de solicitud dirigida a la unidad donde harás horas beca.")
            
        elif "Investigación" in tipo_beca:
             st.markdown(f"**PARA {tipo_beca.upper()}:**")
             st.write("- 🔬 Cumplir los 8 requisitos extra de la DICIT.")
             st.write("- 📋 Visto bueno del Jefe de Investigación de tu Facultad.")
             
        elif "Extensión" in tipo_beca or "Interacción" in tipo_beca:
             st.markdown(f"**PARA {tipo_beca.upper()}:**")
             st.write("- 📘 Dos (2) ejemplares del Proyecto (dirigido a la comunidad o barrio).")
             st.write("- ✅ Visto bueno del Jefe de Extensión de tu Facultad.")
        
        else:
            st.write("Consultar convocatoria específica.")

elif resultado == "RECHAZADO_PUNTAJE":
    st.error("❌ NO HABILITADO. Tu puntaje socioeconómico es menor a 35 puntos.")
    st.markdown("**¿Por qué?** El reglamento exige priorizar a estudiantes con mayor necesidad económica.")

elif resultado == "RECHAZADO_ACADEMICO":
    st.error("❌ NO HABILITADO. Rendimiento académico insuficiente.")
    
    # Explicación pedagógica (Matemática Discreta aplicada)
    st.markdown("""
    **Explicación del Reglamento (Art. 48):**
    La regla es `Aprobadas >= (Inscritas / 2) + 1`.
    * Ejemplo: Si inscribiste 6, la mitad es 3. Más uno es 4. Necesitas 4 aprobadas.
    """)

elif resultado == "PENDIENTE":
    st.info("👈 Completa el formulario de la izquierda para ver tu diagnóstico.")
