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

# Limpiar nombres de columnas para evitar problemas de espacios u otros caracteres
df_diarios.columns = df_diarios.columns.str.strip()

# Convertir la columna de fecha a formato datetime
df_diarios['fecha_tc'] = pd.to_datetime(df_diarios['fecha_tc'])

# Ordenar por fecha (para tener la serie ordenada cronológicamente)
df_diarios = df_diarios.sort_values(by='fecha_tc')

# Obtener el último dato para calcular la brecha cambiaria
latest_data = df_diarios.iloc[-1]

# Calcular la brecha cambiaria en porcentaje: ((Blue - Oficial) / Oficial)*100
brecha_pct = ((latest_data['Blue'] - latest_data['Oficial']) / latest_data['Oficial']) * 100

# Crear dos columnas: una para el value box y otra para el mini gráfico
col_metric, col_chart = st.columns([1, 2])
with col_metric:
    st.metric(label="Brecha Cambiaria (%)", value=f"{brecha_pct:.2f}%")
with col_chart:
    # Crear mini gráfico con Plotly que muestre las series de Oficial y Blue
    mini_fig = go.Figure()
    mini_fig.add_trace(go.Scatter(
        x=df_diarios['fecha_tc'],
        y=df_diarios['Oficial'],
        mode='lines',
        name='Oficial'
    ))
    mini_fig.add_trace(go.Scatter(
        x=df_diarios['fecha_tc'],
        y=df_diarios['Blue'],
        mode='lines',
        name='Blue'
    ))
    mini_fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=200,
        xaxis_title="Fecha",
        yaxis_title="Valor",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(mini_fig, use_container_width=True, key="mini_chart")
