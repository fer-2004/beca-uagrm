import streamlit as st
from datetime import date
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente Becas IDH - UAGRM", page_icon="🎓", layout="centered")

# --- CABECERA ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/eb/Escudo_UAGRM.jpg", caption="U.A.G.R.M.", use_container_width=True)
st.title("🎓 Asistente Virtual de Becas IDH")
st.markdown("---")

# --- BARRA LATERAL: MENÚ DE 2 NIVELES ---
st.sidebar.header("🔍 Selección de Beca")

# NIVEL 1: Categoría
categoria = st.sidebar.selectbox(
    "1. Selecciona el Tipo de Beca:",
    ["A. Becas Socioeconómicas", "B. Becas Académicas", "C. Becas de Extensión"]
)

# NIVEL 2: Beca Específica (Dinámico según la categoría)
if categoria == "A. Becas Socioeconómicas":
    tipo_beca = st.sidebar.selectbox(
        "2. Elige la modalidad:",
        ["Beca Alimentación", "Beca Albergue Universitario", "Beca Estudio", "Beca Estudio Internado Rotatorio"]
    )
elif categoria == "B. Becas Académicas":
    tipo_beca = st.sidebar.selectbox(
        "2. Elige la modalidad:",
        ["Beca Investigación Científica", "Beca Investigación Tesis / Expociencia", "Beca Excelencia Académica"]
    )
else: # C. Extensión
    tipo_beca = st.sidebar.selectbox(
        "2. Elige la modalidad:",
        ["Beca Interacción Social / Extensión"]
    )

# --- DESCRIPCIÓN CONTEXTUAL (En palabras sencillas) ---
# Diccionario de descripciones rápidas para educar al usuario
descripciones = {
    "Beca Alimentación": "🍽️ **¿Qué es?** Acceso gratuito al Comedor Universitario (almuerzo/cena) para estudiantes con recursos limitados.",
    "Beca Albergue Universitario": "🏠 **¿Qué es?** Vivienda compartida gratuita para estudiantes que vienen de provincias alejadas.",
    "Beca Estudio": "💼 **¿Qué es?** Apoyo económico mensual a cambio de realizar horas de apoyo (trabajo ligero) en oficinas o laboratorios de la U.",
    "Beca Estudio Internado Rotatorio": "🏥 **¿Qué es?** Apoyo exclusivo para estudiantes de Salud (Medicina/Enfermería) que están en su etapa de internado.",
    "Beca Investigación Científica": "🔬 **¿Qué es?** Incentivo económico para estudiantes que participan como auxiliares en proyectos oficiales de investigación.",
    "Beca Investigación Tesis / Expociencia": "📜 **¿Qué es?** Apoyo para financiar gastos de tu Tesis de Grado o por haber ganado la feria de ciencias.",
    "Beca Excelencia Académica": "🏆 **¿Qué es?** Premio automático a los mejores promedios de la carrera (no se postula, te eligen).",
    "Beca Interacción Social / Extensión": "🤝 **¿Qué es?** Financiamiento para proyectos que lleven servicios o cultura de la Universidad a los barrios."
}

# Mostrar la descripción seleccionada
st.info(descripciones[tipo_beca])

# --- LÓGICA DE FECHAS ---
hoy = date.today()
if tipo_beca == "Beca Alimentación":
    st.warning("📅 PLAZO DE ENTREGA: Del 24 de Febrero al 07 de Marzo.")
elif tipo_beca == "Beca Excelencia Académica":
    st.success("📅 FECHA: Automática. Se otorga al finalizar la gestión.")
else:
    st.warning("📅 PLAZO DE ENTREGA: Del 24 de Marzo al 04 de Abril.")

st.markdown("---")

# --- CASO ESPECIAL: EXCELENCIA ACADÉMICA ---
if tipo_beca == "Beca Excelencia Académica":
    st.write("""
    **Requisitos Especiales (Art. 7 Reglamento):**
    1. Haber aprobado el **100% de las materias inscritas** (o mín. 80%).
    2. Tener uno de los **promedios más altos** de tu carrera.
    3. **Nota:** No necesitas presentar papeles ahora. Verifica en tu perfil web si saliste beneficiado.
    """)
    st.stop() 

# --- PASO 1: FILTROS "FATALES" ---
st.subheader("Paso 1: Requisitos Generales")
col1, col2 = st.columns(2)

with col1:
    nacionalidad = st.radio("¿Eres boliviano?", ("Sí", "No"))
    regular = st.radio("¿Eres estudiante regular?", ("Sí", "No"))

