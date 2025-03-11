import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Inyectar CSS para reducir el espacio entre columnas
st.markdown(
    """
    <style>
    [data-testid="column"] {
         padding: 0 !important;
         margin: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configurar la página en ancho completo
st.set_page_config(layout="wide")

# Título centrado
st.markdown("<h1 style='text-align: center;'>Monitoreo - Argentina</h1>", unsafe_allow_html=True)

# Cargar la hoja 'diarios' del archivo Excel
data_file = 'indicadores_arg.xlsx'
xls = pd.ExcelFile(data_file)
df_diarios = pd.read_excel(xls, sheet_name='diarios')

# Limpiar nombres de columnas
df_diarios.columns = df_diarios.columns.str.strip()

# Convertir la columna de fecha y asegurar que 'Oficial' y 'Blue' sean numéricas,
# reemplazando comas por puntos y quitando espacios
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

# Tomar el último registro para calcular la brecha cambiaria y obtener la fecha
latest_data = df_diarios.iloc[-1]
brecha_pct = ((latest_data['Blue'] - latest_data['Oficial']) / latest_data['Oficial']) * 100
fecha_ultimo = latest_data['fecha_tc'].strftime('%Y-%m-%d')

# Crear dos columnas de igual tamaño para que estén casi pegadas
col1, col2 = st.columns([1, 1])
with col1:
    # Value box estilo tarjeta cuadrada (200x200 px)
    value_box_html = f"""
    <div style="
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        width: 200px;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;">
        <h4 style="margin: 0; font-size: 18px;">Brecha Cambiaria (%)</h4>
        <p style="font-size: 32px; margin: 5px 0;">{brecha_pct:.2f}%</p>
        <p style="font-size: 14px; margin: 0;">Último dato: {fecha_ultimo}</p>
    </div>
    """
    st.markdown(value_box_html, unsafe_allow_html=True)
with col2:
    # Mini gráfico de la evolución del tipo de cambio (Oficial vs Blue)
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
    st.plotly_chart(mini_fig, use_container_width=True, key="mini_chart")
