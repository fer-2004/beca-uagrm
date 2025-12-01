import streamlit as st
from datetime import date
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente Becas IDH", page_icon="🎓", layout="centered")

# --- ESTILOS CSS PERSONALIZADOS (MAQUILLAJE) ---
# --- ESTILOS CSS PERSONALIZADOS (MODO OSCURO PRO) ---
st.markdown("""
    <style>
    /* 1. Fondo principal y texto */
    .stApp {
        background-color: #0e1117; /* Fondo oscuro elegante */
        color: #fafafa;
    }
    
    /* 2. Barra lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #262730; /* Gris oscuro para el menú */
        border-right: 1px solid #4b4b4b;
    }
    
    /* 3. Títulos y Cabeceras */
    h1, h2, h3 {
        color: #ff4b4b !important; /* Rojo Streamlit (combina con el escudo) */
        font-family: 'Helvetica', sans-serif;
    }
    
    /* 4. Cajas de Info/Éxito (Alertas) */
    .stAlert {
        background-color: #1c1e24; /* Fondo suave para cajas */
        border: 1px solid #4b4b4b;
        color: #ffffff;
    }
    
    /* 5. Radio Buttons y Selectbox */
    .stRadio label, .stSelectbox label {
        color: #ffffff !important;
        font-weight: bold;
    }
    
    /* 6. Ajuste del Logo para que no se vea gigante */
    [data-testid="stSidebar"] img {
        margin-top: 20px;
        margin-bottom: 20px;
        border-radius: 50%; /* Hace el logo circular si es cuadrado */
        border: 2px solid #ffffff; /* Borde blanco fino */
    }
    </style>
""", unsafe_allow_html=True)
# --- BARRA LATERAL: IDENTIDAD Y MENÚ ---
# 1. EL LOGO (Asegúrate de haber subido 'logo_uagrm.jpg' a GitHub)
try:
    st.sidebar.image("logo_uagrm.jpg", use_container_width=True)
except:
    # Si falla la carga, usa el escudo de Wikimedia por defecto
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/eb/Escudo_UAGRM.jpg", use_container_width=True)

st.sidebar.title("🎓 Menú de Becas")
st.sidebar.markdown("---")

# 2. NIVEL 1: CATEGORÍA (Usamos Radio Button para diferenciarlo)
st.sidebar.header("1️⃣ Selecciona la Categoría:")
categoria = st.sidebar.radio(
    "Tipo de Beneficio:",
    ["A. Becas Socioeconómicas", "B. Becas Académicas", "C. Becas de Extensión"],
    help="Elige el grupo de becas que te interesa para ver las opciones."
)

# --- BURBUJA DE EXPLICACIÓN (Contexto inmediato) ---
if categoria == "A. Becas Socioeconómicas":
    st.sidebar.info("💡 **Info:** Apoyo destinado a estudiantes con recursos limitados (Comedor, Vivienda, Dinero).")
    opciones_beca = ["Beca Alimentación", "Beca Albergue Universitario", "Beca Estudio", "Beca Estudio Internado Rotatorio"]

elif categoria == "B. Becas Académicas":
    st.sidebar.info("💡 **Info:** Incentivos para estudiantes destacados en notas o investigación.")
    opciones_beca = ["Beca Investigación Científica", "Beca Investigación Tesis / Expociencia", "Beca Excelencia Académica"]

else: # C. Extensión
    st.sidebar.info("💡 **Info:** Financiamiento para proyectos que ayuden a la sociedad.")
    opciones_beca = ["Beca Interacción Social / Extensión"]

# 3. NIVEL 2: BECA ESPECÍFICA
st.sidebar.markdown("---")
st.sidebar.header("2️⃣ Elige la Modalidad:")
tipo_beca = st.sidebar.selectbox("Selecciona una opción:", opciones_beca)

# --- CUERPO PRINCIPAL ---
st.title(f"Requisitos: {tipo_beca}")

# Diccionario de descripciones detalladas
descripciones = {
    "Beca Alimentación": "🍽️ Acceso gratuito al Comedor Universitario (almuerzo/cena) diario.",
    "Beca Albergue Universitario": "🏠 Vivienda gratuita para estudiantes de provincias alejadas.",
    "Beca Estudio": "💼 Apoyo económico mensual a cambio de horas de trabajo administrativo.",
    "Beca Estudio Internado Rotatorio": "🏥 Apoyo exclusivo para internos de Medicina/Enfermería.",
    "Beca Investigación Científica": "🔬 Pago mensual por auxiliar en proyectos oficiales de la DICiT.",
    "Beca Investigación Tesis / Expociencia": "📜 Financiamiento para gastos de graduación o premios de ferias.",
    "Beca Excelencia Académica": "🏆 Premio automático a los mejores promedios (sin postulación).",
    "Beca Interacción Social / Extensión": "🤝 Fondos para ejecutar proyectos en barrios o comunidades."
}

st.success(descripciones[tipo_beca])

# --- LÓGICA DE FECHAS ---
hoy = date.today()
if tipo_beca == "Beca Alimentación":
    st.warning("📅 **PLAZO URGENTE:** Del 24 de Febrero al 07 de Marzo.")
