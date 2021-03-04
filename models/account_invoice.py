# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
import math
import logging
_logger = logging.getLogger(__name__)


class DTELines(models.Model):
    _inherit = 'account.invoice'

    def _line_size(self, texto):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        factor = float(ICPSudo.get_param(
                    'dte_lines.dte_lines_factor', default=50.0))
        lines = texto.split('\n')
        size = len(lines)
        for l in lines:
            l_size = math.ceil((len(l) / factor))
            size += (l_size - 1)
        return size

    def _lines_total(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        dte_lines = int(ICPSudo.get_param(
                    'dte_lines.dte_lines', default=24))
        total_lines = 0
        for l in self.invoice_line_ids:
            total_lines += 1
        if self.referencias:
            dte_lines -= (len(self.references) - 2)
        return total_lines, dte_lines

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        dte_action = ICPSudo.get_param(
                                'dte_lines.dte_lines_action', default='create')
        dte_lines, total_lines = self._lines_total()
        if not self.ticket and total_lines > dte_lines and dte_action == 'stop':
            raise UserError("Se está creando una cantidad de líneas de detalle mayor a la permitida")
        return super(DTELines, self)._onchange_invoice_line_ids()

    def action_invoice_open(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        dte_action = ICPSudo.get_param(
                                'dte_lines.dte_lines_action')
        for r in self:
            # if not r.ticket:
            #     continue
            total_lines, dte_lines = r._lines_total()
            if not r.ticket and total_lines > dte_lines:
                dte_action = ICPSudo.get_param(
                                'dte_lines.dte_lines_action')
                if dte_action == 'create':
                    new = r.copy()
                    for il in r.invoice_line_ids:
                        if il.sequence > dte_lines:
                            il.unlink()
                            continue
                    for nil in new.invoice_line_ids:
                        if nil.sequence < dte_lines:
                            nil.unlink()
                            continue
                        nil.sequence -= dte_lines + 1
                    new._onchange_partner_id()
                    new._onchange_invoice_line_ids()
                    r._onchange_partner_id()
                    r._onchange_invoice_line_ids()
                    self += new
                elif dte_action == 'stop':
                    raise UserError("Se está creando una cantidad de líneas mayor a la permitida")
        return super(DTELines, self).action_invoice_open()

