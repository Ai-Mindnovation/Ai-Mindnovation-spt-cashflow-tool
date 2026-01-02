{
    'name': 'SPT Cash Flow Tool',
    'version': '16.0.1.0.0',
    'category': 'Accounting/Finance',
    'author': 'AI-MindNovation',
    'website': 'https://www.ai-mindnovation.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'views/cashflow_dashboard.xml',
        'views/cashflow_analysis_views.xml',
        'views/revenue_projection_views.xml',
        'views/menu.xml',
        'wizard/import_historical_wizard.xml',
        'wizard/generate_projection_wizard.xml',
        'reports/cashflow_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'spt_cashflow_tool/static/src/css/dashboard.css',
            'spt_cashflow_tool/static/src/js/dashboard.js',
        ],
    },
    'images': [
        'static/description/icon.png',
    ],
    'web_icon': 'spt_cashflow_tool,static/description/icon.png',
    'installable': True,
    'auto_install': False,
    'application': True,
    'description': """
        Dashboard interactivo de análisis de flujo de efectivo para SPT Colombia.
        
        Funcionalidades:
        - Resumen Ejecutivo con KPIs principales
        - Análisis Histórico de ingresos y clientes
        - Proyecciones de flujo de efectivo
        - Reportes detallados en PDF
    """,
}
