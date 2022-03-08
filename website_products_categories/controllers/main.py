# -*- coding: utf-8 -*-
# Copyright (c) 2022-SINAPSYS MASTERCORE

import json

from odoo import http
from odoo.http import request
from odoo.addons.theme_prime.controllers.main import ThemePrimeWebsiteSale
from odoo.addons.website.controllers.main import QueryURL
from odoo.osv import expression
import logging

_logger = logging.getLogger(__name__)
class ThemePrimeWebsiteSaleInherit(ThemePrimeWebsiteSale):
    
    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
        domains = [request.website.sale_product_domain()]
        if search:
            for srch in search.split(" "):
                subdomains = [
                    [('name', 'ilike', srch)],
                    [('product_variant_ids.default_code', 'ilike', srch)]
                ]
                if search_in_description:
                    subdomains.append([('description', 'ilike', srch)])
                    subdomains.append([('description_sale', 'ilike', srch)])
                domains.append(expression.OR(subdomains))

        if category:
            domains.append([('public_categ_ids', 'child_of', int(category))])

        if attrib_values:
            attrib = None
            ids = []
            brand_ids = []
            for value in attrib_values:
                if value[0] == 0:
                    brand_ids.append(value[1])
                else:
                    if not attrib:
                        attrib = value[0]
                        ids.append(value[1])
                    elif value[0] == attrib:
                        ids.append(value[1])
                    else:
                        domains.append([('attribute_line_ids.value_ids', 'in', ids)])
                        attrib = value[0]
                        ids = [value[1]]
            if attrib:
                domains.append([('attribute_line_ids.value_ids', 'in', ids)])
            if brand_ids:
                domains.append([('dr_brand_id', 'in', brand_ids)])

        min_price = request.httprequest.args.get('min_price')
        max_price = request.httprequest.args.get('max_price')
        if min_price:
            min_price = self._check_float(min_price)
            if min_price:
                domains.append([('list_price', '>=', min_price)])
        if max_price:
            max_price = self._check_float(max_price)
            if max_price:
                domains.append([('list_price', '<=', max_price)])
        
        vehicle_type = request.httprequest.args.get('vehicle_type')
        if vehicle_type and vehicle_type != 'Todos':
            domains.append([('vehicle_type','=', vehicle_type)])

        # model_id = request.httprequest.args.get('model')
        # if model_id and vehicle_type != 'Todos':
        #     domains.append([('fleet_models_ids', 'child_of', model_id)])
            
        return expression.AND(domains)
        
    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response = super(ThemePrimeWebsiteSaleInherit, self).shop(page, category, search, ppg, **post)
        theme = request.website.sudo().theme_id
        vehicles_types = [(False, 'Todos'),('liviano', 'Vehículo Liviano'),('pesado', 'Vehículo Pesado')]
        vehicle_models = request.env['fleet.vehicle.model'].sudo().search([], order="name")
        # Get the Years from fleet.vehicles, avoid saving duplicates in list and sort this list
        record_fleet = request.env['fleet.vehicle.model'].sudo().search(['&',('year_start','!=',False),('year_start','!=',False)])
        years_start = []
        years_end = []
        for record in record_fleet:
            if record.year_start not in years_start:
                years_start.append(record.year_start)
            if record.year_end not in years_end:
                years_end.append(record.year_end)
        years_start.sort()
        years_end.sort()
        
        if theme and theme.name.startswith('theme_prime'):
            prices = request.env['product.template'].read_group([], ['max_price:max(list_price)', 'min_price:min(list_price)'], [])[0]
            min_price = float(prices['min_price'] or 0)
            max_price = float(prices['max_price'] or 0)
            min_age = request.httprequest.args.get('min_age'),
            max_age = request.httprequest.args.get('max_age'),
            model = request.httprequest.args.get('model')
            keep = QueryURL(
                '/shop',
                category=category and int(category),
                search=search,
                attrib=request.httprequest.args.getlist('attrib'),
                ppg=ppg,
                order=post.get('order'),
                min_price=request.httprequest.args.get('min_price'),
                max_price=request.httprequest.args.get('max_price'),
                vehicle_type=request.httprequest.args.get('vehicle_type')
            )
            response.qcontext.update(keep=keep, min_price=min_price, max_price=max_price, vehicles_types=vehicles_types, vehicle_models=vehicle_models, years_start=years_start, years_end=years_end)

            # Grid Sizing
            bins = []
            for product in response.qcontext.get('products'):
                bins.append([{
                    'class': " ".join(x.html_class for x in product.website_style_ids if x.html_class),
                    'product': product,
                    'x': 1,
                    'y': 1
                }])
            response.qcontext.update(bins=bins)

            attrib_list = request.httprequest.args.getlist('attrib')
            attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
            attributes_ids = [v[0] for v in attrib_values]

            response.qcontext.update(attributes_ids=attributes_ids)

        return response