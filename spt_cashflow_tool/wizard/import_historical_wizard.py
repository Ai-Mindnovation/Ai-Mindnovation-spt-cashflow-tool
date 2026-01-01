"""
Wizard para importar datos históricos de facturas
"""
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ImportHistoricalDataWizard(models.TransientModel):
    _name = 'import.historical.data.wizard'
    _description = 'Importar Datos Históricos de Cash Flow'

    date_from = fields.Date('Fecha Inicio', required=True, help='Fecha inicial del período a analizar')
    date_to = fields.Date('Fecha Fin', required=True, help='Fecha final del período a analizar')
    period_type = fields.Selection(
        [('monthly', 'Mensual'), ('quarterly', 'Trimestral')],
        'Tipo de Período', required=True, default='monthly'
    )
    company_id = fields.Many2one('res.company', 'Empresa', required=True, default=lambda self: self.env.company)

    def action_import_historical_data(self):
        """
        Ejecuta el análisis histórico basado en facturas
        """
        self.ensure_one()
        
        # Delegar al modelo de análisis
        cashflow_analysis = self.env['cashflow.analysis']
        cashflow_analysis.import_historical_data(
            date_from=self.date_from,
            date_to=self.date_to,
            period_type=self.period_type,
            company_id=self.company_id
        )
        
        # Retornar action a la vista de análisis
        return {
            'name': 'Análisis de Cash Flow',
            'type': 'ir.actions.act_window',
            'res_model': 'cashflow.analysis',
            'view_mode': 'tree,form',
            'domain': [
                ('company_id', '=', self.company_id.id),
                ('date_from', '>=', self.date_from),
                ('date_to', '<=', self.date_to),
            ],
            'target': 'main',
        }
