# -*- coding: utf-8 -*-

from openerp import models, fields, api

# Apparatus or body systems
class type_body_system(models.Model):	
	_name = 'type.body.system'

	@api.onchange('nickname')
	def _onchange_nickname(self):
		if self.nickname:
			self.nickname = self.nickname.upper().strip()
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.title().strip()
	    		
	name = fields.Char(string='Description', size=120, required=True, help = 'Apparatus or System Full Description')
	nickname = fields.Char(string='Nickname', size=8, required=True, help = 'Short name')
	type = fields.Selection([('apparatus','Apparatus'),('system','System')], 'Apparatus or System',required=True)
	active = fields.Boolean(string='Active', default=True)
	bodypart_ids = fields.One2many('body.part', 'apparatus_id',"Body Parts", ondelete='restrict')
	system_ids = fields.One2many('body.part', 'system_id',"systems", ondelete='restrict')

	# sort by name
	_order = 'name'
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]

# Body Parts
class body_part(models.Model):
	_name = 'body.part'

	@api.onchange('nickname')
	def _onchange_nickname(self):
		if self.nickname:
			self.nickname = self.nickname.upper().strip()
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.title().strip()
		    		
	name = fields.Char(string='Description', size=120, required=True, help = 'Body Part description')
	nickname = fields.Char(string='Nickname', size=8, required=True, help = 'Short name')
	location = fields.Selection([('L','Left'),('R','Right'), ('B','Both'),('N','Not Apply')], 'Location',required=True)
	apparatus_id = fields.Many2one('type.body.system', 'Apparatus', domain=['&',('active','=',True),('type','=','apparatus')], ondelete='restrict')
	system_id = fields.Many2one('type.body.system', 'System', domain=['&',('active','=',True),('type','=','system')], ondelete='restrict')
	active = fields.Boolean(string='Active', default=True)

	_order = 'name'	
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]
	
# Type of disease
class type_disease(models.Model):
	_name = "type.disease" 
	
	@api.onchange('nickname')
	def _onchange_nickname(self):
		if self.nickname:
			self.nickname = self.nickname.upper().strip()
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name: 
			self.name = self.name.title().strip()
	
	name = fields.Char(string='Description', size=120, required=True, help = 'Full Disease Description')
	nickname = fields.Char(string='Nickname', size=8, required=True, help = 'Short name')
	active = fields.Boolean(string='Active', default=True)
	enfermedad_ids = fields.One2many('disease', 'type_disease_id', "Diseases",ondelete='restrict')
    
	_order = 'name'	
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]
	
# Disease
class disease(models.Model): 
	_name = "disease"

	@api.onchange('nickname')
	def _onchange_nickname(self):
		if self.nickname: 
			self.nickname = self.nickname.upper().strip()
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name: 
			self.name = self.name.title().strip()

	name = fields.Char(string='Description', size=500, required=True, help = 'Disease description')
	nickname = fields.Char(string='Nickname', size=8, required=True, help = 'Short name')
	type_disease_id = fields.Many2one('type.disease', 'Type of Disease', required=True, domain="[('active','=',True)]", ondelete="restrict")
	active = fields.Boolean(string='Active', default=True)
    
	_order = 'name'	
	_sql_constraints = [('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]

# Types of medical appointments
class type_medical_appointment(models.Model):
	_name = "type.medical.appointment" 

	@api.onchange('nickname')
	def _onchange_nickname(self):
		if self.nickname:
			self.nickname = self.nickname.upper().strip()
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name: 
			self.name = self.name.title().strip()
		
	name = fields.Char(string='Description', size=120, required=True, help = 'Appointment Full Description')
	nickname = fields.Char(string='Nickname', size=10, required=True, help = 'Short Name')
	category = fields.Selection([('curative','Curative'),('preventive','Preventive')], 'Category',required=True)	
	active = fields.Boolean(string='Active',default=True)

	_order = 'name'	
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]
	
# Services provided by nursing
class nursing_service(models.Model):
	_name = "nursing.service"

	@api.onchange('nickname')
	def _onchange_nickname(self):
		if self.nickname:
			self.nickname = self.nickname.upper().strip()
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.title().strip()
	
	@api.onchange('range')
	def _onchange_range(self):
		if  self.range == False:
			self.normal = ''
			self.minimum = ''
			self.maximum = ''
	
	name = fields.Char(string='Description', size=120, required=True, help = 'Full Description')
	nickname = fields.Char(string='Nickname', size=10, required=True, help = 'Short Name')
	range = fields.Boolean(string='Range')
	normal = fields.Char(string='Normal Range', size=20, help = 'Normal or Average value')
	minimum = fields.Char(string='Minimum Range', size=20, help = 'Minimum range value')
	maximum = fields.Char(string='maximum Range', size=20, help = 'Maximum range value')
	category = fields.Selection([('curative','Curative'),('preventive','Preventive')], 'Category',required=True)
	active = fields.Boolean(string='Active', default=True)

	_order = 'name'	 
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]
_PER_ESP = [('','')]

class res_partner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	@api.onchange('profession')
	def _onchange_profession(self):
		self.specialization_id=''
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.title().strip() 
	
	user_id = fields.Many2one('res.users', 'User', ondelete="restrict")
	#active = fields.Boolean(string='Active',default=True)

	_order = 'name'
	_sql_constraints = [('name_uniq','unique(name)', 'The name must be unique!')]

# Professions
class profession(models.Model):
	_name = "profession"
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.title().strip()

	name = fields.Char(string='Profession', size=30,required=True)
	active = fields.Boolean(string='Active',default=True)

	_order = 'name'
	_sql_constraints = [('name_uniq','unique(name)', 'The name must be unique!')]	

# Specialization
class specialization(models.Model):
	_name = "specialization" 

	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.title().strip()
				
	name = fields.Char(string='Specialty', size=30,required=True)
	active = fields.Boolean(string='Active',default=True)
	
	_order = 'name'
	_sql_constraints = [('name_uniq','unique(name)', 'The name must be unique!')]	