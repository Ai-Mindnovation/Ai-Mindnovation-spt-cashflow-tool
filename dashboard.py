"""
SPT CASH FLOW TOOL - Dashboard Streamlit (Versión Simplificada)
================================================================
Dashboard de análisis de flujo de efectivo para SPT Colombia

Autor: AI-MindNovation
Cliente: SPT Colombia
Fecha: Noviembre 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="SPT Cash Flow Tool",
    page_icon="💰",
    layout="wide"
)

# Estilos CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #2563EB;
        text-align: center;
        padding: 1rem 0;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">💰 SPT CASH FLOW TOOL</div>', unsafe_allow_html=True)
st.markdown(f"**Estado al:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ SPT Colombia")
    st.markdown("**Análisis de Flujo de Efectivo**")
    st.markdown("---")
    
    page = st.radio(
        "Navegación:",
        ["🏠 Resumen Ejecutivo", "📈 Análisis Histórico", "💵 Proyecciones"]
    )
    
    st.markdown("---")
    st.markdown("**Desarrollado por:**")
    st.markdown("[AI-MindNovation](https://www.ai-mindnovation.com)")

# Página: Resumen Ejecutivo
if page == "🏠 Resumen Ejecutivo":
    st.markdown("## 🎯 Resumen Ejecutivo")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("💰 Efectivo", "$80,000", "+5.2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("📊 Revenue", "$185,661", "+12.3%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("🔥 Burn Rate", "$87,089", "-3.1%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("⏱️ Runway", "8.5 meses")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráfico
    st.markdown("### 📈 Tendencia de Revenue")
    
    df = pd.DataFrame({
        'mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        'revenue': [120000, 135000, 128000, 145000, 138000, 152000, 148000, 155000, 162000, 158000, 165000, 172000]
    })
    
    fig = px.line(df, x='mes', y='revenue', markers=True)
    fig.update_traces(line_color='#2563EB', line_width=3)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recomendación
    st.success("""
    **✅ EXCEDENTE DE EFECTIVO**
    
    - Efectivo disponible: $80,000
    - Necesidades próximos 3 meses: $30,000
    - **Excedente para inversión: $50,000**
    """)

# Página: Análisis Histórico
elif page == "📈 Análisis Histórico":
    st.markdown("## 📈 Análisis Histórico (2023-2025)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Revenue Promedio", "$185,661")
    with col2:
        st.metric("Revenue Mínimo", "$120,000")
    with col3:
        st.metric("Revenue Máximo", "$172,000")
    
    st.markdown("### 👥 Top 5 Clientes")
    
    df_clients = pd.DataFrame({
        'Cliente': ['Kluane/Aris', 'Explomin', 'Kluane', 'Office', 'SPT Colombia'],
        'Revenue': [549800, 496700, 490575, 481310, 445850]
    })
    
    fig = px.bar(df_clients, x='Revenue', y='Cliente', orientation='h')
    fig.update_traces(marker_color='#2563EB')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Página: Proyecciones
elif page == "💵 Proyecciones":
    st.markdown("## 💵 Proyecciones de Flujo de Efectivo")
    
    meses = st.slider("Meses a proyectar:", 1, 12, 3)
    
    df_proj = pd.DataFrame({
        'mes': [f'Mes {i+1}' for i in range(meses)],
        'ingresos': [180000 + (i * 5000) for i in range(meses)],
        'gastos': [87000] * meses
    })
    df_proj['flujo_neto'] = df_proj['ingresos'] - df_proj['gastos']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Ingresos', x=df_proj['mes'], y=df_proj['ingresos'], marker_color='#10B981'))
    fig.add_trace(go.Bar(name='Gastos', x=df_proj['mes'], y=df_proj['gastos'], marker_color='#EF4444'))
    
    fig.update_layout(
        title='Proyección de Flujo de Efectivo',
        height=500,
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla
    st.dataframe(df_proj, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B;'>
    <p><strong>SPT Cash Flow Tool v4.1</strong></p>
    <p>Desarrollado por <a href='https://www.ai-mindnovation.com'>AI-MindNovation</a></p>
</div>
""", unsafe_allow_html=True)
