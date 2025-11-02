# 💰 SPT Cash Flow Tool

Dashboard interactivo de análisis de flujo de efectivo para SPT Colombia.

## 🎯 Descripción

Herramienta de análisis financiero que consolida datos históricos (2023-2025), calcula proyecciones y proporciona recomendaciones estratégicas para la gestión del flujo de efectivo.

## ✨ Funcionalidades

### 📊 Análisis Disponibles
- **Resumen Ejecutivo**: KPIs principales y tendencias
- **Análisis Histórico**: Revenue histórico (2023-2025) y top clientes
- **Proyecciones**: Flujo de efectivo proyectado con múltiples escenarios
- **Reportes Detallados**: Estacionalidad, Burn Rate, Balance proyectado

### 💡 Características Clave
- ✅ Cálculo automático de Burn Rate (gastos fijos + variables)
- ✅ Proyecciones con factores estacionales
- ✅ Análisis de necesidades/excedentes de efectivo
- ✅ Recomendaciones de inversión automáticas
- ✅ Visualizaciones interactivas con Plotly
- ✅ Carga de datos propia o modo demostración

## 🚀 Uso

### Acceso Online
La aplicación está disponible en:
- **Dashboard**: https://www.ai-mindnovation.com/spt-cashflow
- **Streamlit Direct**: [URL de Streamlit Cloud]

### Modo Demostración
1. Selecciona "Datos de demostración" en el sidebar
2. Navega por las diferentes secciones del dashboard
3. Explora las visualizaciones y métricas

### Modo con Datos Propios
1. Selecciona "Cargar archivos propios" en el sidebar
2. Sube los siguientes archivos Excel:
   - Utilization Report 2023
   - Utilization Report 2024
   - Utilization Report 2025
   - Weekly Operation Report (estado actual)
   - Estado Financiero
3. Click en "Procesar Archivos"
4. El dashboard se actualiza con tus datos

## 📁 Estructura de Archivos Requeridos

### Utilization Reports (2023-2025)
Columnas esperadas:
- `Date`: Fecha en formato mmm-aa (ej: ene-25)
- `Client`: Nombre del cliente
- `Accrual Revenue`: Ingresos reales devengados

### Weekly Operation Report
Columnas esperadas:
- Información de equipos disponibles
- Estado de contratos activos
- Utilización actual

### Estado Financiero
Columnas esperadas:
- Costos fijos mensuales
- Costos variables
- Gastos operacionales

## 🛠️ Tecnologías

- **Frontend**: Streamlit
- **Visualizaciones**: Plotly
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Cloud
- **Version Control**: GitHub

## 📊 Métricas Calculadas

### KPIs Principales
- **Efectivo Disponible**: Monto actual en caja
- **Revenue Mensual**: Promedio de ingresos mensuales
- **Burn Rate**: Gastos mensuales totales (fijos + variables)
- **Runway**: Meses de operación con efectivo actual

### Análisis Avanzados
- Factores estacionales por mes
- Proyecciones multi-escenario
- Top clientes históricos
- Distribución de gastos

## 🔒 Seguridad y Privacidad

- ❌ **NO se almacenan datos**: Los archivos subidos se procesan en memoria
- ❌ **NO hay persistencia**: Los datos se eliminan al cerrar la sesión
- ✅ **Privacidad garantizada**: Tus datos nunca se guardan en el servidor
- ✅ **Repositorio privado**: El código fuente es privado

## 👥 Autores

**Desarrollado por**: [AI-MindNovation](https://www.ai-mindnovation.com)  
**Cliente**: SPT Colombia  
**Versión**: 4.1  
**Fecha**: Noviembre 2025

## 📝 Licencia

© 2025 AI-MindNovation. Todos los derechos reservados.  
Desarrollado exclusivamente para SPT Colombia.

## 📧 Contacto

Para soporte o consultas:
- **Website**: https://www.ai-mindnovation.com
- **Email**: contacto@ai-mindnovation.com

---

**Nota para desarrolladores**: Este es el frontend (dashboard) del sistema. El backend completo con parsers y análisis está en archivos separados no incluidos en este repositorio por razones de seguridad.
