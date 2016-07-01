# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import itertools
from lxml import etree

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp

class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"
    
    @api.one
    def _piezas_count(self):
        self.piezas_count = len(self.env['product.product'].search([('vehiculo_id', '=',self.id)]))

    piezas_count = fields.Integer(string='# Piezas', type='integer', compute='_piezas_count')
    
    vehiculo_id = fields.Many2one('fleet.vehicle', string='Vehiculo',
        readonly=False, copy=False,
        help="Vehiculo al que pertence.")
                   
    @api.multi
    def view_piezas(self):
        mod_obj = self.env['ir.model.data']
        dummy, action_id = tuple(mod_obj.get_object_reference('product', 'product_normal_action'))
        action = self.pool.get('ir.actions.act_window').read(self._cr, self._uid, action_id, context=self._context)

        p_ids = []
        for vh in self:
            for p in self.env['product.product'].search([('vehiculo_id', '=',self.id)]):
                    p_ids += [p.id]
        action['domain'] = "[('id','in',[" + ','.join(map(str, p_ids)) + "])]"

        return action
    
    
    

