from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta
from medical_appointment import str2datetime

class medical_activity_task(models.Model):
    _name = 'medical.activity.task'
    
    summary = fields.Text('Summary')
    time = fields.Float('Time')
    date = fields.Datetime('Date', default=lambda self: datetime.today())
    staff_id = fields.Many2one('hr.employee', string='Done By', ondelete="restrict", domain ="[('category_parent', 'in',['Medical'])]")
    activity_id = fields.Many2one('medical.activity', string='Activity', ondelete="cascade")

class medical_activity_type(models.Model):
	_name = 'medical.activity.type'
	
	name = fields.Char(string='Name', size=100)
	description = fields.Text(string='Description')
	active = fields.Boolean('Active', default=True, help="For records associated with other records!")
	service_type = fields.Selection([('preventive', 'Preventive'), ('curative', 'Curative')], 'Service Type')
	type_medical_service = fields.Selection([('occupational', 'Occupational'), ('integral', 'Integral')],'Type Medical Service')

	@api.constrains('name')
	def _check_name(self, cr, uid, ids,context=None):
		if context is None:
			context = {}
		for rec in self.browse(cr, uid, ids, context=context):
			cr.execute("SELECT id FROM medical_activity_type WHERE id != %d AND lower(trim(name)) = lower(trim('%s'))" %(rec.id, rec.name,))
			if len(cr.fetchall())>0:
				raise ValidationError("The name must be unique!")

class medical_activity(models.Model):
    
    _name = 'medical.activity'

    @api.depends('patient_ids')
    def _get_served_qty(self):
        for rec in self:
            rec.served_qty = len(rec.patient_ids)
    
    @api.depends('nursing_service_ids','patient_ids')
    def _get_total_served(self):
        for rec in self:
            total_served = 0
            if rec.served_qty and len(rec.nursing_service_ids) > 0:
                total_served = rec.served_qty * len(rec.nursing_service_ids)
            rec.total_served = total_served

    @api.onchange('nursing_service_ids', 'patient_ids')
    def onchange_patient_nursing(self):
        for rec in self:
            if rec.patient_ids:
                rec.served_qty = len(rec.patient_ids)
                if len(rec.nursing_service_ids) > 0:
                    rec.total_served = rec.served_qty*len(rec.nursing_service_ids[0][2])

    name = fields.Char(string='Activity No', size=10, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('programmed', 'Programmed'), ('running', 'Running'), 
                            ('executed', 'executed'), ('annulled', 'Annulled')],'State')
    create_date = fields.Date(string='Create Date', readonly=True)
    programmed_by = fields.Char(string='Programmed By', size=120, readonly=True, default=lambda self: self.env.user.name)
    programming_date = fields.Datetime(string='Programming Date', default = lambda self: str(datetime.today()+timedelta(minutes=10)))
    start_date = fields.Datetime(string='Start Date', default = lambda self: str(datetime.today()+timedelta(minutes=10)))
    end_date = fields.Datetime(string='End Date', default = lambda self: str(datetime.today()+timedelta(minutes=10)))
    execution_date = fields.Datetime(string='Execution Date', readonly=True)
    executed_date = fields.Datetime(string='Executed Date', readonly=True)
    rescheduled = fields.Boolean('Rescheduled', readonly=True)
    postpone = fields.Boolean('Postpone')
    activity_type_id = fields.Many2one('medical.activity.type', string='Type', ondelete="restrict")
    remark = fields.Char('Remark', size=120)
    staff_id = fields.Many2one('hr.employee', 'Staff', readonly=True, ondelete="restrict")
    type_partakers = fields.Selection([('internal', 'Internal'), ('external', 'External'), ('combined', 'Combined')],'Type Partakers')
    served_qty = fields.Integer(compute='_get_served_qty', string='Served', store=True)
    total_served = fields.Integer(compute='_get_total_served', string='Total Served', store=True)
    activity_task_ids = fields.One2many('medical.activity.task', 'activity_id', string='Task')
    patient_ids = fields.Many2many('res.partner', string='Patients', domain ="[('type','=','patient')]")
    nursing_service_ids = fields.Many2many('medical.nursing.service', string='Nursing Service')
    staff_ids = fields.Many2many('hr.employee', string='Staff', domain ="[('category_parent', 'in',['Medical'])]")

    @api.constrains('programming_date')
    def _check_programming_date(self):
        now = datetime.today()  
        for rec in self:
            if rec.programming_date and (not rec.state) and (not rec.postpone):
                if str2datetime(rec.programming_date)< now:
                    raise ValidationError("The programming date can not be less to the current date!")
    
    @api.constrains('start_date')    
    def _check_start_date(self):
        for rec in self:
            if rec.start_date and rec.programming_date:
                if str2datetime(rec.start_date) < str2datetime(rec.programming_date):
                    raise ValidationError("The start date can not be less to the programming date!")

    @api.constrains('end_date')    
    def _check_end_date(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                if str2datetime(rec.start_date) > str2datetime(rec.end_date):
                   raise ValidationError("The end date can not be less to the start date!")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('medical_activity_code')
        return super(medical_activity, self).create(vals)
 
    @api.model
    def write(self, values):
        if values.get('programming_date') != self.programming_date:
            values['rescheduled'] = True
        return super(medical_activity, self).write(values)

    def update_state(self, status):
        vals = {'state': status}
        today = datetime.today()
        if status == 'running':
            vals.update({'execution_date': today})
        elif status == 'executed':
            vals.update({'executed_date': today})
        self.write(vals)
        return True