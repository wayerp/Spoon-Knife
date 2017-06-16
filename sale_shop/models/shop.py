#!/usr/bin/env python
#-*- coding:utf-8 -*-
##################################################################
##																##
##	coded by: DunkelMeister (gab_delgadillo@outlook.com)		##
##																##
##################################################################
##################################################################################
#    																			##
#    OpenERP, Open Source Management Solution									##
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).						##
#																				##
#    This program is free software: you can redistribute it and/or modify		##
#    it under the terms of the GNU Affero General Public License as				##
#    published by the Free Software Foundation, either version 3 of the			##
#    License, or (at your option) any later version.							##
#																				##
#    This program is distributed in the hope that it will be useful,			##
#    but WITHOUT ANY WARRANTY; without even the implied warranty of				##
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the				##
#    GNU Affero General Public License for more details.						##
#																				##
#    You should have received a copy of the GNU Affero General Public License	##
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     	##
#																				##
##################################################################################

import logging
import psycopg2
import time
from datetime import datetime

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools import float_is_zero
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
import openerp.addons.product.product

_logger = logging.getLogger(__name__)

class sale_shop(osv.osv):
	_name = "sale.shop"

	_columns = {	
		'name': fields.char('Name', required=True, readonly=True, copy=False),
		'company_id':fields.many2one('res.company', 'Company', required=True, readonly=True),
		'warehouse_id':fields.many2one('stock.warehouse','Warehouse',required=True),
		'fiscal_position_id':fields.many2one('account.fiscal.position','Fiscal Position'),
		'default_partner':fields.many2one('res.partner','Default Partner'),
		'sales_journal':fields.many2one('account.journal','Sale Journal',domain="[('type','=','sale')]")
			}

class sale_or(osv.Model):
	_inherit = 'sale.order'
	
	_columns ={
		'shop_id': fields.many2one('sale.shop','Shop'),		
			}

class user_u(osv.Model):
	_inherit = 'res.users'
	
	_columns = {
		'shop_id':fields.many2one('sale.shop','Shop')			
			}

class points(osv.Model):
	_inherit = 'pos.config'
	
	_columns ={
		'shop_id':fields.many2one('sale.shop','Shop')
			}

class porder(osv.Model):
	_inherit = 'pos.order'

	_columns ={
		'shop_id':fields.many2one('sale.shop','Shop')
			}


