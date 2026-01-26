import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- CONFIGURACIÓN SEGURA ---
# El código buscará la llave en la caja fuerte de Streamlit
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ No se detectó la API Key en los Secrets de Streamlit.")
    st.stop()

# Configurar Gemini (Usamos el modelo estándar actual)
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

# --- FUNCIÓN PARA CARGAR DATOS ---
def cargar_datos():
    archivo_nombre = "ReportePeriodo2.csv"
    try:
        df = pd.read_csv(archivo_nombre)
        
        # Limpieza básica
        if len(df.columns) > 1:
            rename_map = {df.columns[0]: 'numero_lista', df.columns[1]: 'nombre'}
            df = df.rename(columns=rename_map)
        
        df = df[pd.to_numeric(df['numero_lista'], errors='coerce').notna()]
        df['numero_lista'] = df['numero_lista'].astype(float).astype(int).astype(str)
        
        # Mapeo de columnas (Ajustado a tu duda anterior: Indice = Excel - 1)
        def limpiar_nota(col_idx):
            if col_idx < len(df.columns):
                return pd.to_numeric(df[df.columns[col_idx]], errors='coerce').fillna(0)
            return 0.0

        # Ajusta estos índices si cambiaste columnas en el Excel
        # Recuerda: Columna 17 en Excel es índice 16 en Python
        df['MATEMATICAS IV'] = limpiar_nota(2) 
        df['DERECHO'] = limpiar_nota(3)
        df['LITERATURA'] = limpiar_nota(4)
        df['INGLES'] = limpiar_nota(5)
        df['PSICOLOGIA'] = limpiar_nota(6)
        df['GEOGRAFIA'] = limpiar_nota(7)
        df['CIENCIAS SOCIALES'] = limpiar_nota(8)
        df['PEMEX'] = limpiar_nota(9)
        df['CONTABILIDAD'] = limpiar_nota(10)
        df['ESTADISTICA'] = limpiar_nota(11)
        df['EDUCACION FISICA'] = limpiar_nota(12)
        df['PROMEDIO PARCIAL'] = limpiar_nota(13)
        df['FRANCES'] = limpiar_nota(14)
        df['EDUCACION EN LA FE'] = limpiar_nota(15)
        df['PROMEDIO FINAL'] = limpiar_nota(16)
        return df
    except Exception as e:
        st.error(f"⚠️ Error al leer CSV: {e}")
        return None

# --- INTERFAZ ---
st.set_page_config(page_title="Calificaciones Estadística - Miraflores", page_icon="🦁")
st.title("🦁 Consulta de Calificaciones")
st.subheader("Periodo 2: Calificaciones 6° D")

col1, col2 = st.columns(2)
num = col1.text_input("Número de Lista:")
nom = col2.text_input("Primer Nombre:")

if st.button("Ver Resultados"):
    df = cargar_datos()
    if df is not None and num and nom:
        alumno = df[df['numero_lista'] == num.strip()]
        if not alumno.empty:
            nombre_real = alumno.iloc[0]['nombre']
            if isinstance(nombre_real, str) and nom.lower().strip() in nombre_real.lower():
                row = alumno.iloc[0]
                
                # --- FEEDBACK IA ---
                mensaje = ""
                try:
                    prompt = f"Actúa como un profesor amable, no des muchos rodeos. Alumno: {nombre_real}. Nota: {row['promedio_final']} Resalta la calificación obtenida en el periodo. Motívalo brevemente, una buena calificación va de 85 para arriba, una calificación media de 70 a 85 y una calificación mala de 70 69 para abajo, aunque la aprobatoria es 60 hay que motivarlos. Firma como 'Atentamente: Marco'."
                    with st.spinner('Analizando desempeño...'):
                        response = model.generate_content(prompt)
                        mensaje = response.text
                except Exception as e:
                    mensaje = f"Buen esfuerzo. (El sistema de IA está descansando: {str(e)})"

                st.success(f"Alumno: {nombre_real}")
                c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15  = st.columns(15)
                c1.metric("MATEMÁTICAS IV", row['MATEMATICAS IV'])
                c2.metric("DERECHO", row['DERECHO'])
                c3.metric("LITERATURA", row['LITERATURA'])
                c4.metric("INGLÉS", row['INGLES'])
                c5.metric("PSICOLOGÍA", row['PSICOLOGIA'])
                c6.metric("GEOGRAFÍA", row['GEOGRAFIA'])
                c7.metric("CIENCIAS SOCIALES", row['CIENCIAS SOCIALES'])
                c8.metric("PEMEX", row['PEMEX'])
                c9.metric("CONTABILIDAD", row['CONTABILIDAD'])
                c10.metric("ESTADÍSTICA", row['ESTADISTICA'])
                c11.metric("EDUCACIÓN FÍSICA", row['EDUCACION FISICA'])
                c12.metric("PROMEDIO PARCIAL", row['PROMEDIO PARCIAL'])
                c13.metric("FRANCÉS", row['FRANCES'])
                c14.metric("EDUCACIÓN EN LA FE", row['EDUCACION EN LA FE'])
                c15.metric("PROMEDIO FINAL", row['PROMEDIO FINAL'])
                #st.info(f"**Comentario del Profe:** {mensaje}")
            else:
                st.error("Nombre incorrecto.")
        else:
            st.error("Lista no encontrada.")







