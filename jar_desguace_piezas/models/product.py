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

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    vehiculo_motor = fields.Char(related='vehiculo_id.motor',
        string='Motor')
    
    vehiculo_cilindrada = fields.Integer(related='vehiculo_id.cilindrada',
        string='Cilindrada')
    
    vehiculo_caballos = fields.Integer(related='vehiculo_id.horsepower',
        string='Caballos')
    
    vehiculo_modelo = fields.Many2one(related='vehiculo_id.model_id',
        string='Modelo')
    
    vehiculo_marca= fields.Many2one(related='vehiculo_modelo.brand_id',
        string='Marca')
    
    vehiculo_produce= fields.Date(related='vehiculo_id.produce_date',
        string='Fecha de Fabricacion')
    
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    vehiculo_motor = fields.Char(related='product_variant_ids.vehiculo_motor',
        string='Motor')
    
    vehiculo_cilindrada = fields.Integer(related='product_variant_ids.vehiculo_cilindrada',
        string='Cilindrada')
    
    vehiculo_caballos = fields.Integer(related='product_variant_ids.vehiculo_caballos',
        string='Caballos')
    
    vehiculo_modelo = fields.Many2one(related='product_variant_ids.vehiculo_modelo',
        string='Modelo')
    
    vehiculo_marca= fields.Many2one(related='product_variant_ids.vehiculo_marca',
        string='Marca')
    
    vehiculo_produce= fields.Date(related='product_variant_ids.vehiculo_produce',
        string='Fecha de Fabricacion')
