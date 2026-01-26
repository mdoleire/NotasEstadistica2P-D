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

# Configurar Gemini
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
        
        # Función auxiliar para limpiar notas
        def limpiar_nota(col_idx):
            if col_idx < len(df.columns):
                return pd.to_numeric(df[df.columns[col_idx]], errors='coerce').fillna(0)
            return 0.0

        # Asignación de columnas basada en tus índices
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
        
        # Calculamos/obtenemos el promedio final para mostrarlo al final
        # Si ya viene en el CSV, usas la columna 16 como hiciste arriba.
        # Creamos una columna en minúsculas para facilitar el uso en el prompt si es necesario
        df['promedio_final'] = df['PROMEDIO FINAL']
        
        return df
    except Exception as e:
        st.error(f"⚠️ Error al leer CSV: {e}")
        return None

# --- INTERFAZ ---
st.set_page_config(page_title="Calificaciones Estadística - Miraflores", page_icon="🦁", layout="wide") 
# Nota: Agregué layout="wide" para aprovechar más espacio en pantalla si es posible

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
            # Validación de nombre flexible (insensible a mayúsculas/minúsculas)
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

                # --- DISEÑO MEJORADO (OPCIÓN 1) ---
                # Dividimos las 15 métricas en 3 filas de 5 columnas cada una
                
                st.markdown("##### 📘 Materias Troncales")
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("MATEMÁTICAS IV", row['MATEMATICAS IV'])
                c2.metric("DERECHO", row['DERECHO'])
                c3.metric("LITERATURA", row['LITERATURA'])
                c4.metric("INGLÉS", row['INGLES'])
                c5.metric("PSICOLOGÍA", row['PSICOLOGIA'])

                st.markdown("##### 🌎 Ciencias Sociales y Económicas")
                c6, c7, c8, c9, c10 = st.columns(5)
                c6.metric("GEOGRAFÍA", row['GEOGRAFIA'])
                c7.metric("CS. SOCIALES", row['CIENCIAS SOCIALES'])
                c8.metric("PEMEX", row['PEMEX'])
                c9.metric("CONTABILIDAD", row['CONTABILIDAD'])
                c10.metric("ESTADÍSTICA", row['ESTADISTICA'])

                st.markdown("##### 🏃‍♂️ Formación y Promedios")
                c11, c12, c13, c14, c15 = st.columns(5)
                c11.metric("ED. FÍSICA", row['EDUCACION FISICA'])
                c12.metric("P. PARCIAL", row['PROMEDIO PARCIAL'])
                c13.metric("FRANCÉS", row['FRANCES'])
                c14.metric("ED. EN LA FE", row['EDUCACION EN LA FE'])
                c15.metric("PROMEDIO FINAL", row['PROMEDIO FINAL'])

                st.markdown("---")
                
                # Sección de conclusión
                #col_final, col_msg = st.columns([1, 3])
                #with col_final:
                #     st.metric("🎓 CALIFICACIÓN FINAL", row['promedio_final'])
                #with col_msg:
                #     st.info(f"**Mensaje del Profesor:**\n\n{mensaje}")
                
            else:
                st.error("Nombre incorrecto. Verifica que coincida con el número de lista.")
        else:
            st.error("Número de lista no encontrado.")
