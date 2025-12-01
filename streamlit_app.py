import streamlit as st
from datetime import date
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente Becas IDH - UAGRM", page_icon="🎓", layout="centered")

# --- CABECERA ---
st.title("🎓 Asistente Virtual de Becas IDH - UAGRM")
st.markdown("---")
st.info("Este es un prototipo lógico para validar requisitos de postulación. Basado en la Convocatoria Gestión 2025 y Normativa DUBSS.")

# --- BARRA LATERAL: SELECCIÓN DE BECA ---
st.sidebar.header("1. ¿Qué beca te interesa?")
tipo_beca = st.sidebar.selectbox(
    "Selecciona la modalidad:",
    ["Beca Alimentación", "Beca Estudio", "Beca Estudio Internado Rotatorio", 
     "Beca Investigación Científica", "Beca Investigación Tesis", 
     "Beca Interacción Social / Extensión", "Beca Excelencia Académica"]
)

# --- LÓGICA DE FECHAS ---
# Definimos las fechas límite según cronograma oficial
hoy = date.today()

if tipo_beca == "Beca Alimentación":
    st.header(f"Requisitos para: {tipo_beca}")
    st.warning("📅 PLAZO DE ENTREGA: Del 24 de Febrero al 07 de Marzo.")
elif tipo_beca == "Beca Excelencia Académica":
    st.header(f"Requisitos para: {tipo_beca}")
    st.success("📅 FECHA: Automática. Se otorga a los mejores promedios al finalizar la gestión.")
else:
    st.header(f"Requisitos para: {tipo_beca}")
    st.warning("📅 PLAZO DE ENTREGA: Del 24 de Marzo al 04 de Abril.")

st.markdown("---")

# --- CASO ESPECIAL: EXCELENCIA ACADÉMICA ---
if tipo_beca == "Beca Excelencia Académica":
    st.info("ℹ️ Esta beca se rige por normativa especial (Art. 7 Reglamento).")
    st.write("""
    **Requisitos Principales:**
    1. Haber aprobado el **100% de las materias inscritas** en la gestión anterior (o mínimo el 80% según caso).
    2. Tener los **promedios ponderados más altos** de tu carrera.
    3. No requiere postulación manual (es automática), pero debes verificar en tu perfil.
    """)
    st.stop() # Detiene el código aquí para esta beca

# --- PASO 1: FILTROS "FATALES" (Requisitos Generales) ---
st.subheader("Paso 1: Requisitos Generales")
col1, col2 = st.columns(2)

with col1:
    nacionalidad = st.radio("¿Tienes nacionalidad boliviana?", ("Sí", "No"))
    regular = st.radio("¿Eres estudiante regular en tu carrera?", ("Sí", "No"))

with col2:
    deuda = st.radio("¿Tienes deudas pendientes con la universidad?", ("No", "Sí"))
    doble_beneficio = st.radio("¿Tienes otro beneficio económico vigente?", ("No", "Sí"))

# Lógica de descalificación inmediata
if nacionalidad == "No" or regular == "No" or deuda == "Sí" or doble_beneficio == "Sí":
    st.error("❌ NO HABILITADO: No cumples con los requisitos generales (Art. Requisitos a, b, f).")
    st.markdown("""
    **Causas comunes de rechazo:**
    * No ser boliviano.
    * Deber libros o matrículas.
    * Tener ya otra beca (Comedor, Auxiliatura, etc.).
    """)
    st.stop()
else:
    st.success("✅ Requisitos generales cumplidos.")

st.markdown("---")

# --- PASO 2: TIPO DE ESTUDIANTE (Lógica Académica) ---
st.subheader("Paso 2: Condición Académica")

tipo_estudiante = st.selectbox(
    "¿Cuál es tu situación actual?",
    ["Selecciona una opción...", "Estudiante Nuevo (1er año/semestre)", "Estudiante Antiguo"]
)

resultado = "PENDIENTE"

if tipo_estudiante == "Estudiante Nuevo (1er año/semestre)":
    st.markdown("**Regla para Nuevos:** Se valora la condición socio-económica (Inciso e).")
    puntaje = st.number_input("Ingresa tu puntaje de la Ficha Socioeconómica:", min_value=0, max_value=100)
    
    if puntaje >= 35:
        resultado = "APROBADO"
    else:
        resultado = "RECHAZADO_PUNTAJE"

