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

class ProductSolicitud(models.Model):
    _name = "product.solicitud"
    _description = "Solicitud de Pieza"
 
    name = fields.Char(string='Solicitud',default=lambda self: self.env['ir.sequence'].get('product.solicitud') or '/')
    
    nombre  = fields.Char('Nombre')
    
    apellidos  = fields.Char('Apellidos')
    
    direccion  = fields.Char('Direccion')
    
    ciudad  = fields.Char('Ciudad')
    
    provincia_id = fields.Many2one("res.country.state", string='Provincia')
    
    cp = fields.Char('CP')
    
    email = fields.Char('Email')
    
    telefono =  fields.Char('Telefono')
    
    marca_id = fields.Many2one("fleet.vehicle.model.brand", string='Marca')
    
    modelo = fields.Char(string='Modelo')
    
    motor = fields.Char(string='Motor')
    
    produce_date = fields.Char(string='Fecha de Fabricacion')
    
    pieza = fields.Char(string='Pieza')
    
    comentarios = fields.Text(string='Comentarios')