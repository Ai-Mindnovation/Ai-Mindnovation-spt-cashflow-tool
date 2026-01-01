/* SPT Cash Flow Tool - Dashboard JavaScript */

odoo.define('spt_cashflow_tool.dashboard', function(require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');
    var _t = core._t;

    /**
     * Dashboard Widget para SPT Cash Flow Tool
     * Maneja gráficos e interactividad del dashboard
     */
    var CashflowDashboard = Widget.extend({
        template: 'CashflowDashboard',

        init: function(parent, action) {
            this._super.apply(this, arguments);
            this.data = action.context || {};
        },

        willStart: function() {
            return $.when(this._super.apply(this, arguments));
        },

        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                // Inicializar gráficos
                self._initializeCharts();
                // Inicializar tooltips
                self._initializeTooltips();
                // Aplicar efectos visuales
                self._applyAnimations();
            });
        },

        /**
         * Inicializa gráficos usando Chart.js (si está disponible)
         */
        _initializeCharts: function() {
            // Los gráficos de Odoo usan PlotlyJS por defecto
            // Este método es para enhancements futuros con Chart.js
            console.log('SPT Cash Flow: Dashboard charts initialized');
        },

        /**
         * Inicializa tooltips interactivos
         */
        _initializeTooltips: function() {
            var self = this;
            
            // Tooltip para KPI Cards
            $('.o_kpi_card').each(function() {
                var card = $(this);
                var label = card.find('.o_kpi_label').text();
                var value = card.find('.o_kpi_value').text();
                
                // Agregar atributo title para tooltip nativo
                card.attr('title', label + ': ' + value);
            });

            // Tooltip para variaciones
            $('.o_kpi_variation').each(function() {
                var variation = $(this).text();
                var card = $(this).closest('.o_kpi_card');
                var label = card.find('.o_kpi_label').text();
                
                if (variation.includes('%')) {
                    if (parseFloat(variation) >= 0) {
                        $(this).attr('title', label + ' aumentó');
                    } else {
                        $(this).attr('title', label + ' disminuyó');
                    }
                }
            });

            console.log('SPT Cash Flow: Tooltips initialized');
        },

        /**
         * Aplica animaciones a elementos
         */
        _applyAnimations: function() {
            // Animar KPI cards al scroll
            this._observeElementsInViewport();
            
            // Ripple effect en clics
            this._addRippleEffect();
            
            console.log('SPT Cash Flow: Animations applied');
        },

        /**
         * Observa elementos que entran en viewport y los anima
         */
        _observeElementsInViewport: function() {
            if (!window.IntersectionObserver) {
                return; // Fallback para navegadores viejos
            }

            var observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        $(entry.target).addClass('o_animated');
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1
            });

            $('.o_kpi_card').each(function() {
                observer.observe(this);
            });
        },

        /**
         * Agrega efecto ripple al hacer click
         */
        _addRippleEffect: function() {
            $(document).on('click', '.o_kpi_card', function(e) {
                var ripple = $('<span class="o_ripple"></span>');
                var rect = this.getBoundingClientRect();
                var size = Math.max(rect.width, rect.height);
                var x = e.clientX - rect.left - size / 2;
                var y = e.clientY - rect.top - size / 2;

                ripple.css({
                    width: size,
                    height: size,
                    left: x,
                    top: y
                });

                $(this).append(ripple);

                setTimeout(function() {
                    ripple.remove();
                }, 600);
            });
        },

        /**
         * Exportar datos del dashboard
         */
        exportDashboardData: function(format) {
            format = format || 'json';
            
            var data = {
                timestamp: new Date().toISOString(),
                kpis: this._extractKPIData(),
                format: format
            };

            if (format === 'json') {
                this._exportAsJSON(data);
            } else if (format === 'csv') {
                this._exportAsCSV(data);
            }
        },

        /**
         * Extrae datos de KPIs
         */
        _extractKPIData: function() {
            var kpis = [];
            
            $('.o_kpi_card').each(function() {
                var card = $(this);
                kpis.push({
                    label: card.find('.o_kpi_label').text(),
                    value: card.find('.o_kpi_value').text(),
                    variation: card.find('.o_kpi_variation').text()
                });
            });

            return kpis;
        },

        /**
         * Exporta datos como JSON
         */
        _exportAsJSON: function(data) {
            var jsonData = JSON.stringify(data, null, 2);
            var blob = new Blob([jsonData], {type: 'application/json'});
            this._downloadFile(blob, 'cashflow-dashboard-' + Date.now() + '.json');
        },

        /**
         * Exporta datos como CSV
         */
        _exportAsCSV: function(data) {
            var csv = 'KPI,Valor,Variación\n';
            
            data.kpis.forEach(function(kpi) {
                csv += '"' + kpi.label + '","' + kpi.value + '","' + kpi.variation + '"\n';
            });

            var blob = new Blob([csv], {type: 'text/csv'});
            this._downloadFile(blob, 'cashflow-dashboard-' + Date.now() + '.csv');
        },

        /**
         * Descarga un archivo
         */
        _downloadFile: function(blob, filename) {
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        },

        /**
         * Imprime el dashboard
         */
        printDashboard: function() {
            window.print();
        }
    });

    return {
        CashflowDashboard: CashflowDashboard
    };
});

/**
 * jQuery Extension: Plugin para formatear números como moneda
 */
jQuery.fn.formatCurrency = function(symbol, decimals) {
    symbol = symbol || '$';
    decimals = decimals !== undefined ? decimals : 2;

    return this.each(function() {
        var value = parseFloat($(this).text());
        if (!isNaN(value)) {
            var formatted = symbol + value.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
            $(this).text(formatted);
        }
    });
};

/**
 * Inicialización al cargar la página
 */
$(document).ready(function() {
    // Formatear valores monetarios
    $('.o_kpi_value').formatCurrency('$', 2);

    // Log de inicialización
    console.log('SPT Cash Flow Tool: Dashboard loaded successfully');

    // Event listeners para acciones
    $(document).on('click', '.o_btn_export_json', function(e) {
        e.preventDefault();
        console.log('SPT Cash Flow: Exporting as JSON');
    });

    $(document).on('click', '.o_btn_export_csv', function(e) {
        e.preventDefault();
        console.log('SPT Cash Flow: Exporting as CSV');
    });

    $(document).on('click', '.o_btn_print', function(e) {
        e.preventDefault();
        window.print();
    });
});
