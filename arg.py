import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurar la página en ancho completo
st.set_page_config(layout="wide")

# Título centrado
st.markdown("<h1 style='text-align: center;'>Monitoreo - Argentina</h1>", unsafe_allow_html=True)

# Cargar la hoja 'diarios' del archivo Excel
data_file = 'indicadores_arg.xlsx'
xls = pd.ExcelFile(data_file)
df_diarios = pd.read_excel(xls, sheet_name='diarios')

# Limpiar nombres de columnas (eliminar espacios)
df_diarios.columns = df_diarios.columns.str.strip()

# Convertir la columna de fecha y asegurar que 'Oficial' y 'Blue' sean numéricas
df_diarios['fecha_tc'] = pd.to_datetime(df_diarios['fecha_tc'], errors='coerce')

# Reemplazar comas por puntos y quitar espacios, luego convertir a numérico
df_diarios['Oficial'] = pd.to_numeric(
    df_diarios['Oficial'].astype(str).str.replace(',', '.').str.strip(), errors='coerce'
)
df_diarios['Blue'] = pd.to_numeric(
    df_diarios['Blue'].astype(str).str.replace(',', '.').str.strip(), errors='coerce'
)

# Eliminar filas con datos inválidos en fecha, Oficial o Blue
df_diarios = df_diarios.dropna(subset=['fecha_tc', 'Oficial', 'Blue'])
df_diarios = df_diarios.sort_values(by='fecha_tc')

# Tomar el último registro para calcular la brecha cambiaria
latest_data = df_diarios.iloc[-1]
# Calcular la brecha en porcentaje: ((Blue - Oficial) / Oficial) * 100
brecha_pct = ((latest_data['Blue'] - latest_data['Oficial']) / latest_data['Oficial']) * 100

# Crear dos columnas de igual tamaño para el value box y el mini gráfico
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Brecha Cambiaria (%)", value=f"{brecha_pct:.2f}%")
with col2:
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
        margin=dict(l=10, r=10, t=10, b=10),
        height=100,           # Altura compacta para que coincida con el value box
        xaxis_title=None,
        yaxis_title=None,
        showlegend=True
    )
    st.plotly_chart(mini_fig, use_container_width=True, key="mini_chart")
