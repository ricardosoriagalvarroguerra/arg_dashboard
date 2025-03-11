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

# Limpiar nombres de columnas para evitar espacios u otros caracteres extra
df_diarios.columns = df_diarios.columns.str.strip()

# Convertir la columna de fecha a formato datetime
df_diarios['fecha_tc'] = pd.to_datetime(df_diarios['fecha_tc'])

# Ordenar por fecha (opcional) y obtener el último dato para calcular la brecha cambiaria
df_diarios = df_diarios.sort_values(by='fecha_tc')
latest_data = df_diarios.iloc[-1]

# Calcular la brecha cambiaria: diferencia entre Blue y Oficial
brecha = latest_data['Blue'] - latest_data['Oficial']

# Crear un value box usando columnas: una para la métrica y otra para el mini gráfico
col1, col2 = st.columns([1, 2])
with col1:
    st.metric(label="Brecha Cambiaria", value=f"{brecha:.2f}")
with col2:
    # Crear mini gráfico con Plotly para mostrar ambas series
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
        margin=dict(l=20, r=20, t=20, b=20),
        height=200,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=True
    )
    st.plotly_chart(mini_fig, use_container_width=True)
    
    # Expander para ver el gráfico en tamaño completo
    with st.expander("Ampliar gráfico"):
        st.plotly_chart(mini_fig, use_container_width=True)
