# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError

# Apparatus or body systems
class medical_body_system_type(models.Model):	
	_name = 'medical.body.system.type'

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
	body_part_ids = fields.One2many('medical.body.part', 'apparatus_id',"Body Parts", ondelete='restrict')
	system_ids = fields.One2many('medical.body.part', 'system_id',"Systems", ondelete='restrict')

	# sort by name
	_order = 'name'
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]

# Body Parts
class medical_body_part(models.Model):
	_name = 'medical.body.part'

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
	apparatus_id = fields.Many2one('medical.body.system.type', 'Apparatus', domain=['&',('active','=',True),('type','=','apparatus')], ondelete='restrict')
	system_id = fields.Many2one('medical.body.system.type', 'System', domain=['&',('active','=',True),('type','=','system')], ondelete='restrict')
	active = fields.Boolean(string='Active', default=True)

	_order = 'name'	
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]
	
# Type of disease
class medical_disease_type(models.Model):
	_name = "medical.disease.type" 
	
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
	enfermedad_ids = fields.One2many('medical.disease', 'disease_type_id', "Diseases",ondelete='restrict')
    
	_order = 'name'	
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]
	
# Disease
class medical_disease(models.Model): 
	_name = "medical.disease"

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
	disease_type_id = fields.Many2one('medical.disease.type', 'Type of Disease', required=True, domain="[('active','=',True)]", ondelete="restrict")
	active = fields.Boolean(string='Active', default=True)
    
	_order = 'name'	
	_sql_constraints = [('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]

# Types of medical appointments
class medical_appointment_type(models.Model):
	_name = "medical.appointment.type" 

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
class medical_nursing_service(models.Model):
	_name = "medical.nursing.service"

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

class medical_staff(models.Model):
	_name = 'hr.employee'
	_inherit = 'hr.employee'

	@api.onchange('profession')
	def _onchange_profession(self):
		self.specialization_id=''
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.title().strip() 
	
	profession_ids = fields.Many2many('profession', string="Professions")
	specialization_ids = fields.Many2many('specialization', string="Specializations")
	schedule_ids = fields.Many2many('resource.calendar.attendance', string="Attention Schedule")
	user_id = fields.Many2one('res.users', 'User', ondelete="restrict")

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

class medical_diagnostic_impression(models.Model):
	
	_name = 'medical.diagnostic.impression'
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.upper().strip()

	name = fields.Char(string='name', size=10)
	description = fields.Char('Description', size=120)
	active = fields.Boolean('Active', default=True)

	_order = 'name'
	_sql_constraints = [('name_uniq','unique(name)', 'The name must be unique!')]

class medical_activity_type(models.Model):
	_name = 'medical.activity.type'
	
	name = fields.Char(string='Short Name', size=10)
	description = fields.Char(string='Description', size=120)
	active = fields.Boolean('Active', default=True)
	service_type = fields.Selection([('preventive', 'Preventive'), ('curative', 'Curative')], 'Service Type')
	type_medical_service = fields.Selection([('occupational', 'Occupational'), ('integral', 'Integral')],'Type Medical Service')

	@api.constrains('name')
	def _check_name(self, cr, uid, ids,context=None):
		if context is None:
			context = {}
		for rec in self.browse(cr, uid, ids, context=context):
			cr.execute("SELECT id FROM type_activity WHERE id != %d AND lower(trim(name)) = lower(trim('%s'))" %(rec.id, rec.name,))
			if len(cr.fetchall())>0:
				raise ValidationError("The short name must be unique!")
    
	@api.constrains('name')
	def _check_description(self, cr, uid, ids,context=None):
		if context is None:
			context = {}
		for rec in self.browse(cr, uid, ids, context=context):
			cr.execute("SELECT id FROM type_activity WHERE id != %d AND lower(trim(description)) = lower(trim('%s'))" %(rec.id, rec.description,))
			if len(cr.fetchall())>0:
				raise ValidationError("The description must be unique!")