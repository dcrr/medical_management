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
	    		
	name = fields.Char(string='Name', size=120, required=True, help = 'Name')
	nickname = fields.Char(string='Nickname', size=12, required=True, help = 'Short name')
	type = fields.Selection([('apparatus','Apparatus'),('system','System')], 'Apparatus or System',required=True)
	active = fields.Boolean(string='Active', default=True, help="For records associated with other records!")
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
		    		
	name = fields.Char(string='Name', size=120, required=True, help='Name')
	nickname = fields.Char(string='Nickname', size=12, required=True, help = 'Short name')
	location = fields.Selection([('L','Left'),('R','Right'), ('B','Both'),('N','Not Apply')], 'Location',required=True)
	apparatus_id = fields.Many2one('medical.body.system.type', 'Apparatus', domain=['&',('active','=',True),('type','=','apparatus')], ondelete='restrict')
	system_id = fields.Many2one('medical.body.system.type', 'System', domain=['&',('active','=',True),('type','=','system')], ondelete='restrict')
	active = fields.Boolean(string='Active', default=True, help="For records associated with other records!")

	_order = 'name'	
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('nickname_uniq', 'unique (nickname)', 'The nickname must be unique!'),]

class medical_diseases_classification(models.Model):
	_name = "medical.disease.classification"

	name = fields.Char(string="Name")
	version = fields.Char(string="Version")
	description = fields.Text(string="Description")
	active = fields.Boolean(string='Active', default=True, help="For records associated with other records!")
	disease_type_ids = fields.One2many('medical.disease.type', 'classification_id', "Diseases Type",ondelete='restrict')

# Type of disease
class medical_disease_type(models.Model):
	_name = "medical.disease.type" 
	
	@api.onchange('code')
	def _onchange_code(self):
		if self.code:
			self.code = self.code.upper().strip()
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name: 
			self.name = self.name.title().strip()
	
	name = fields.Char(string='Name', size=300, required=True, help = 'Name')
	code = fields.Char(string='Code', size=8, required=True, help = 'Code')
	classification_id = fields.Many2one('medical.disease.classification', string="Classification")
	active = fields.Boolean(string='Active', default=True, help="For records associated with other records!")
	disease_ids = fields.One2many('medical.disease', 'disease_type_id', "Diseases",ondelete='restrict')
    
	_order = 'name'	
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The description must be unique!'),
        ('code_uniq', 'unique (code)', 'The code must be unique!'),]
	
# Disease
class medical_disease(models.Model): 
	_name = "medical.disease"

	@api.onchange('code')
	def _onchange_code(self):
		if self.code: 
			self.code = self.code.upper().strip()
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name: 
			self.name = self.name.title().strip()

	name = fields.Char(string='Name', size=500, required=True, help = 'Name')
	code = fields.Char(string='Code', size=8, required=True, help = 'Code')
	disease_type_id = fields.Many2one('medical.disease.type', 'Type of Disease', required=True, domain="[('active','=',True)]", ondelete="restrict")
	active = fields.Boolean(string='Active', default=True, help="For records associated with other records!")
    
	_order = 'name'	
	_sql_constraints = [('name_uniq', 'unique (name)', 'The name must be unique!'),]
	
# Services provided by nursing
class medical_nursing_service(models.Model):
	_name = "medical.nursing.service"

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
	
	name = fields.Char(string='Name', size=100, required=True, help = 'Name')
	description = fields.Text(string='Description',required=True, help='Description')
	range = fields.Boolean(string='Range')
	normal = fields.Char(string='Normal Range', size=20, help='Normal or Average value')
	minimum = fields.Char(string='Minimum Range', size=20, help='Minimum range value')
	maximum = fields.Char(string='Maximum Range', size=20, help='Maximum range value')
	category = fields.Selection([('curative','Curative'),('preventive','Preventive')], 'Category',required=True)
	active = fields.Boolean(string='Active', default=True, help="For records associated with other records!")

	_order = 'name'	 
	_sql_constraints = [('name_uniq', 'unique (name)', 'The description must be unique!'),]
