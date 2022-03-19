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
        if vehicle_type and vehicle_type != 'All':
            domains.append([('vehicle_type','=', vehicle_type)])

        model_id = request.httprequest.args.get('model')
        if model_id and model_id != 'All':
            domains.append([('fleet_model_ids.fleet_model_id', 'in', [int(model_id)])])

        brand_id = request.httprequest.args.get('brand_vehicle')
        if brand_id and brand_id != 'All':
            domains.append([('fleet_model_ids.fleet_model_id.brand_id', 'in', [int(brand_id)])])

        year = request.httprequest.args.get('year')
        if year and year != 'All':
            domains.append(['&',('fleet_model_ids.fleet_model_id.year_end', '>=', int(year)),('fleet_model_ids.fleet_model_id.year_start', '<=', int(year))])

        """ brand_id = request.httprequest.args.get('brand_id')
        if brand_id:
            domains.append([('fleet_model_ids.fleet_model_id.brand_id', 'in', [int(brand_id)])]) """
        
        return expression.AND(domains)
        
    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response = super(ThemePrimeWebsiteSaleInherit, self).shop(page, category, search, ppg, **post)
        theme = request.website.sudo().theme_id
        # Tipos de vehiculos
        vehicles_types = [('liviano', 'Vehículo Liviano'),('pesado', 'Vehículo Pesado')]
        # Marca de vehículos
        vehicle_type_selected = request.httprequest.args.get('vehicle_type')
        if vehicle_type_selected and vehicle_type_selected != 'All':
            brands_vehicle = request.env['fleet.vehicle.model.brand'].sudo().search([('vehicle_type', '=', vehicle_type_selected)])
        else:
            brands_vehicle = request.env['fleet.vehicle.model.brand'].sudo().search([])
        # Modelos de vehiculos
        brand_type_selected = request.httprequest.args.get('brand_vehicle')
        if brand_type_selected and brand_type_selected != 'All':
            vehicle_models = request.env['fleet.vehicle.model'].sudo().search([('brand_id', 'in', [int(brand_type_selected)])], order="name")
        else:
            vehicle_models = request.env['fleet.vehicle.model'].sudo().search([], order="name")
        
        # Años
        vehicle_models_selected = request.httprequest.args.get('model')
        if vehicle_models_selected and vehicle_models_selected != 'All':
            model_selected = request.env['fleet.vehicle.model'].sudo().search([('id', '=', vehicle_models_selected)])
            years = list(range(int(model_selected.year_start),int(model_selected.year_end)-1, -1))
        else:
            years = list(range(2022,1970,-1))
        
        Category = request.env['product.public.category']
        website_domain = request.website.website_domain()
        if vehicle_type_selected and vehicle_type_selected != 'All':
            categs_domain = [('parent_id', '=', False)] + [('vehicle_type', '=', vehicle_type_selected)] + website_domain
        else:
            categs_domain = [('parent_id', '=', False)] + website_domain

        if search:
            search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

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
            response.qcontext.update(keep=keep, min_price=min_price, max_price=max_price, vehicles_types=vehicles_types, vehicle_models=vehicle_models, years=years, brands_vehicle=brands_vehicle, categories=categs)

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