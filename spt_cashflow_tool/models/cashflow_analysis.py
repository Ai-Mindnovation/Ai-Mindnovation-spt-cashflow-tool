"""
Cashflow Analysis Model
Almacena datos históricos de ingresos y gastos por periodo
"""
from odoo import models, fields, api
from datetime import datetime


class CashflowAnalysis(models.Model):
    _name = 'cashflow.analysis'
    _description = 'Cashflow Analysis'
    _order = 'date_from desc'

    # Campos básicos
    name = fields.Char('Descripción del Periodo', required=True, compute='_compute_name', store=True)
    period = fields.Selection(
        [('monthly', 'Mensual'), ('quarterly', 'Trimestral'), ('annual', 'Anual')],
        'Periodo', required=True, default='monthly'
    )
    date_from = fields.Date('Fecha Inicio', required=True)
    date_to = fields.Date('Fecha Fin', required=True)
    company_id = fields.Many2one('res.company', 'Empresa', required=True, default=lambda self: self.env.company)

    # Campos financieros
    revenue = fields.Float('Ingresos ($)', digits=(16, 2), required=True)
    expenses = fields.Float('Gastos ($)', digits=(16, 2), required=True)
    net_cashflow = fields.Float('Flujo Neto ($)', digits=(16, 2), compute='_compute_net_cashflow', store=True)

    # Cliente asociado (opcional)
    client_id = fields.Many2one('res.partner', 'Cliente')

    # Notas y referencias
    notes = fields.Text('Notas')
    active = fields.Boolean('Activo', default=True)

    @api.depends('date_from', 'date_to', 'period')
    def _compute_name(self):
        """Genera nombre descriptivo del periodo"""
        for record in self:
            date_from_str = record.date_from.strftime('%b %Y') if record.date_from else 'N/A'
            date_to_str = record.date_to.strftime('%b %Y') if record.date_to else 'N/A'
            
            period_label = dict(record._fields['period'].selection).get(record.period, '')
            record.name = f'{period_label}: {date_from_str} - {date_to_str}'

    @api.depends('revenue', 'expenses')
    def _compute_net_cashflow(self):
        """Calcula el flujo neto: ingresos - gastos"""
        for record in self:
            record.net_cashflow = record.revenue - record.expenses

    @api.model
    def get_revenue_trend(self, months=12):
        """
        Obtiene datos de tendencia de revenue de los últimos N meses
        Retorna: lista de dicts con mes y revenue
        """
        analyses = self.search(
            [('company_id', '=', self.env.company.id)],
            limit=months,
            order='date_from desc'
        )
        analyses = analyses.sorted(key=lambda x: x.date_from)  # Orden ascendente
        
        trend_data = []
        for analysis in analyses:
            trend_data.append({
                'date': analysis.date_from.strftime('%b %Y'),
                'revenue': analysis.revenue,
                'month_key': analysis.date_from.strftime('%Y-%m'),
            })
        return trend_data

    @api.model
    def get_top_clients(self, limit=5):
        """
        Obtiene los top N clientes por total de ingresos
        Retorna: lista de dicts con cliente y revenue total
        """
        from odoo.tools import groupby
        
        analyses = self.search([('company_id', '=', self.env.company.id)])
        
        # Agrupar por cliente y sumar revenue
        client_revenues = {}
        for analysis in analyses:
            client_name = analysis.client_id.name if analysis.client_id else 'Sin Cliente'
            if client_name not in client_revenues:
                client_revenues[client_name] = 0
            client_revenues[client_name] += analysis.revenue
        
        # Ordenar y limitar
        sorted_clients = sorted(
            client_revenues.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        top_data = [{'client': name, 'revenue': amount} for name, amount in sorted_clients]
        return top_data

    @api.model
    def get_revenue_statistics(self):
        """
        Calcula estadísticas de revenue: promedio, mínimo, máximo
        Retorna: dict con estadísticas
        """
        analyses = self.search([('company_id', '=', self.env.company.id)])
        
        if not analyses:
            return {
                'average_revenue': 0,
                'min_revenue': 0,
                'max_revenue': 0,
                'total_periods': 0,
            }
        
        revenues = [a.revenue for a in analyses]
        
        return {
            'average_revenue': sum(revenues) / len(revenues) if revenues else 0,
            'min_revenue': min(revenues) if revenues else 0,
            'max_revenue': max(revenues) if revenues else 0,
            'total_periods': len(revenues),
        }
