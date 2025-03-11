import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Título del dashboard
st.title('Dashboard de Indicadores Argentina')

# Cargar el archivo Excel
data_file = 'indicadores_arg.xlsx'
xls = pd.ExcelFile(data_file)

# Leer las hojas de datos
df_mes = pd.read_excel(xls, sheet_name='Mes')
df_diarios = pd.read_excel(xls, sheet_name='diarios')

# Sección de datos mensuales
st.header("Datos Mensuales")
st.dataframe(df_mes)

# Gráfico interactivo con Plotly: Evolución del IPC interanual general
st.subheader("Evolución del IPC interanual general")
fig1 = px.line(df_mes, x='fecha_mes', y='ipc_yoy_general',
               title='Evolución del IPC interanual general',
               labels={'fecha_mes': 'Fecha', 'ipc_yoy_general': 'IPC interanual general'})
st.plotly_chart(fig1)

# Sección de datos diarios
st.header("Datos Diarios")
st.dataframe(df_diarios)

# Convertir la columna de fecha a datetime (por si no lo está)
df_diarios['fecha_tc'] = pd.to_datetime(df_diarios['fecha_tc'])

# Gráfico interactivo con Plotly: Tipo de cambio Oficial vs Blue
st.subheader("Evolución del Tipo de Cambio (Oficial y Blue)")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_diarios['fecha_tc'], y=df_diarios['Oficial'],
                          mode='lines+markers', name='Oficial'))
fig2.add_trace(go.Scatter(x=df_diarios['fecha_tc'], y=df_diarios['Blue'],
                          mode='lines+markers', name='Blue'))
fig2.update_layout(title='Evolución del Tipo de Cambio',
                   xaxis_title='Fecha', yaxis_title='Tipo de Cambio')
st.plotly_chart(fig2)
