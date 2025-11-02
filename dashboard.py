"""
SPT CASH FLOW TOOL - Dashboard Streamlit
=========================================
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
import json
from pathlib import Path
import sys

# Configuración de la página
st.set_page_config(
    page_title="SPT Cash Flow Tool",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2563EB;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #64748B;
        text-align: center;
        padding-bottom: 2rem;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E293B;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #64748B;
        text-transform: uppercase;
    }
    .metric-positive {
        color: #10B981;
    }
    .metric-negative {
        color: #EF4444;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def format_money(value):
    """Formatea valores monetarios"""
    if pd.isna(value) or value is None:
        return "$0"
    return f"${value:,.0f}"

def format_percentage(value):
    """Formatea porcentajes"""
    if pd.isna(value) or value is None:
        return "0.0%"
    return f"{value * 100:.1f}%"

def create_kpi_card(label, value, icon="💰", trend=None):
    """Crea una tarjeta KPI"""
    trend_html = ""
    if trend is not None:
        color = "metric-positive" if trend >= 0 else "metric-negative"
        arrow = "↑" if trend >= 0 else "↓"
        trend_html = f'<span class="{color}">{arrow} {abs(trend):.1f}%</span>'
    
    html = f"""
    <div class="kpi-card">
        <div style="font-size: 2rem;">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {trend_html}
    </div>
    """
    return html

def load_demo_data():
    """Carga datos de demostración"""
    # Datos históricos simulados
    historical_data = {
        'periodo': ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06',
                   '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', '2023-12'],
        'revenue': [120000, 135000, 128000, 145000, 138000, 152000,
                   148000, 155000, 162000, 158000, 165000, 172000]
    }
    
    return pd.DataFrame(historical_data)

# =============================================================================
# INTERFAZ PRINCIPAL
# =============================================================================

def main():
    # Header
    st.markdown('<div class="main-header">💰 SPT CASH FLOW TOOL</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Análisis de Flujo de Efectivo - SPT Colombia</div>', unsafe_allow_html=True)
    st.markdown(f"**📅 Estado al:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/2563EB/FFFFFF?text=SPT+Colombia", use_column_width=True)
        st.markdown("### ⚙️ Configuración")
        
        # Opción de carga de datos
        data_source = st.radio(
            "Fuente de datos:",
            ["Datos de demostración", "Cargar archivos propios"]
        )
        
        if data_source == "Cargar archivos propios":
            st.markdown("#### 📁 Subir Archivos")
            
            st.markdown("**Archivos Históricos (2023-2025):**")
            file_2023 = st.file_uploader("Utilization Report 2023", type=['xlsx', 'xls'], key="2023")
            file_2024 = st.file_uploader("Utilization Report 2024", type=['xlsx', 'xls'], key="2024")
            file_2025 = st.file_uploader("Utilization Report 2025", type=['xlsx', 'xls'], key="2025")
            
            st.markdown("**Estado Actual:**")
            file_weekly = st.file_uploader("Weekly Report", type=['xlsx', 'xls'], key="weekly")
            
            st.markdown("**Financiero:**")
            file_financial = st.file_uploader("Estado Financiero", type=['xlsx', 'xls'], key="financial")
            
            if st.button("🚀 Procesar Archivos"):
                if file_2023 and file_2024 and file_2025 and file_weekly and file_financial:
                    with st.spinner("Procesando archivos..."):
                        st.success("✅ Archivos procesados correctamente")
                        st.info("💡 Nota: En producción, aquí se ejecutaría el backend completo")
                else:
                    st.warning("⚠️ Por favor sube todos los archivos requeridos")
        
        st.markdown("---")
        st.markdown("### 📊 Navegación")
        page = st.radio(
            "Selecciona sección:",
            ["🏠 Resumen Ejecutivo", 
             "📈 Análisis Histórico", 
             "💵 Proyecciones",
             "📊 Reportes Detallados"]
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Información")
        st.markdown("""
        **Desarrollado por:**  
        AI-MindNovation
        
        **Cliente:**  
        SPT Colombia
        
        **Versión:** 4.1
        """)
    
    # Contenido principal
    if page == "🏠 Resumen Ejecutivo":
        show_executive_summary()
    elif page == "📈 Análisis Histórico":
        show_historical_analysis()
    elif page == "💵 Proyecciones":
        show_projections()
    elif page == "📊 Reportes Detallados":
        show_detailed_reports()

def show_executive_summary():
    """Muestra resumen ejecutivo con KPIs principales"""
    st.markdown("## 🎯 Resumen Ejecutivo")
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card("Efectivo Disponible", "$80,000", "💰", 5.2), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card("Revenue Mensual", "$185,661", "📊", 12.3), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card("Burn Rate", "$87,089", "🔥", -3.1), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card("Runway", "8.5 meses", "⏱️", None), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráfico de tendencia
    st.markdown("### 📈 Tendencia de Revenue (2023-2025)")
    df = load_demo_data()
    
    fig = px.line(df, x='periodo', y='revenue', 
                  title='Revenue Mensual Histórico',
                  labels={'periodo': 'Período', 'revenue': 'Revenue (USD)'},
                  markers=True)
    fig.update_traces(line_color='#2563EB', line_width=3)
    fig.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Análisis de flujo de efectivo
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💵 Flujo de Efectivo Proyectado")
        cash_flow_data = {
            'mes': ['Nov-25', 'Dic-25', 'Ene-26'],
            'flujo': [45000, 52000, 38000]
        }
        df_cash = pd.DataFrame(cash_flow_data)
        
        fig = go.Figure(data=[
            go.Bar(x=df_cash['mes'], y=df_cash['flujo'],
                   marker_color=['#10B981', '#10B981', '#10B981'])
        ])
        fig.update_layout(
            title='Próximos 3 Meses',
            xaxis_title='Mes',
            yaxis_title='Flujo Neto (USD)',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Recomendación")
        st.success("""
        **✅ EXCEDENTE DE EFECTIVO**
        
        Basado en el análisis actual:
        - Efectivo disponible: $80,000
        - Necesidades próximos 3 meses: $30,000
        - **Excedente para inversión: $50,000**
        
        **Recomendaciones:**
        1. Asignar 30% a reserva de emergencia
        2. Invertir 40% en expansión
        3. Usar 30% para pago adelantado de deudas
        """)

def show_historical_analysis():
    """Muestra análisis histórico detallado"""
    st.markdown("## 📈 Análisis Histórico (2023-2025)")
    
    df = load_demo_data()
    
    # Métricas históricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_revenue = df['revenue'].mean()
        st.metric("Revenue Promedio", format_money(avg_revenue))
    
    with col2:
        min_revenue = df['revenue'].min()
        st.metric("Revenue Mínimo", format_money(min_revenue))
    
    with col3:
        max_revenue = df['revenue'].max()
        st.metric("Revenue Máximo", format_money(max_revenue))
    
    # Gráfico histórico
    fig = px.area(df, x='periodo', y='revenue',
                  title='Evolución Histórica del Revenue',
                  labels={'periodo': 'Período', 'revenue': 'Revenue (USD)'})
    fig.update_traces(line_color='#2563EB', fillcolor='rgba(37, 99, 235, 0.2)')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top clientes
    st.markdown("### 👥 Top 5 Clientes Históricos")
    top_clients = pd.DataFrame({
        'Cliente': ['Kluane/Aris', 'Explomin/Segovia', 'Kluane', 'Office', 'SPT Colombia'],
        'Revenue Total': [549800, 496700, 490575, 481310, 445850]
    })
    
    fig = px.bar(top_clients, x='Revenue Total', y='Cliente', orientation='h',
                 title='Revenue por Cliente (2023-2025)',
                 labels={'Revenue Total': 'Revenue Total (USD)', 'Cliente': ''})
    fig.update_traces(marker_color='#2563EB')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_projections():
    """Muestra proyecciones de flujo de efectivo"""
    st.markdown("## 💵 Proyecciones de Flujo de Efectivo")
    
    st.info("📊 **Nota:** Estas son proyecciones basadas en datos históricos y factores estacionales")
    
    # Parámetros de proyección
    col1, col2 = st.columns(2)
    
    with col1:
        meses = st.slider("Meses a proyectar:", 1, 12, 3)
    
    with col2:
        escenario = st.selectbox("Escenario:", ["Conservador", "Base", "Optimista"])
    
    # Datos de proyección simulados
    projection_data = {
        'mes': [f'Mes {i+1}' for i in range(meses)],
        'ingresos': [180000 + (i * 5000) for i in range(meses)],
        'gastos': [87000] * meses
    }
    df_proj = pd.DataFrame(projection_data)
    df_proj['flujo_neto'] = df_proj['ingresos'] - df_proj['gastos']
    
    # Gráfico de proyección
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Ingresos', x=df_proj['mes'], y=df_proj['ingresos'],
                         marker_color='#10B981'))
    fig.add_trace(go.Bar(name='Gastos', x=df_proj['mes'], y=df_proj['gastos'],
                         marker_color='#EF4444'))
    fig.add_trace(go.Scatter(name='Flujo Neto', x=df_proj['mes'], y=df_proj['flujo_neto'],
                            mode='lines+markers', line=dict(color='#2563EB', width=3)))
    
    fig.update_layout(
        title=f'Proyección de Flujo de Efectivo - Escenario {escenario}',
        xaxis_title='Período',
        yaxis_title='Monto (USD)',
        height=500,
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de proyección
    st.markdown("### 📋 Detalle de Proyección")
    df_display = df_proj.copy()
    df_display['ingresos'] = df_display['ingresos'].apply(format_money)
    df_display['gastos'] = df_display['gastos'].apply(format_money)
    df_display['flujo_neto'] = df_display['flujo_neto'].apply(format_money)
    df_display.columns = ['Mes', 'Ingresos Proyectados', 'Gastos Proyectados', 'Flujo Neto']
    st.dataframe(df_display, use_container_width=True)

def show_detailed_reports():
    """Muestra reportes detallados"""
    st.markdown("## 📊 Reportes Detallados")
    
    tabs = st.tabs(["📈 Estacionalidad", "🔥 Burn Rate", "💰 Balance", "📄 Exportar"])
    
    with tabs[0]:
        st.markdown("### 📅 Análisis de Estacionalidad")
        seasonal_data = pd.DataFrame({
            'Mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                   'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            'Factor': [1.15, 0.85, 1.05, 0.95, 1.10, 1.20, 1.08, 0.92, 1.03, 1.12, 0.98, 1.18]
        })
        
        fig = go.Figure(data=go.Scatterpolar(
            r=seasonal_data['Factor'],
            theta=seasonal_data['Mes'],
            fill='toself',
            line=dict(color='#2563EB')
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1.5])),
            title='Factores Estacionales por Mes',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        st.markdown("### 🔥 Análisis de Burn Rate")
        st.metric("Burn Rate Mensual", "$87,089")
        st.metric("Gastos Fijos", "$65,000")
        st.metric("Costos Variables", "$22,089")
        
        burn_breakdown = pd.DataFrame({
            'Categoría': ['Salarios', 'Logística', 'Mantenimiento', 'Administrativos', 'Otros'],
            'Monto': [40000, 15000, 12000, 10000, 10089]
        })
        
        fig = px.pie(burn_breakdown, values='Monto', names='Categoría',
                     title='Distribución del Burn Rate')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        st.markdown("### 💰 Balance Proyectado")
        balance_data = pd.DataFrame({
            'Mes': ['Nov-25', 'Dic-25', 'Ene-26'],
            'Efectivo Inicial': [80000, 125000, 177000],
            'Ingresos': [185000, 192000, 180000],
            'Gastos': [140000, 140000, 142000],
            'Efectivo Final': [125000, 177000, 215000]
        })
        
        st.dataframe(balance_data.style.format({
            'Efectivo Inicial': '${:,.0f}',
            'Ingresos': '${:,.0f}',
            'Gastos': '${:,.0f}',
            'Efectivo Final': '${:,.0f}'
        }), use_container_width=True)
    
    with tabs[3]:
        st.markdown("### 📄 Exportar Reportes")
        st.markdown("Selecciona el formato de exportación:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Exportar Excel"):
                st.info("Funcionalidad de exportación disponible en versión completa")
        with col2:
            if st.button("📄 Exportar PDF"):
                st.info("Funcionalidad de exportación disponible en versión completa")
        with col3:
            if st.button("💾 Exportar JSON"):
                st.info("Funcionalidad de exportación disponible en versión completa")

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    main()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; padding: 2rem 0;'>
    <p><strong>SPT Cash Flow Tool v4.1</strong></p>
    <p>Desarrollado por <a href='https://www.ai-mindnovation.com' target='_blank'>AI-MindNovation</a></p>
    <p>© 2025 AI-MindNovation. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
