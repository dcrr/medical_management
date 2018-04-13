# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta, date

class medical_patient_disease(models.Model): 
    _name = "medical.patient.disease" 
    
    type_disease_id = fields.Many2one('medical.disease.type', 'Type of Disease', ondelete="restrict")
    disease_id = fields.Many2one('medical.disease', 'Disease', ondelete="restrict")
    idx = fields.Many2one('medical.diagnostic.impression', 'IDX', ondelete="restrict")
    chronic = fields.Boolean(string='Chronic')
    waste_ime = fields.Boolean(string='Waste Time')
    transfer = fields.Boolean(string='Transfer')
    active = fields.Boolean(string='Active')
    remark = fields.Char('Remark',size=650)
    medical_appointment_id = fields.Many2one('medical.appointment', 'Medical Appointment', ondelete="cascade")

class medical_patient_service(models.Model): 
	
	_name = "medical.patient.service" 
    
    service_id = fields.Many2one('medical.nursing.service', 'Service', ondelete="restrict")
    range = fields.Boolean(related='service_id.range', string='Range', store=False, readonly=True, copy=False)
    min_range = fields.Char(related='service_id.minimum', string='Min', store=False, readonly=True, copy=False)
    normal_range = fields.Char(related='service_id.normal', string='Normal', store=False, readonly=True, copy=False)
    max_range = fields.Char(related='service_id.maximum', string='Max', store=False, readonly=True, copy=False)
    description = fields.Char('Description',size=650)
    result = fields.Char('Result',size=650)
    altered = fields.Boolean(string='Altered')
    staff_id = fields.Many2one('hr.employee', 'Nursing Staff', ondelete="restrict") # domain=[('profession','=','enf')]
    # route_administration_id = fields.Many2one('route.administration', 'Route Administration', ondelete="restrict")
    medical_appointment_id = fields.Many2one('medical.appointment', 'Medical Appointment')
    # nursing_attention_id = fields.Many2one('medical.nursing.attention', 'Nursing Attention', ondelete="cascade"

	# def onchange_service_id(self, cr, uid, ids, service_id):
	# 	""""""
	# 	result = {}
	# 	if service_id:
	# 		service_obj = self.pool.get('nursing.service')
	# 		service = service_obj.read(cr, uid, service_id, ['range','minimum','normal','maximum'])
	# 		result.update({'value': {'range':service['range'], 'min_range':service['minimum'], 
	# 								'normal_range':service['normal'],'max_range':service['maximum']} })
	# 	else:
	# 		result.update({'value': {'range':'', 'min_range':'', 'normal_range':'','max_range':''} })
	# 	return result

class medical_appointment(models.Model):
    _name = 'medical.appointment'
    
    def _get_send_mail_to(self):
        for rec in self:
            rec.id = rec.employee_id.work_email
    
    def _get_lang(self):
        if self._context.get('lang'):
            self.lang = self._context['lang']
        else:
            lang_list = self.env['res.lang'].search([('code','=','es_VE')])
            if len(lang_list)>0:
                self.lang= lang_list.code
    
    def _appoinment_email(self):
        for rec in self:
            fecha_utc = rec.appointment_date
            fecha_utc = datetime.strptime(fecha_utc, '%Y-%m-%d %H:%M:%S')
            fecha_gmt = fecha_utc - timedelta(hours=4)
            fecha_gmt = fecha_gmt.strftime('%Y-%m-%d %H:%M:%S')
            rec.appointment_date_email = fecha_gmt
    
    def _get_quantity(self):
        for rec in self:
            rec.quantity = 1
    
    name = fields.Char(string='Code', size=120, readonly=True)
    send_mail_to = fields.Char(compute='_get_send_mail_to', string='Send mail to', store=False)
    lang = fields.Char(compute='_get_lang', string='Language', store = False)
    appointment_date = fields.Datetime('Appointment Date', select="1")
    appointment_date_email = fields.Char(compute='appoinment_email', string='Appoinment email', store=True)
    waiting_date = fields.Datetime('Waiting Date')
    attention_date = fields.Datetime('Attention Date')
    patient_id = fields.Many2one('res.partner', 'Patient', ondelete="restrict")
    patient_age = fields.Integer(string='Age', readonly=True)
    #patient_marital = fields.Char(string='Marital Status', size=60, readonly=True)
    # patient_blood_type = fields.related('patient_id', 'blood_type', string='Blood Type', type='char',store=False, readonly=True)
    # patient_blood_factor = fields.related('employee_id', 'blood_factor', string='Blood Factor', type='char',store=False, readonly=True)
    # employee_state = fields.char(string='Employee State',readonly=True)
    # employee_gender = fields.related('employee_id', 'gender', string='Gender', type='char',store=False, readonly=True)
    # employee_birthday = fields.related('employee_id', 'birthday', string='Birthday', type='date',store=False, readonly=True) 
    # employee_mobile_phone = fields.char(string='Employee Phone', readonly=True)
    # #'employee_lefty = fields.boolean('Lefty')
    # employee_educational_level = fields.many2one('hr.alucasa.educational.level', string='Educational Level', readonly=True, ondelete="restrict")
    appointmet_type_id = fields.Many2one('medical.appointment.type', 'Type Medical Appointment', ondelete="restrict")
    appointmet_type_category = fields.Char(related='appointmet_type_id.category', string='Appointment Category', store=True, readonly=True, copy=False)
    assigned_by = fields.Many2one('res.users',string='Assigned By', readonly=True, ondelete="restrict")
    rescheduled = fields.Boolean('Rescheduled', readonly=True)
    postpone = fields.Boolean('Postpone')
    state = fields.Selection([('scheduled', 'Scheduled'), ('waiting', 'Waiting'), ('annulled', 'Annulled'),
                               ('in_attention', 'In Attention'), ('attended', 'Attended')],'State')
    doctor_id = fields.Many2one('hr.employee', string='Doctor', ondelete="restrict") #, domain=[('profession','=','med')]
    reason_for_appointment = fields.Char(string='Reason for appointment', size=120)
    patient_details = fields.Text(string='Patient Details')
    medical_report = fields.Text(string='Medical Report')
    laboratory_tests = fields.Boolean(string='Laboratory Tests')
    requires_medical_leave = fields.Boolean(string='Requires Medical Leave')
    requires_diet = fields.Boolean(string='Requires Diet')
    referral = fields.Boolean(string='Referral')
    # specialist = fields.char(string='Specialist', size=300)
    # to_present = fields.text(string='To Present')
    prescription = fields.Text(string='Prescription', size=120)
    prescription_indications = fields.Text(string='Indications', size=120)
    patient_disease_ids = fields.One2many('medical.patient.disease', 'medical_appointment_id','Diseases',domain=['|',('active','=',False),('active','=',True)])
    # body_area_affected_ids = fields.one2many('body.area', 'medical_appointment_id','Body Area Affected')
    patient_service_ids = fields.One2many('medical.patient.service', 'medical_appointment_id','Patient Services')
    # clinical_analysis_ids = fields.one2many('medical.appointment.clinical.analysis', 'medical_appointment_id','Clinical Analysis')
    # template_clinical_analysis_ids = fields.many2many('template.clinical.analysis', 'medical_appointment_clinical_analysis','medical_appointment_id','template_clinical_analysis_id','Templates')
    color = fields.Integer('Color')
    quantity = fields.Integer(compute='_get_quantity', string='Count', store=True)