elif tipo_estudiante == "Estudiante Antiguo":
    st.markdown("**Regla para Antiguos:** Rendimiento académico del periodo anterior (Inciso d).")
    
    col_a, col_b = st.columns(2)
    with col_a:
        materias_inscritas = st.number_input("Materias inscritas semestre anterior:", min_value=1, step=1)
    with col_b:
        materias_aprobadas = st.number_input("Materias APROBADAS semestre anterior:", min_value=0, step=1)
    
    # Lógica de "Mitad más uno (valor entero mayor)"
    minimo_necesario = math.floor(materias_inscritas / 2) + 1
    
    st.caption(f"🧮 Cálculo interno: La mitad de {materias_inscritas} es {materias_inscritas/2}. El entero mayor +1 requiere aprobar **{minimo_necesario}** materias.")
    
    if materias_aprobadas >= minimo_necesario:
        resultado = "APROBADO"
    else:
        resultado = "RECHAZADO_ACADEMICO"

# --- PASO 3: RESULTADO FINAL Y SALIDA (OUTPUT) ---
st.markdown("---")
st.subheader("Resultado del Diagnóstico")

if resultado == "APROBADO":
    st.balloons()
    st.success(f"🎉 ¡FELICIDADES! Eres apto para postular a la {tipo_beca}.")
    
    # --- LÓGICA DE DOCUMENTOS (VERSIÓN FINAL VERIFICADA WEB UAGRM) ---
    
    st.markdown("### 📂 Documentación Oficial a Presentar")
    st.warning("⚠️ IMPORTANTE: El Folder Amarillo debe llevar en la tapa: Nombre, Carrera, Registro y **N° DE CELULAR**.")

    tab1, tab2 = st.tabs(["📄 Requisitos Comunes (Todos)", "🔍 Requisitos Específicos por Beca"])
    
    with tab1:
        st.info("Estos 10 documentos son OBLIGATORIOS para cualquier postulación (Fuente: DUBSS/Web UAGRM):")
        st.markdown("""
        1. **Ficha Socioeconómica:** Rellenada con bolígrafo azul.
        2. **Ficha Social:** Impresa del perfil web.
        3. **Boleta de Inscripción:** Semestre actual (1-2025).
        4. **Histórico Académico:** Impreso del perfil.
        5. **Fotocopia de Carnet:** 2 copias (vigentes).
        6. **Certificado de Nacimiento:** 1 fotocopia.
        7. **Croquis de Vivienda:** Detallado (Google Maps o dibujo) con ubicación exacta.
        8. **Respaldo de Vivienda:** Aviso de luz/agua (propia) o Recibo/Contrato (alquiler).
        9. **Respaldo de Ingresos:** Boleta de pago (padres) o Certificado de trabajo/gremio.
        10. **Folder Amarillo:** Con nepaco y debidamente rotulado.
        """)
        st.caption("Nota: Si eres de provincia, adjunta tu Certificado de Comunidad/Barrio.")

    with tab2:
        if tipo_beca == "Beca Alimentación":
            st.markdown(f"**🌽 {tipo_beca.upper()}:**")
            st.write("- Asistir personalmente al comedor para la habilitación biométrica.")
            st.write("- Llevar C.I. original para firma de planilla.")
            
        elif "Estudio" in tipo_beca:
            st.markdown(f"**📚 {tipo_beca.upper()}:**")
            st.write("- Formulario de informe mensual de actividades.")
            st.write("- Carta de solicitud/aceptación de la unidad donde harás las horas beca.")
            
        elif "Investigación" in tipo_beca:
             st.markdown(f"**🔬 {tipo_beca.upper()} (Requisitos DICiT):**")
             st.success("💰 Dato: Esta beca suele tener un incentivo económico mayor.")
             st.write("- **Carta dirigida a la Directora de la DICiT**.")
             st.write("- **Declaración Jurada de NO Plagio** (otorgado por DICiT).")
             st.write("- **Dos (2) ejemplares del Perfil de Investigación** aprobados por Tutor.")
             st.write("- Informe de evaluación del Tutor.")
             
        elif "Extensión" in tipo_beca or "Interacción" in tipo_beca:
             st.markdown(f"**🤝 {tipo_beca.upper()}:**")
             st.write("- Dos (2) ejemplares del Proyecto dirigido a la comunidad.")
             st.write("- Visto bueno del Jefe de Extensión/Interacción de tu Facultad.")
        
        else:
            st.write("Selecciona una beca específica para ver sus requisitos extra.")

elif resultado == "RECHAZADO_PUNTAJE":
    st.error("❌ NO HABILITADO. Tu puntaje socioeconómico es menor a 35 puntos.")
    st.markdown("**¿Por qué?** El reglamento exige priorizar a estudiantes con mayor necesidad económica.")

elif resultado == "RECHAZADO_ACADEMICO":
    st.error("❌ NO HABILITADO. Rendimiento académico insuficiente.")
    st.markdown(f"""
    **Explicación del Reglamento (Art. 48):**
    Para {materias_inscritas} materias inscritas, debiste aprobar al menos **{minimo_necesario}**.
    """)

elif resultado == "PENDIENTE":
    st.info("👈 Completa el formulario de la izquierda para ver tu diagnóstico.")
