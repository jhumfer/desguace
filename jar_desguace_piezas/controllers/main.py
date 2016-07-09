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


# -*- coding: utf-8 -*-
import base64

import werkzeug
import werkzeug.urls

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _


class solicitud_pieza(http.Controller):
    
    def generate_google_map_url(self, street, city, city_zip, country_name):
        url = "http://maps.googleapis.com/maps/api/staticmap?center=%s&sensor=false&zoom=8&size=298x298" % werkzeug.url_quote_plus(
            '%s, %s %s, %s' % (street, city, city_zip, country_name)
        )
        return url



    @http.route(['/page/website.solicitud_pieza'], type='http', auth="public", website=True)
    def solicitud(self, **kwargs):
        values = {}
        for field in ['nombre','apellidos','email','telefono','direccion','ciudad','provincia_id','cp',
                      'marca_id','modelo','motor','produce_date','pieza',
                      'comentarios','file']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        marca = request.registry['fleet.vehicle.model.brand']
        marca_ids = marca.search(request.cr, SUPERUSER_ID, [], context=request.context)
        marcas = marca.browse(request.cr, SUPERUSER_ID, marca_ids, context=request.context)
        provincia = request.registry['res.country.state']
        provincia_ids = provincia.search(request.cr, SUPERUSER_ID, [], context=request.context)
        provincias = provincia.browse(request.cr, SUPERUSER_ID, provincia_ids, context=request.context)
        values.update(kwargs=kwargs.items())
        values.update({
            'marca_id': marcas,
            'provincia_id': provincias,
        })
        
        return request.website.render("website.solicitud_pieza", values)
    
    @http.route(['/desguace/solicitud_pieza'], type='http', auth="public", website=True)
    def solicitud_pieza(self, **kwargs):
        def dict_to_str(title, dictvar):
            ret = "\n\n%s" % title
            for field in dictvar:
                ret += "\n%s" % field
            return ret

        _TECHNICAL = ['show_info', 'view_from', 'view_callback']  # Only use for behavior, don't stock it
        _BLACKLIST = ['id', 'create_uid', 'create_date', 'write_uid', 'write_date', 'user_id', 'active']  # Allow in description
        _REQUIRED = ['email']  # Could be improved including required from model
        _TEAMVIEWER = ['file']

        post_file = []  # List of file to add to ir_attachment once we have the ID
        post_description = []  # Info to add after the message
        values = {}

        values['medium_id'] = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'helpdesk_medium_website')
        values['section_id'] = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'website.salesteam_website_sales')

        for field_name, field_value in kwargs.items():
            if hasattr(field_value, 'filename'):
                post_file.append(field_value)
            elif field_name in request.registry['product.solicitud']._fields and field_name not in _BLACKLIST:
                values[field_name] = field_value
            elif field_name in _TEAMVIEWER:
                values[field_name] = field_value
            elif field_name not in _TECHNICAL:  # allow to add some free fields or blacklisted field like ID
                post_description.append("%s: %s" % (field_name, field_value))

        # fields validation : Check that required field from model crm_lead exists
        error = set(field for field in _REQUIRED if not values.get(field))

        if error:
            values = dict(values, error=error, kwargs=kwargs.items())
            return request.website.render(kwargs.get("view_from", "website.solicitud_pieza"), values)

        # description is required, so it is always already initialized
        if post_description:
            values['subject'] += dict_to_str(_("Custom Fields: "), post_description)

        if kwargs.get("show_info"):
            post_description = []
            environ = request.httprequest.headers.environ
            post_description.append("%s: %s" % ("IP", environ.get("REMOTE_ADDR")))
            post_description.append("%s: %s" % ("USER_AGENT", environ.get("HTTP_USER_AGENT")))
            post_description.append("%s: %s" % ("ACCEPT_LANGUAGE", environ.get("HTTP_ACCEPT_LANGUAGE")))
            post_description.append("%s: %s" % ("REFERER", environ.get("HTTP_REFERER")))
            values['subject'] += dict_to_str(_("Environ Fields: "), post_description)
        #partner = request.registry['res.partner']
        #partner_ids = partner.search(request.cr, SUPERUSER_ID, [('email','=',values['client_email'])], context=request.context)
#         if partner_ids:
        solicitud_id = self.create_solicitud(request, dict(values, user_id=False), kwargs)
        values.update(solicitud_id=solicitud_id)
        
        if kwargs.get('attachment',False):
            Attachments = request.registry['ir.attachment']
            name = kwargs.get('attachment').filename      
            file = kwargs.get('attachment')
            attachment_id = Attachments.create(request.cr, request.uid, {
                'name':name,
                'res_name': name,
                'type': 'binary',
                'res_model': 'product.solicitud',
                'res_id': solicitud_id,
                'datas': base64.encodestring(file.read()),
            }, request.context)
             
    
        return self.get_solicitud_response(values, kwargs)
    
    def preRenderThanks(self, values, kwargs):
        """ Allow to be overrided """
        # company = request.website.company_id
        user_obj = request.registry['res.users']
        #user_id = user_obj.search(request.cr, SUPERUSER_ID, [('partner_id.email','=',values['client_email'])], context=request.context)
        user = user_obj.browse(request.cr, SUPERUSER_ID,[SUPERUSER_ID])
        company = user.company_id
        return {
            'google_map_url': self.generate_google_map_url(company.street, company.city, company.zip, company.country_id and company.country_id.name_get()[0][1] or ''),
            '_values': values,
            '_kwargs': kwargs,
        }
    
    def get_solicitud_response(self, values, kwargs):
        
        values = self.preRenderThanks(values, kwargs)
        return request.website.render(kwargs.get("view_callback", "website.solicitud_thanks"), values)
    
#     def get_helpdesk_response_no_client(self, values, kwargs):
#         
#         values = self.preRenderThanks(values, kwargs)
#         return request.website.render(kwargs.get("view_callback", "website.helpdesk_no_client"), values)
    
    def create_solicitud(self, request, values, kwargs):
        """ Allow to be overrided """
        cr, context = request.cr, request.context

        return request.registry['product.solicitud'].create(cr, SUPERUSER_ID, values, context=dict(context))
