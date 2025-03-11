import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(layout="wide")

# Cargar datos del archivo Excel
data_file = 'indicadores_arg.xlsx'
xls = pd.ExcelFile(data_file)

###############################################################################
# Datos diarios: Tipo de cambio Oficial y Blue
###############################################################################
df_diarios = pd.read_excel(xls, sheet_name='diarios')
df_diarios.columns = df_diarios.columns.str.strip()

# Convertir 'fecha_tc' a datetime y 'Oficial' y 'Blue' a numérico
df_diarios['fecha_tc'] = pd.to_datetime(df_diarios['fecha_tc'], errors='coerce')
df_diarios['Oficial'] = pd.to_numeric(
    df_diarios['Oficial'].astype(str).str.replace(',', '.').str.strip(), errors='coerce'
)
df_diarios['Blue'] = pd.to_numeric(
    df_diarios['Blue'].astype(str).str.replace(',', '.').str.strip(), errors='coerce'
)

# Eliminar filas inválidas y ordenar cronológicamente
df_diarios = df_diarios.dropna(subset=['fecha_tc', 'Oficial', 'Blue'])
df_diarios = df_diarios.sort_values(by='fecha_tc')

# Tomar el último registro para calcular la brecha cambiaria
latest_data = df_diarios.iloc[-1]
brecha_pct = ((latest_data['Blue'] - latest_data['Oficial']) / latest_data['Oficial']) * 100
fecha_ultimo = latest_data['fecha_tc'].strftime('%Y-%m-%d')

###############################################################################
# Datos mensuales: Inflación mensual a partir de ipc_mom_general en la hoja "Mes"
###############################################################################
df_mes = pd.read_excel(xls, sheet_name='Mes')
df_mes.columns = df_mes.columns.str.strip()

# Convertir 'ipc_mom_general' a numérico
df_mes['ipc_mom_general'] = pd.to_numeric(
    df_mes['ipc_mom_general'].astype(str).str.replace(',', '.').str.strip(), errors='coerce'
)

# Si existe una columna con la fecha (por ejemplo, 'Mes'), se procesa la fecha para ordenar cronológicamente
if 'Mes' in df_mes.columns:
    df_mes['Mes'] = pd.to_datetime(df_mes['Mes'], errors='coerce')
    df_mes = df_mes.dropna(subset=['Mes', 'ipc_mom_general'])
    df_mes = df_mes.sort_values(by='Mes')
    latest_inflacion = df_mes.iloc[-1]
    inflacion_value = latest_inflacion['ipc_mom_general']
    fecha_inflacion = latest_inflacion['Mes'].strftime('%Y-%m')
else:
    # En caso de que no haya una columna de fecha, se toma el último registro según el orden original
    df_mes = df_mes.dropna(subset=['ipc_mom_general'])
    df_mes = df_mes.sort_index()
    latest_inflacion = df_mes.iloc[-1]
    inflacion_value = latest_inflacion['ipc_mom_general']
    fecha_inflacion = "N/A"

###############################################################################
# Configuración de estilo para los value boxes
###############################################################################
element_width = 100

st.markdown("<h1 style='text-align: center;'>Monitoreo - Argentina</h1>", unsafe_allow_html=True)

st.markdown(f"""
<style>
div[data-testid="metric-container"] {{
    min-width: 0 !important;
    width: {element_width}px !important;  /* Ancho fijo para la métrica */
    padding: 0.4rem 0.5rem;
    border: 1px solid #CCC;
    border-radius: 5px;
}}
div[data-testid="metric-container"] label {{
    font-size: 0.85rem;
    color: #333;
}}
div[data-testid="metric-container"] .css-1vuvp8l {{
    font-size: 1.2rem;
    color: #000;
}}
</style>
""", unsafe_allow_html=True)

###############################################################################
# Mostrar los indicadores en dos columnas: Brecha cambiaria e Inflación mensual
###############################################################################
col1, col2 = st.columns(2, gap="small")
with col1:
    st.metric(label="Brecha Cambiaria (%)", value=f"{brecha_pct:.2f}%")
    st.caption(f"Último dato: {fecha_ultimo}")
with col2:
    st.metric(label="Inflación Mensual (%)", value=f"{inflacion_value:.2f}%")
    st.caption(f"Último dato: {fecha_inflacion}")