_PER_ESP = [('','')]

class medical_staff(models.Model):
	_name = 'hr.employee'
	_inherit = 'hr.employee'

	@api.one
	@api.depends('name', 'last_name')
	def _compute_display_name(self):
		for rec in self:
			if rec.name and rec.last_name:
				rec.display_name = rec.name.lstrip().rstrip() + ' ' + rec.last_name.lstrip().rstrip()
			else:
				rec.display_name = rec.name
	
	@api.multi
	def name_get(self):
		for rec in self:
			res = []
			if rec.env.context.get('special_display_name'):
				res.append((rec.id, "%s" % (rec.display_name)))
			else:
				res = super(medical_staff, self).name_get()
			return res
			
	last_name = fields.Char(string='Last Name', size=300)
	display_name = fields.Char(string='Name', compute='_compute_display_name')	
	category_name = fields.Char(related="category_ids.name", string="Category")
	category_parent = fields.Char(related="category_ids.parent_id.name", string="Parent Category")
	profession_ids = fields.Many2many('profession', string="Professions")
	specialization_ids = fields.Many2many('specialization', string="Specializations")
	schedule_ids = fields.Many2many('resource.calendar.attendance', string="Attention Schedule")
	user_id = fields.Many2one('res.users', 'User', ondelete="restrict")

	_order = 'name'

# Professions
class profession(models.Model):
	_name = "profession"
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.title().strip()

	name = fields.Char(string='Profession', size=30,required=True)
	active = fields.Boolean(string='Active',default=True, help="For records associated with other records!")

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
	active = fields.Boolean(string='Active',default=True, help="For records associated with other records!")
	
	_order = 'name'
	_sql_constraints = [('name_uniq','unique(name)', 'The name must be unique!')]

class medical_diagnostic_impression(models.Model):
	
	_name = 'medical.diagnostic.impression'
	
	@api.onchange('name')
	def _onchange_name(self):
		if self.name:
			self.name = self.name.upper().strip()

	name = fields.Char(string='name', size=10)
	description = fields.Text('Description')
	active = fields.Boolean('Active', default=True, help="For records associated with other records!")

	_order = 'name'
	_sql_constraints = [('name_uniq','unique(name)', 'The name must be unique!')]

class medical_analysis_type(models.Model):	
	_name = 'medical.analysis.type'
	
	name = fields.Char(string='Name', size=120)
	description = fields.Text('Description')
	analysis_group_ids = fields.One2many('medical.analysis.group', 'analysis_type_id','Groups', ondelete='restrict')

class medical_analysis_group(models.Model):
	_name = 'medical.analysis.group'
	
	name = fields.Char(string='Name', size=120)
	description = fields.Text('Description')
	analysis_type_id = fields.Many2one('medical.analysis.type', 'Type', ondelete="restrict")

class medical_analysis(models.Model):
	_name = 'medical.analysis'
	
	name = fields.Char(string='Name', size=120)
	description = fields.Text('Description')

class medical_analysis_details(models.Model):
	_name = 'medical.analysis.details'
	
	name = fields.Char(string='Name', size=120)
	description = fields.Text('Description')
	
class medical_template_analysis(models.Model):
	_name = 'medical.template.analysis'
	
	def _get_name(self):
		for rec in self:
			rec.name = rec.type_id.name+'/'+rec.group_id.name+'/'+rec.analysis_id.name
			if rec.details_id:
				rec.name = rec.name+'/'+rec.details_id.name

	name = fields.Char(compute='_get_name', method=True,string='Name', 
						store={'medical.template.analysis':(lambda  self:['group_id','type_id','analysis_id','details_id'] , 10)})
	group_id = fields.Many2one('medical.analysis.group', 'Group', ondelete="restrict")
	type_id = fields.Many2one(related='group_id.analysis_type_id', string='Type', relation='medical.analysis.type', store=True, ondelete="restrict")
	analysis_id = fields.Many2one('medical.analysis', 'Medical Analysis', ondelete="restrict")
	details_id = fields.Many2one('medical.analysis.details', 'Details', ondelete="restrict")