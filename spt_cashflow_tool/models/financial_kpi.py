"""
Financial KPI Model
Almacena y calcula los 4 KPIs principales del Cash Flow Tool
"""
from odoo import models, fields, api
from odoo.tools import float_compare


class FinancialKPI(models.Model):
    _name = 'financial.kpi'
    _description = 'Financial KPI'
    _order = 'date desc'

    # Campos básicos
    name = fields.Char('Descripción', required=True)
    date = fields.Date('Fecha del KPI', required=True, default=fields.Date.today)
    company_id = fields.Many2one('res.company', 'Empresa', required=True, default=lambda self: self.env.company)

    # KPI 1: Efectivo Disponible
    cash_available = fields.Float('Efectivo Disponible ($)', digits=(16, 2))
    cash_variation = fields.Float('Variación Efectivo (%)', digits=(5, 2), compute='_compute_variations', store=True)

    # KPI 2: Revenue Mensual
    monthly_revenue = fields.Float('Revenue Mensual ($)', digits=(16, 2))
    revenue_variation = fields.Float('Variación Revenue (%)', digits=(5, 2), compute='_compute_variations', store=True)

    # KPI 3: Burn Rate (Tasa de Quema)
    burn_rate = fields.Float('Burn Rate - Gastos Mensuales ($)', digits=(16, 2))
    burn_rate_variation = fields.Float('Variación Burn Rate (%)', digits=(5, 2), compute='_compute_variations', store=True)

    # KPI 4: Runway
    runway_months = fields.Float('Runway - Meses Disponibles', digits=(5, 2), compute='_compute_runway_months', store=True)

    # Campos adicionales
    notes = fields.Text('Notas')
    active = fields.Boolean('Activo', default=True)

    @api.depends('cash_available', 'burn_rate')
    def _compute_runway_months(self):
        """Calcula cuántos meses de operación quedan con el efectivo disponible"""
        for record in self:
            if record.burn_rate > 0:
                record.runway_months = record.cash_available / record.burn_rate
            else:
                record.runway_months = 0

    @api.depends('date', 'cash_available', 'monthly_revenue', 'burn_rate')
    def _compute_variations(self):
        """Calcula variaciones porcentuales vs mes anterior"""
        for record in self:
            # Buscar KPI del mes anterior
            previous_date = fields.Date.subtract(record.date, months=1)
            
            previous_kpi = self.search([
                ('date', '<=', previous_date),
                ('company_id', '=', record.company_id.id),
                ('id', '!=', record.id)
            ], limit=1, order='date desc')

            # Variación de Efectivo
            if previous_kpi and previous_kpi.cash_available > 0:
                record.cash_variation = (
                    (record.cash_available - previous_kpi.cash_available) / previous_kpi.cash_available * 100
                )
            else:
                record.cash_variation = 0

            # Variación de Revenue
            if previous_kpi and previous_kpi.monthly_revenue > 0:
                record.revenue_variation = (
                    (record.monthly_revenue - previous_kpi.monthly_revenue) / previous_kpi.monthly_revenue * 100
                )
            else:
                record.revenue_variation = 0

            # Variación de Burn Rate
            if previous_kpi and previous_kpi.burn_rate > 0:
                record.burn_rate_variation = (
                    (record.burn_rate - previous_kpi.burn_rate) / previous_kpi.burn_rate * 100
                )
            else:
                record.burn_rate_variation = 0

    @api.model
    def get_latest_kpis(self):
        """Obtiene los KPIs más recientes por empresa"""
        kpis = self.search([('company_id', '=', self.env.company.id)], limit=1, order='date desc')
        return kpis

    def get_kpi_dashboard_data(self):
        """Retorna datos formateados para el dashboard"""
        self.ensure_one()
        return {
            'cash_available': round(self.cash_available, 2),
            'cash_variation': round(self.cash_variation, 2),
            'monthly_revenue': round(self.monthly_revenue, 2),
            'revenue_variation': round(self.revenue_variation, 2),
            'burn_rate': round(self.burn_rate, 2),
            'burn_rate_variation': round(self.burn_rate_variation, 2),
            'runway_months': round(self.runway_months, 2),
            'date': self.date.strftime('%Y-%m-%d'),
        }

    @api.model
    def calculate_from_invoices(self):
        """
        Calcula los KPIs a partir de las facturas del mes actual
        - Revenue: suma de facturas validadas del mes
        - Cash Available: saldo de cuentas de banco
        - Burn Rate: suma de gastos (facturas de proveedores)
        Retorna: dict con KPIs calculados
        """
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        company = self.env.company
        today = fields.Date.today()
        
        # Período del mes actual
        first_day = today.replace(day=1)
        last_day = (first_day + relativedelta(months=1) - relativedelta(days=1)).date()
        
        # 1. REVENUE: Facturas de clientes validadas del mes
        sale_invoices = self.env['account.move'].search([
            ('company_id', '=', company.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', first_day),
            ('invoice_date', '<=', last_day),
        ])
        monthly_revenue = sum(sale_invoices.mapped('amount_total'))
        
        # 2. CASH AVAILABLE: Saldo de cuentas bancarias
        bank_accounts = self.env['account.account'].search([
            ('company_id', '=', company.id),
            ('account_type', '=', 'asset_cash'),
        ])
        
        cash_available = 0
        for account in bank_accounts:
            # Obtener saldo actual de la cuenta
            balance = account.current_balance
            cash_available += balance
        
        # 3. BURN RATE: Gastos mensuales (facturas de proveedores + gastos de empresa)
        purchase_invoices = self.env['account.move'].search([
            ('company_id', '=', company.id),
            ('move_type', '=', 'in_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', first_day),
            ('invoice_date', '<=', last_day),
        ])
        burn_rate = sum(purchase_invoices.mapped('amount_total'))
        
        # Agregar otros gastos operacionales si existen (facturas de gastos)
        expense_invoices = self.env['account.move'].search([
            ('company_id', '=', company.id),
            ('move_type', '=', 'in_expense'),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', first_day),
            ('invoice_date', '<=', last_day),
        ])
        burn_rate += sum(expense_invoices.mapped('amount_total'))
        
        return {
            'monthly_revenue': monthly_revenue,
            'cash_available': cash_available,
            'burn_rate': burn_rate,
            'calculation_date': today,
        }

    @api.model
    def create_daily_kpi(self):
        """
        Cron job: Calcula y crea un registro diario de KPIs
        Se ejecuta automáticamente cada día vía cron
        """
        company = self.env.company
        today = fields.Date.today()
        
        # Verificar si ya existe un KPI para hoy
        existing_kpi = self.search([
            ('company_id', '=', company.id),
            ('date', '=', today),
        ], limit=1)
        
        if existing_kpi:
            # Actualizar el existente
            kpi_data = self.calculate_from_invoices()
            existing_kpi.write({
                'monthly_revenue': kpi_data['monthly_revenue'],
                'cash_available': kpi_data['cash_available'],
                'burn_rate': kpi_data['burn_rate'],
            })
            return existing_kpi
        else:
            # Crear nuevo
            kpi_data = self.calculate_from_invoices()
            
            kpi = self.create({
                'name': f"KPI {today.strftime('%d/%m/%Y')}",
                'date': today,
                'monthly_revenue': kpi_data['monthly_revenue'],
                'cash_available': kpi_data['cash_available'],
                'burn_rate': kpi_data['burn_rate'],
                'company_id': company.id,
            })
            return kpi
