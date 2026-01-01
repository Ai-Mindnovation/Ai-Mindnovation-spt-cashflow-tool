"""
Wizard para generar proyecciones automáticas
"""
from odoo import models, fields, api


class GenerateProjectionWizard(models.TransientModel):
    _name = 'generate.projection.wizard'
    _description = 'Generar Proyección Automática'

    name = fields.Char('Nombre de Proyección', required=True)
    projection_date = fields.Date('Fecha Base', required=True, default=fields.Date.today)
    months_to_project = fields.Integer('Meses a Proyectar', required=True, default=6, help='De 1 a 12 meses')
    base_revenue = fields.Float('Revenue Base Mensual ($)', required=True, help='Dejar en 0 para calcular automáticamente')
    base_expenses = fields.Float('Gastos Base Mensual ($)', required=True, help='Dejar en 0 para calcular automáticamente')
    growth_rate = fields.Float('Tasa de Crecimiento (%)', default=0, help='Crecimiento mensual esperado')
    auto_calculate = fields.Boolean('Calcular automáticamente desde análisis histórico', default=True)
    company_id = fields.Many2one('res.company', 'Empresa', required=True, default=lambda self: self.env.company)

    @api.onchange('auto_calculate')
    def _onchange_auto_calculate(self):
        """Si se selecciona auto_calculate, obtiene valores del histórico"""
        if self.auto_calculate:
            from dateutil.relativedelta import relativedelta
            
            # Obtener análisis de últimos 6 meses
            six_months_ago = fields.Date.today() - relativedelta(months=6)
            cashflow_analysis = self.env['cashflow.analysis']
            recent = cashflow_analysis.search([
                ('company_id', '=', self.company_id.id),
                ('date_from', '>=', six_months_ago),
            ])
            
            if recent:
                avg_revenue = sum(recent.mapped('revenue')) / len(recent)
                avg_expenses = sum(recent.mapped('expenses')) / len(recent)
                self.base_revenue = avg_revenue
                self.base_expenses = avg_expenses

    def action_generate_projection(self):
        """Crea la proyección con los parámetros especificados"""
        self.ensure_one()
        
        # Crear proyección
        projection = self.env['revenue.projection'].create({
            'name': self.name,
            'projection_date': self.projection_date,
            'months_to_project': self.months_to_project,
            'base_revenue': self.base_revenue,
            'base_expenses': self.base_expenses,
            'growth_rate': self.growth_rate,
            'company_id': self.company_id.id,
        })
        
        # Generar líneas automáticamente
        projection.generate_projections()
        
        # Retornar vista de la proyección creada
        return {
            'name': 'Proyección Creada',
            'type': 'ir.actions.act_window',
            'res_model': 'revenue.projection',
            'res_id': projection.id,
            'view_mode': 'form',
            'target': 'main',
        }
