"""
Report para Reporte de Cash Flow
"""
from odoo import models, fields, api


class CashflowReportView(models.Model):
    _name = 'cashflow.report'
    _description = 'Cash Flow Report'

    name = fields.Char('Nombre del Reporte')
    report_date = fields.Date('Fecha del Reporte', default=fields.Date.today)
    company_id = fields.Many2one('res.company', 'Empresa', required=True, default=lambda self: self.env.company)
    
    # Datos agregados
    kpi_data = fields.Json('Datos KPI')
    analysis_data = fields.Json('Datos Análisis Histórico')
    projection_data = fields.Json('Datos Proyecciones')

    @api.model
    def generate_cashflow_report(self, company_id=None):
        """
        Genera datos para el reporte PDF
        Retorna: dict con todos los datos necesarios
        """
        if not company_id:
            company_id = self.env.company
        
        # 1. Obtener KPIs más recientes
        kpi = self.env['financial.kpi'].search([
            ('company_id', '=', company_id.id)
        ], limit=1, order='date desc')
        
        kpi_data = {}
        if kpi:
            kpi_data = kpi.get_kpi_dashboard_data()
        
        # 2. Obtener estadísticas de análisis histórico
        cashflow_analysis = self.env['cashflow.analysis']
        stats = cashflow_analysis.get_revenue_statistics()
        
        # Top 5 clientes
        top_clients = cashflow_analysis.get_top_clients(limit=5)
        
        # Tendencia de revenue
        revenue_trend = cashflow_analysis.get_revenue_trend(months=12)
        
        analysis_data = {
            'statistics': stats,
            'top_clients': top_clients,
            'revenue_trend': revenue_trend,
        }
        
        # 3. Obtener proyecciones más recientes
        projection = self.env['revenue.projection'].search([
            ('company_id', '=', company_id.id)
        ], limit=1, order='projection_date desc')
        
        projection_data = {}
        if projection:
            projection_data = {
                'name': projection.name,
                'projection_date': projection.projection_date.strftime('%Y-%m-%d'),
                'months': projection.months_to_project,
                'growth_rate': projection.growth_rate,
                'lines': [
                    {
                        'month': line.month_name,
                        'revenue': round(line.projected_revenue, 2),
                        'expenses': round(line.projected_expenses, 2),
                        'net_flow': round(line.net_flow, 2),
                    }
                    for line in projection.projection_line_ids
                ]
            }
        
        return {
            'kpi': kpi_data,
            'analysis': analysis_data,
            'projection': projection_data,
            'company': company_id.name,
            'report_date': fields.Date.today().strftime('%Y-%m-%d'),
        }