elif tipo_beca == "Beca Excelencia Académica":
    st.info("📅 **FECHA:** Automática al finalizar la gestión.")
else:
    st.warning("📅 **PLAZO GENERAL:** Del 24 de Marzo al 04 de Abril.")

st.markdown("---")

# --- CASO ESPECIAL: EXCELENCIA ---
if tipo_beca == "Beca Excelencia Académica":
    st.write("### 🥇 Normativa Especial")
    st.write("Esta beca no requiere presentar folder. Debes cumplir:")
    st.write("1. Haber aprobado el **100% de materias** (o 80% en casos especiales).")
    st.write("2. Tener el promedio más alto de tu carrera.")
    st.stop()

# --- PASO 1: FILTROS GENERALES ---
st.subheader("📋 Paso 1: Filtros Básicos")
col1, col2 = st.columns(2)

with col1:
    nacionalidad = st.radio("¿Eres boliviano?", ("Sí", "No"))
    regular = st.radio("¿Eres estudiante regular?", ("Sí", "No"))

with col2:
    deuda = st.radio("¿Tienes deudas con la U?", ("No", "Sí"))
    doble_beneficio = st.radio("¿Tienes otra beca?", ("No", "Sí"))

if nacionalidad == "No" or regular == "No" or deuda == "Sí" or doble_beneficio == "Sí":
    st.error("❌ NO HABILITADO. Revisa: Nacionalidad, Deudas o Doble Beneficio.")
    st.stop()
else:
    st.write("✅ Filtros básicos aprobados.")

st.markdown("---")

# --- PASO 2: EVALUACIÓN ACADÉMICA ---
st.subheader("📊 Paso 2: Evaluación Académica")

tipo_estudiante = st.selectbox(
    "Situación del Estudiante:",
    ["Selecciona...", "Estudiante Nuevo (1er año/semestre)", "Estudiante Antiguo"]
)

resultado = "PENDIENTE"

if tipo_estudiante == "Estudiante Nuevo (1er año/semestre)":
    st.info("Regla: Se evalúa situación socioeconómica.")
    puntaje = st.number_input("Puntaje Ficha Socioeconómica (0-100):", 0, 100)
    if puntaje >= 35: resultado = "APROBADO"
    else: resultado = "RECHAZADO_PUNTAJE"

elif tipo_estudiante == "Estudiante Antiguo":
    st.info("Regla: Debes haber vencido la mitad más uno de tus materias.")
    c1, c2 = st.columns(2)
    with c1: inscritas = st.number_input("Materias Inscritas (Semestre Anterior):", 1)
    with c2: aprobadas = st.number_input("Materias Aprobadas:", 0)
    
    minimo = math.floor(inscritas / 2) + 1
    
    if aprobadas >= minimo: resultado = "APROBADO"
    else: resultado = "RECHAZADO_ACADEMICO"

# --- DIAGNÓSTICO FINAL ---
st.markdown("---")
st.subheader("🏁 Diagnóstico Final")

if resultado == "APROBADO":
    st.balloons()
    st.success(f"🎉 ¡ESTÁS HABILITADO PARA: {tipo_beca}!")
    
    with st.expander("📂 VER LISTA DE REQUISITOS (Clic aquí)", expanded=True):
        st.warning("⚠️ El Folder Amarillo debe llevar en la tapa: Nombre, Registro, Carrera y **CELULAR**.")
        st.write("1. **Ficha Socioeconómica** (Lapicero azul).")
        st.write("2. **Ficha Social** (Impresa).")
        st.write("3. **Boleta Inscripción** (1-2025).")
        st.write("4. **Histórico Académico**.")
        st.write("5. **Fotocopia C.I.** (2 copias).")
        st.write("6. **Certificado Nacimiento**.")
        st.write("7. **Croquis Vivienda** (Google Maps).")
        st.write("8. **Factura Luz/Agua**.")
        st.write("9. **Respaldo Ingresos** (Boleta/Certificado).")
        st.write("10. **Folder Amarillo**.")
        
        st.markdown("---")
        st.markdown(f"**➕ REQUISITO ESPECÍFICO PARA {tipo_beca}:**")
        
        if "Alimentación" in tipo_beca:
            st.write("🆔 C.I. Original + Asistencia Biométrica.")
        elif "Estudio" in tipo_beca:
            st.write("📝 Informe Mensual + Carta Solicitud.")
        elif "Investigación" in tipo_beca:
            st.write("🔬 Carta a DICiT + Declaración No Plagio + 2 Perfiles.")
        elif "Extensión" in tipo_beca:
            st.write("📘 2 Proyectos Visados por Jefatura.")

elif resultado == "RECHAZADO_PUNTAJE":
    st.error("❌ NO HABILITADO. Puntaje socioeconómico insuficiente (<35).")
elif resultado == "RECHAZADO_ACADEMICO":
    st.error(f"❌ NO HABILITADO. Te faltaron materias. Necesitabas {minimo}.")
elif resultado == "PENDIENTE":
    st.warning("👈 Completa los datos del Paso 2.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    Desarrollado para Metodología de la Investigación - UAGRM<br>
    ⚠️ Prototipo Académico no vinculante.
</div>
""", unsafe_allow_html=True)
