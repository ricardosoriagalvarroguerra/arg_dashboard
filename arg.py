import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Dashboard de Indicadores Argentina")

# Cargar el archivo Excel
data_file = 'indicadores_arg.xlsx'
xls = pd.ExcelFile(data_file)

# Cargar datos de cada hoja
df_mes = pd.read_excel(xls, sheet_name='Mes')
df_diarios = pd.read_excel(xls, sheet_name='diarios')

# Limpiar nombres de columnas para evitar problemas con espacios o caracteres no deseados
df_mes.columns = df_mes.columns.str.strip()
df_diarios.columns = df_diarios.columns.str.strip()

# Convertir las columnas de fecha a datetime
df_mes['fecha_mes'] = pd.to_datetime(df_mes['fecha_mes'])
df_diarios['fecha_itcrm'] = pd.to_datetime(df_diarios['fecha_itcrm'])
df_diarios['fecha_rin'] = pd.to_datetime(df_diarios['fecha_rin'])
df_diarios['fecha_riesgopais'] = pd.to_datetime(df_diarios['fecha_riesgopais'])
df_diarios['fecha_tc'] = pd.to_datetime(df_diarios['fecha_tc'])

# Mostrar los nombres de las columnas para depuración (opcional)
st.write("Columnas en df_diarios:", df_diarios.columns)

# Crear pestañas para organizar los gráficos
tab1, tab2 = st.tabs(["Datos Mensuales", "Datos Diarios"])

# -----------------------------
# Pestaña: Datos Mensuales
# -----------------------------
with tab1:
    st.header("Datos Mensuales")
    st.dataframe(df_mes)

    # Gráfico 1: Evolución de IPC Interanual (varios indicadores)
    st.subheader("Evolución de IPC Interanual")
    fig_ipc = go.Figure()
    fig_ipc.add_trace(go.Scatter(x=df_mes['fecha_mes'], y=df_mes['ipc_yoy_general'],
                                 mode='lines+markers', name='IPC YoY General'))
    fig_ipc.add_trace(go.Scatter(x=df_mes['fecha_mes'], y=df_mes['ipc_yoy_estacional'],
                                 mode='lines+markers', name='IPC YoY Estacional'))
    fig_ipc.add_trace(go.Scatter(x=df_mes['fecha_mes'], y=df_mes['ipc_yoy_nucleo'],
                                 mode='lines+markers', name='IPC YoY Núcleo'))
    fig_ipc.add_trace(go.Scatter(x=df_mes['fecha_mes'], y=df_mes['ipc_yoy_regulados'],
                                 mode='lines+markers', name='IPC YoY Regulados'))
    fig_ipc.update_layout(title="Evolución de IPC Interanual",
                          xaxis_title="Fecha", yaxis_title="Variación (%)")
    st.plotly_chart(fig_ipc, use_container_width=True)

    # Gráfico 2: IPC Mom General
    st.subheader("Evolución del IPC Mom General")
    fig_ipc_mom = px.line(df_mes, x='fecha_mes', y='ipc_mom_general', 
                          title="Evolución del IPC Mom General",
                          labels={'fecha_mes': 'Fecha', 'ipc_mom_general': 'IPC Mom General'})
    st.plotly_chart(fig_ipc_mom, use_container_width=True)

    # Gráfico 3: Exportaciones e Importaciones
    st.subheader("Evolución de Exportaciones e Importaciones")
    fig_trade = go.Figure()
    fig_trade.add_trace(go.Scatter(x=df_mes['fecha_mes'], y=df_mes['exports'],
                                   mode='lines+markers', name='Exportaciones'))
    fig_trade.add_trace(go.Scatter(x=df_mes['fecha_mes'], y=df_mes['imports'],
                                   mode='lines+markers', name='Importaciones'))
    fig_trade.update_layout(title="Exportaciones e Importaciones",
                            xaxis_title="Fecha", yaxis_title="Valor")
    st.plotly_chart(fig_trade, use_container_width=True)

# -----------------------------
# Pestaña: Datos Diarios
# -----------------------------
with tab2:
    st.header("Datos Diarios")
    st.dataframe(df_diarios)

    # Gráfico 4: ITCRM
    st.subheader("Evolución del ITCRM")
    fig_itcrm = px.line(df_diarios, x='fecha_itcrm', y='itcrm', 
                        title="Evolución del ITCRM",
                        labels={'fecha_itcrm': 'Fecha', 'itcrm': 'ITCRM'})
    st.plotly_chart(fig_itcrm, use_container_width=True)

    # Gráfico 5: Reservas Internacionales
    st.subheader("Evolución de Reservas Internacionales")
    fig_reservas = px.line(df_diarios, x='fecha_rin', y='Reservas', 
                           title="Evolución de Reservas Internacionales",
                           labels={'fecha_rin': 'Fecha', 'Reservas': 'Reservas'})
    st.plotly_chart(fig_reservas, use_container_width=True)

    # Gráfico 6: Riesgo País
    st.subheader("Evolución del Riesgo País")
    fig_riesgo = px.line(df_diarios, x='fecha_riesgopais', y='riesgopais', 
                         title="Evolución del Riesgo País",
                         labels={'fecha_riesgopais': 'Fecha', 'riesgopais': 'Riesgo País'})
    st.plotly_chart(fig_riesgo, use_container_width=True)

    # Gráfico 7: Tipo de Cambio: Oficial vs Blue
    st.subheader("Evolución del Tipo de Cambio (Oficial vs Blue)")
    fig_tc = go.Figure()
    fig_tc.add_trace(go.Scatter(x=df_diarios['fecha_tc'], y=df_diarios['Oficial'],
                                mode='lines+markers', name='Oficial'))
    fig_tc.add_trace(go.Scatter(x=df_diarios['fecha_tc'], y=df_diarios['Blue'],
                                mode='lines+markers', name='Blue'))
    fig_tc.update_layout(title="Evolución del Tipo de Cambio",
                         xaxis_title="Fecha", yaxis_title="Valor")
    st.plotly_chart(fig_tc, use_container_width=True)
