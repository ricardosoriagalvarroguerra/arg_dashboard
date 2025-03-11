import streamlit as st
st.set_page_config(layout="wide")  # DEBE estar al inicio

import pandas as pd
import plotly.graph_objects as go

# ---------------------------
# Procesamiento de datos
# ---------------------------
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

# Crear mini gráfico con Plotly para mostrar las series
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
    height=200,
    xaxis_title=None,
    yaxis_title=None,
    showlegend=True
)

# ---------------------------
# Diseño del Dashboard
# ---------------------------

# Título centrado
st.markdown("<h1 style='text-align: center;'>Monitoreo - Argentina</h1>", unsafe_allow_html=True)

# Inyectar CSS para la tarjeta (card)
st.markdown(
    """
    <style>
    .card-container {
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: #f0f2f6;
        padding: 10px;
        margin: 0 auto;
        max-width: 800px;
    }
    .card-container .card-metric {
        flex: 1;
        text-align: center;
        padding: 10px;
    }
    .card-container .card-chart {
        flex: 2;
        padding: 10px;
    }
    .card-content {
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Crear la tarjeta que integra el value box y el gráfico
with st.container():
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-content">', unsafe_allow_html=True)
    # Sección del value box (métrica)
    st.markdown(
        f"""
        <div class="card-metric">
            <h4 style="margin: 0;">Brecha Cambiaria (%)</h4>
            <p style="font-size:32px; margin: 5px 0;">{brecha_pct:.2f}%</p>
            <p style="font-size:14px; margin: 0;">Último dato: {fecha_ultimo}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Sección del mini gráfico
    st.markdown('<div class="card-chart">', unsafe_allow_html=True)
    st.plotly_chart(mini_fig, use_container_width=True, key="mini_chart")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
