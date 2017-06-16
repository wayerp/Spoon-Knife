#!/usr/bin/env python
#-*- coding:utf-8 -*-
##################################################################################
##																				##
##	coded by: DunkelMeister (gab_delgadillo@outlook.com)						##
##																				##
##################################################################################
##################################################################################
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

class sudemore(osv.Model):
	_inherit = 'pos.order'
	

	def sudemore_process(self, cr,uid,limit,context=None):
		if not context:
			context = {}
		inv_obj = self.pool.get('account.invoice')
		lin_obj = self.pool.get('account.invoice.line')
		usr_obj = self.pool.get('res.users')

		today_start = time.strftime('%Y-%m-%d 00:00:00')
		today_end 	= time.strftime('%Y-%m-%d 23:59:59')
	 	this_usr = usr_obj.browse(cr,uid,uid,context=context)
		shop = this_usr.shop_id
		today_orders = self.search(cr,uid,[('date_order','>=',today_start),('date_order','=',today_end),('shop_id','=',shop.id)],context=context)
		total = 0
		
		new_invoice = {
						'partner_id':shop.default_partner.id,
						'company_id':this_usr.company_id.id,
						'account_id':shop.default_partner.property_account_receivable.id,
						'currency_id':this_usr.company_id.currency_id.id,
						'journal_id':shop.sales_journal.id,
						}
		for order in self.browse(cr,uid,today_orders,context=context):
			total += order.amount_total
			if total >= limit:
				break
			for line in order.lines:
				income_acc = line.product_id.property_account_income and line.product_id.property_account_income.id or line.product_id.categ_id.property_account_income_categ and line.product_id.categ_id.property_account_income.id or False
				new_line = {
						'product_id':line.product_id.id,
						'quantity':line.qty,
						'name':line.product_id.name,
						'price_unit':line.price_unit,
						'account_id':income_acc,
						'invoice_id':invoice,
						}
