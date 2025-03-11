import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(layout="wide")

# Cargar datos de la hoja 'diarios'
data_file = 'indicadores_arg.xlsx'
xls = pd.ExcelFile(data_file)
df_diarios = pd.read_excel(xls, sheet_name='diarios')

# Limpiar nombres de columnas
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

# Tomar el último registro para calcular la brecha y obtener la fecha
latest_data = df_diarios.iloc[-1]
brecha_pct = ((latest_data['Blue'] - latest_data['Oficial']) / latest_data['Oficial']) * 100
fecha_ultimo = latest_data['fecha_tc'].strftime('%Y-%m-%d')

# Definir ancho fijo para value box y gráfico
element_width = 150

# Crear mini gráfico con Plotly para mostrar Oficial vs Blue
mini_fig = go.Figure()
mini_fig.add_trace(go.Scatter(
    x=df_diarios['fecha_tc'], y=df_diarios['Oficial'],
    mode='lines', name='Oficial'
))
mini_fig.add_trace(go.Scatter(
    x=df_diarios['fecha_tc'], y=df_diarios['Blue'],
    mode='lines', name='Blue'
))
mini_fig.update_layout(
    margin=dict(l=5, r=5, t=5, b=5),
    width=element_width,   # ancho fijo
    height=150,            # altura reducida
    xaxis_title=None,
    yaxis_title=None,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="center",
        x=0.5
    )
)

# Título centrado
st.markdown("<h1 style='text-align: center;'>Monitoreo - Argentina</h1>", unsafe_allow_html=True)

###############################################################################
# CSS para ajustar el contenedor del value box (st.metric)
###############################################################################
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

# Dividir la página en dos columnas para que queden pegadas y con ancho fijo
col1, col2 = st.columns(2, gap="small")
with col1:
    st.metric(label="Brecha Cambiaria (%)", value=f"{brecha_pct:.2f}%")
    st.caption(f"Último dato: {fecha_ultimo}")
with col2:
    # Se remueve use_container_width para respetar el ancho fijo configurado en el layout del gráfico
    st.plotly_chart(mini_fig, use_container_width=False)
