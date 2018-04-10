# -*- coding: utf-8 -*-

from openerp import models, fields, api

# Apparatus or body systems
class type_body_system(models.Model):	
	_name = 'type.body.system'

	@api.onchange('nickname')
	def _onchange_nickname(self):
		if self.nickname:
			nickname = self.nickname.upper()
			return {'value':{'nickname':nickname.strip()}}
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			name = self.name.title()
			return {'value':{'name':name.strip()}}
	    		
	name = fields.Char(string='Description', size=120, required=True, help = 'Apparatus or System Full Description')
	nickname = fields.Char(string='Nickname', size=8, required=True, help = 'Short name')
	type = fields.Selection([('apparatus','Apparatus'),('system','System')], 'Apparatus or System',required=True)
	active = fields.Boolean(string='Active')
	bodypart_ids = fields.One2many('body.part', 'apparatus_id',"Body Parts", ondelete='restrict')
	system_ids = fields.One2many('body.part', 'system_id',"systems", ondelete='restrict')

# Body Parts
class body_part(models.Model):
	_name = 'body.part'

	@api.onchange('nickname')
	def _onchange_nickname(self):
		if self.nickname:
			nickname = self.nickname.upper()
			return {'value':{'nickname':nickname.strip()}}
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			name = self.name.title()
			return {'value':{'name':name.strip()}}
	
		    		
	name = fields.Char(string='Description', size=120, required=True, help = 'Body Part description')
	nickname = fields.Char(string='Nickname', size=8, required=True, help = 'Short name')
	location = fields.Selection([('L','Left'),('R','Right'), ('B','Both'),('N','Not Apply')], 'Location',required=True)
	apparatus_id = fields.Many2one('type.body.system', 'Apparatus', domain=['&',('active','=',True),('type','=','apparatus')], ondelete='restrict')
	system_id = fields.Many2one('type.body.system', 'System', domain=['&',('active','=',True),('type','=','sistem')], ondelete='restrict')
	active = fields.Boolean(string='Active')