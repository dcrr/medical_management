# -*- coding: utf-8 -*-

from openerp import models, fields

# Apparatus or body systems
class type_body_system(models.Model):	
	_name = 'type.body.system'
	    		
	name = fields.Char(string='Description', size=120, required=True, help = 'Apparatus or System Full Description')
	nickname = fields.Char(string='Nickname', size=8, required=True, help = 'Short name')
	type = fields.Selection([('apparatus','Apparatus'),('system','System')], 'Apparatus or System',required=True)
	active = fields.Boolean(string='Active')