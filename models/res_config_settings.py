# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dte_lines = fields.Integer(
            string="Cantidad de Líneas",
            default=24,
        )
    dte_lines_factor = fields.Float(
            string="Factor de Cálculo Líneas",
            default=50.0
        )
    dte_lines_action = fields.Selection(
            [
                ('create', 'Auto Crear otro documento'),
                ('stop', 'Detener Creación'),
            ],
            string="Acción a ejecutar",
            default="create"
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        dte_lines = int(ICPSudo.get_param(
                    'dte_lines.dte_lines', default=24))
        dte_lines_factor = float(ICPSudo.get_param(
                    'dte_lines.dte_lines_factor', default=50.0))
        dte_lines_action = ICPSudo.get_param(
                    'dte_lines.dte_lines_action', default='create')
        res.update(
                dte_lines=int(dte_lines),
                dte_lines_factor=dte_lines_factor,
                dte_lines_action=dte_lines_action
            )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('dte_lines.dte_lines',
                          self.dte_lines)
        ICPSudo.set_param('dte_lines.dte_lines_factor',
                          self.dte_lines_factor)
        ICPSudo.set_param('dte_lines.dte_lines_action',
                          self.dte_lines_action)