with col2:
    deuda = st.radio("¿Tienes deudas con la U?", ("No", "Sí"))
    doble_beneficio = st.radio("¿Tienes otra beca vigente?", ("No", "Sí"))

if nacionalidad == "No" or regular == "No" or deuda == "Sí" or doble_beneficio == "Sí":
    st.error("❌ NO HABILITADO: Incumples requisitos básicos (Nacionalidad, Deudas o Duplicidad).")
    st.stop()
else:
    st.success("✅ Primer filtro aprobado.")

st.markdown("---")

# --- PASO 2: TIPO DE ESTUDIANTE ---
st.subheader("Paso 2: Evaluación Académica")

tipo_estudiante = st.selectbox(
    "¿Cuál es tu situación?",
    ["Selecciona...", "Estudiante Nuevo (1er año/semestre)", "Estudiante Antiguo"]
)

resultado = "PENDIENTE"

if tipo_estudiante == "Estudiante Nuevo (1er año/semestre)":
    st.markdown("**Regla:** Se evalúa situación socio-económica.")
    puntaje = st.number_input("Puntaje Ficha Socioeconómica:", 0, 100)
    if puntaje >= 35: resultado = "APROBADO"
    else: resultado = "RECHAZADO_PUNTAJE"

elif tipo_estudiante == "Estudiante Antiguo":
    st.markdown("**Regla:** Debes haber vencido la mitad más uno de tus materias.")
    col_a, col_b = st.columns(2)
    with col_a: inscritas = st.number_input("Materias Inscritas (Semestre Anterior):", 1, step=1)
    with col_b: aprobadas = st.number_input("Materias APROBADAS (Semestre Anterior):", 0, step=1)
    
    minimo = math.floor(inscritas / 2) + 1
    st.caption(f"🧮 Necesitas: **{minimo}** aprobadas.")
    
    if aprobadas >= minimo: resultado = "APROBADO"
    else: resultado = "RECHAZADO_ACADEMICO"

# --- PASO 3: RESULTADO ---
st.markdown("---")
st.subheader("Diagnóstico Final")

if resultado == "APROBADO":
    st.balloons()
    st.success(f"🎉 ¡HABILITADO! Puedes postular a: {tipo_beca}")
    
    st.markdown("### 📂 Documentación a Presentar")
    st.warning("⚠️ OJO: Folder Amarillo rotulado con Nombre, Registro, Carrera y **CELULAR**.")

    tab1, tab2 = st.tabs(["📄 Requisitos Comunes", "🔍 Específicos de esta Beca"])
    
    with tab1:
        st.write("""
        1. **Ficha Socioeconómica** (Lapicero azul).
        2. **Ficha Social** (Impresa).
        3. **Boleta Inscripción** (Vigente).
        4. **Histórico Académico**.
        5. **Fotocopia C.I.** (2 copias).
        6. **Certificado Nacimiento** (1 copia).
        7. **Croquis Vivienda** (Mapa detallado).
        8. **Factura Luz/Agua** (Respaldo vivienda).
        9. **Boleta de Pago/Certificado** (Respaldo ingresos).
        10. **Folder Amarillo**.
        """)
        st.caption("Provincias: Adjuntar certificado de comunidad.")

    with tab2:
        if tipo_beca == "Beca Alimentación":
            st.write("- 🆔 C.I. original (firma planilla).")
            st.write("- 🏃 Asistir al comedor para habilitación.")
        elif "Estudio" in tipo_beca:
            st.write("- 📝 Informe mensual de actividades.")
            st.write("- 📨 Carta de aceptación de la Jefatura.")
        elif "Investigación" in tipo_beca:
            st.write("- 📨 Carta a Directora DICiT.")
            st.write("- 🚫 Declaración Jurada No Plagio.")
            st.write("- 📘 2 Perfiles de Investigación (con Tutor).")
        elif "Extensión" in tipo_beca:
            st.write("- 📘 2 Proyectos de Interacción.")
            st.write("- ✅ Visto bueno Jefe Extensión.")

elif resultado == "RECHAZADO_PUNTAJE":
    st.error("❌ NO HABILITADO: Puntaje socioeconómico bajo (<35).")
elif resultado == "RECHAZADO_ACADEMICO":
    st.error(f"❌ NO HABILITADO: Te faltaron materias. Necesitabas {minimo}.")
elif resultado == "PENDIENTE":
    st.info("👈 Completa los datos del Paso 2.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    🛠️ Prototipo Académico - Ing. Informática UAGRM<br>
    Normativa basada en Gestión 2025
</div>
""", unsafe_allow_html=True)
