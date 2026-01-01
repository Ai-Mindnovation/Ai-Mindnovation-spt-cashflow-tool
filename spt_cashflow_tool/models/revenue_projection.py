"""
Revenue Projection Model
Genera proyecciones de flujo de efectivo a N meses
"""
from odoo import models, fields, api
from datetime import datetime, timedelta


class RevenueProjection(models.Model):
    _name = 'revenue.projection'
    _description = 'Revenue Projection'
    _order = 'projection_date desc'

    # Campos básicos
    name = fields.Char('Nombre de Proyección', required=True, compute='_compute_name', store=True)
    projection_date = fields.Date('Fecha Base de Proyección', required=True, default=fields.Date.today)
    company_id = fields.Many2one('res.company', 'Empresa', required=True, default=lambda self: self.env.company)

    # Parámetros de proyección
    months_to_project = fields.Integer('Meses a Proyectar', required=True, default=6, help='De 1 a 12 meses')
    base_revenue = fields.Float('Revenue Base Mensual ($)', required=True, digits=(16, 2), help='Revenue mensual base para calcular proyecciones')
    base_expenses = fields.Float('Gastos Base Mensual ($)', required=True, digits=(16, 2), help='Gastos fijos mensuales')
    growth_rate = fields.Float('Tasa de Crecimiento (%)', default=0, digits=(5, 2), help='Crecimiento mensual en porcentaje')

    # Líneas de proyección (One2many)
    projection_line_ids = fields.One2many('revenue.projection.line', 'projection_id', 'Líneas de Proyección')

    # Campos de estado
    active = fields.Boolean('Activo', default=True)
    notes = fields.Text('Notas')

    @api.depends('projection_date')
    def _compute_name(self):
        """Genera nombre descriptivo"""
        for record in self:
            date_str = record.projection_date.strftime('%b %Y') if record.projection_date else 'N/A'
            record.name = f'Proyección {date_str}'

    @api.constrains('months_to_project')
    def _check_months_to_project(self):
        """Valida que months_to_project esté entre 1 y 12"""
        for record in self:
            if record.months_to_project < 1 or record.months_to_project > 12:
                raise models.ValidationError('Los meses a proyectar deben estar entre 1 y 12')

    def generate_projections(self):
        """
        Genera automáticamente las líneas de proyección basado en los parámetros.
        Limpia líneas existentes y genera nuevas.
        """
        for record in self:
            # Eliminar líneas existentes
            record.projection_line_ids.unlink()

            # Generar nuevas líneas
            current_date = record.projection_date
            
            for month_num in range(1, record.months_to_project + 1):
                # Calcular fecha del mes
                if month_num == 1:
                    month_date = record.projection_date
                else:
                    # Sumar meses a la fecha base
                    month_date = record.projection_date + timedelta(days=30 * (month_num - 1))
                
                # Calcular revenue con crecimiento
                if record.growth_rate > 0:
                    # Aplicar crecimiento compuesto: revenue * (1 + rate)^months
                    growth_factor = (1 + record.growth_rate / 100) ** (month_num - 1)
                    projected_revenue = record.base_revenue * growth_factor
                else:
                    projected_revenue = record.base_revenue

                # Los gastos se asumen fijos (sin variación)
                projected_expenses = record.base_expenses
                
                # Crear línea de proyección
                self.env['revenue.projection.line'].create({
                    'projection_id': record.id,
                    'month_number': month_num,
                    'month_name': month_date.strftime('%b %Y'),
                    'month_date': month_date,
                    'projected_revenue': projected_revenue,
                    'projected_expenses': projected_expenses,
                })

    def action_generate_projections(self):
        """Acción para botón en vista form"""
        self.generate_projections()
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    @api.model
    def get_projection_data(self):
        """
        Obtiene datos de la proyección más reciente
        Retorna: lista de líneas con datos formateados
        """
        projection = self.search([('company_id', '=', self.env.company.id)], limit=1, order='projection_date desc')
        
        if not projection:
            return []
        
        return [
            {
                'month': line.month_name,
                'revenue': line.projected_revenue,
                'expenses': line.projected_expenses,
                'net_flow': line.net_flow,
            }
            for line in projection.projection_line_ids
        ]

    @api.model
    def create_projection_from_analysis(self):
        """
        Crea una proyección automática basada en el análisis histórico
        - Usa el revenue promedio de los últimos 6 meses como base
        - Usa los gastos promedio como base_expenses
        - Genera 6 meses de proyección
        """
        # Obtener análisis históricos de los últimos 6 meses
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        today = fields.Date.today()
        six_months_ago = today - relativedelta(months=6)
        
        cashflow_analysis = self.env['cashflow.analysis']
        recent_analyses = cashflow_analysis.search([
            ('company_id', '=', self.env.company.id),
            ('date_from', '>=', six_months_ago),
        ])
        
        if not recent_analyses:
            # Sin datos históricos, usar valores por defecto
            base_revenue = 100000
            base_expenses = 50000
        else:
            # Calcular promedios
            total_revenue = sum(recent_analyses.mapped('revenue'))
            total_expenses = sum(recent_analyses.mapped('expenses'))
            count = len(recent_analyses)
            
            base_revenue = total_revenue / count
            base_expenses = total_expenses / count
        
        # Crear proyección
        projection = self.create({
            'name': f"Proyección Auto {today.strftime('%b %Y')}",
            'projection_date': today,
            'months_to_project': 6,
            'base_revenue': base_revenue,
            'base_expenses': base_expenses,
            'growth_rate': 0,  # Sin crecimiento inicial
            'company_id': self.env.company.id,
        })
        
        # Generar líneas automáticamente
        projection.generate_projections()
        
        return projection


class RevenueProjectionLine(models.Model):
    _name = 'revenue.projection.line'
    _description = 'Revenue Projection Line'
    _order = 'month_number asc'

    # Relación con proyección padre
    projection_id = fields.Many2one('revenue.projection', 'Proyección', required=True, ondelete='cascade')

    # Información del mes
    month_number = fields.Integer('Número de Mes', required=True)
    month_name = fields.Char('Nombre del Mes', required=True, help='Ej: ene 2026')
    month_date = fields.Date('Fecha del Mes', required=True)

    # Proyecciones financieras
    projected_revenue = fields.Float('Revenue Proyectado ($)', digits=(16, 2), required=True)
    projected_expenses = fields.Float('Gastos Proyectados ($)', digits=(16, 2), required=True)
    net_flow = fields.Float('Flujo Neto Proyectado ($)', compute='_compute_net_flow', store=True, digits=(16, 2))

    @api.depends('projected_revenue', 'projected_expenses')
    def _compute_net_flow(self):
        """Calcula el flujo neto: revenue - expenses"""
        for line in self:
            line.net_flow = line.projected_revenue - line.projected_expenses
