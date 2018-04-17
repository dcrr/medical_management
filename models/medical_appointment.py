# -*- coding: utf-8 -*-

from openerp import models, fields, api, netsvc
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta, date
import re
from collections import Counter

IDENTIFICATION_PATTERN = re.compile(r"^(\d{7,8})$",re.IGNORECASE)

class medical_patient_disease(models.Model): 
    _name = "medical.patient.disease" 
    
    disease_type_id = fields.Many2one('medical.disease.type', 'Type of Disease', ondelete="restrict")
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

class medical_body_area(models.Model):
	_name = "medical.body.area"
	
	body_system_type_id = fields.Many2one('medical.body.system.type', 'Type of System', ondelete="restrict")
	body_part_id = fields.Many2one('medical.body.part', 'Body Part', ondelete="restrict")
	on_left = fields.Boolean(string='On Left')
	on_right = fields.Boolean(string='On Right')
	on_both = fields.Boolean(string='On Both')
	remark = fields.Char('Remark',size=650)
	medical_appointment_id = fields.Many2one('medical.appointment', 'Medical Appointment')

class medical_appointment_template_analysis(models.Model):
    _name = 'medical.appointment.template.analysis'
    
    template_analysis_id = fields.Many2one('medical.template.analysis', 'Medical Analysis')
    medical_appointment_id = fields.Many2one('medical.appointment', 'Medical appointment')
    remark = fields.Text('Remark') 

class medical_patient(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    def _get_age(self):
        today = date.today()
        for rec in self:
            born = datetime.strptime(rec.birthday, '%Y-%m-%d')
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    identification = fields.Char(string='Identification Number', size=12)
    gender = fields.Selection([('female', 'Female'), ('masculine', 'Masculine')], 'Marital Status')
    marital = fields.Selection([('single', 'Single'), ('married', 'married'),('widower', 'Widower'), ('divorced', 'Divorced')], 'Marital Status')
    age = fields.Integer(compute='_get_age', string='Age')


def str2datetime(x):
    if not x: return False
    if len(x)>10:
        format = "%Y-%m-%d %H:%M:%S"
        x = x[0:19]
    else:
         format = "%Y-%m-%d"
    date = datetime.strptime(x, format)
    return date

def str2date(x):
    if not x: return False
    if len(x)>10:
        format = "%Y-%m-%d %H:%M:%S"
        x = x[0:19]
    else:
         format = "%Y-%m-%d"
    date = datetime.strptime(x, format).date()
    return date

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
    
    @api.onchange('template_analysis_ids')
    def _onchange_template_analysis_ids(self):
        if len(self.template_analysis_ids[0][2])==0:
            self.analysis_ids = []
            return        
        analysis_ids = []
        out_analysis_ids = self.analysis_ids[:]
        for analysis in self.analysis_ids:
            template_analysis_id = False 
            if analysis[1]:
                template_analysis_id = self.env['medical.appointment.template.analysis'].read(analysis[1], ['template_analysis_ids'])
                template_analysis_id = template_analysis_id['template_analysis_ids'][0] if template_analysis_id else False
            elif analysis[2]:
                if analysis[2].get('template_analysis_id'):
                    template_analysis_id = analysis[2]['template_analysis_id']
             
            if template_analysis_id:
                if template_analysis_id in self.template_analysis_ids[0][2]:
                    analysis_ids.append(template_analysis_id)
                else:
                    index= self.analysis_ids.index(analysis)
                    del out_analysis_ids[index]
             
        for template_clinical_analysis_id in self.template_analysis_ids[0][2]:
            if template_clinical_analysis_id not in analysis_ids:
                out_analysis_ids.append((0, self.template_analysis_ids[0][1], {'template_analysis_id':template_analysis_id}))

        self.analysis_ids = out_analysis_ids

    # @api.onchange('patient_id')
    # def _onchange_patient_id(self):
    #     self.get_data_patient_id(self.patient_id,'')
    
    # @api.onchange('appointment_date')
    # def _onchange_appointment_date(self):
    #     if self.appointment_date and self.state in ['scheduled','waiting',False] and  not self.postpone: 
    #         appointment_date = str2datetime(self.appointment_date)
    #         if appointment_date < datetime.today():
    #             if date.today() == appointment_date.date():
    #                 appointment_date = appointment_date + timedelta(minutes=5)
    #                 self.appointment_date = str(appointment_date)
    #             else:
    #                 self.appointment_date = ''
    #                 return {'warning': {'title': "Warning",'message': "The appointment date must be greater or equal to the current date!",}}
    #     for rec in self:
    #         if rec.appointment_date != appointment_date:
    #             rec.rescheduled = True
    #             rec.assigned_by = self.env.uid
    #         else:
    #             rec.rescheduled = False

    name = fields.Char(string='Code', size=120, readonly=True)
    send_mail_to = fields.Char(compute='_get_send_mail_to', string='Send mail to', store=False)
    lang = fields.Char(compute='_get_lang', string='Language', store = False)
    appointment_date = fields.Datetime('Appointment Date', select="1")
    appointment_date_email = fields.Char(compute='_appoinment_email', string='Appoinment email', store=True)
    waiting_date = fields.Datetime('Waiting Date')
    attention_date = fields.Datetime('Attention Date')
    patient_id = fields.Many2one('res.partner', 'Patient', ondelete="restrict")
    patient_age = fields.Integer(string='Age', readonly=True)
    patient_marital = fields.Selection(related='patient_id.marital', string='Marital Status', readonly=True, store=True, copy=False)
    patient_name = fields.Char(related='patient_id.name', string='Patient', readonly=True, store=True, copy=False)
    # patient_blood_type = fields.related('patient_id', 'blood_type', string='Blood Type', type='char',store=False, readonly=True)
    # patient_blood_factor = fields.related('employee_id', 'blood_factor', string='Blood Factor', type='char',store=False, readonly=True)
    # employee_state = fields.char(string='Employee State',readonly=True)
    # employee_gender = fields.related('employee_id', 'gender', string='Gender', type='char',store=False, readonly=True)
    # employee_birthday = fields.related('employee_id', 'birthday', string='Birthday', type='date',store=False, readonly=True) 
    # employee_mobile_phone = fields.char(string='Employee Phone', readonly=True)
    # #'employee_lefty = fields.boolean('Lefty')
    # employee_educational_level = fields.many2one('hr.alucasa.educational.level', string='Educational Level', readonly=True, ondelete="restrict")
    appointmet_type_id = fields.Many2one('medical.appointment.type', 'Type Medical Appointment', ondelete="restrict")
    appointmet_category = fields.Selection(related='appointmet_type_id.category', string='Appointment Category', store=True, readonly=True, copy=False)
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
    referral_specialty_id = fields.Many2one('specialization',string='Referred specialty', ondelete="restrict")
    specialist_name = fields.Char(related='referral_specialty_id.name', string='Referred specialty', store=True, readonly=True, copy=False)
    # to_present = fields.text(string='To Present')
    prescription = fields.Text(string='Prescription', size=120)
    prescription_indications = fields.Text(string='Indications', size=120)
    patient_disease_ids = fields.One2many('medical.patient.disease', 'medical_appointment_id','Diseases',domain=['|',('active','=',False),('active','=',True)])
    body_area_affected_ids = fields.One2many('medical.body.area', 'medical_appointment_id','Body Area Affected')
    patient_service_ids = fields.One2many('medical.patient.service', 'medical_appointment_id','Patient Services')
    template_analysis_ids = fields.Many2many('medical.template.analysis', 'Templates')
    analysis_ids = fields.One2many('medical.appointment.template.analysis', 'medical_appointment_id','Medical Analysis')
    color = fields.Integer('Color')
    quantity = fields.Integer(compute='_get_quantity', string='Count', store=True)
    
    @api.constrains('name')
    def _check_name(self):
            for rec in self:
                rec.env.cr.execute("SELECT id FROM medical_appointment WHERE id != %d AND lower(trim(name)) = lower(trim('%s'))" %(rec.id, rec.name,))            
                if len(rec.env.cr.fetchall())>0:
                    raise ValidationError("The medical appointment code must be unique! Contact your administrator.")
    
    @api.constrains('appointment_date') 
    def _check_appointment_date(self):
        now = datetime.today()
        for rec in self:
            if rec.appointment_date and (not rec.state) and (not rec.postpone):
                if str2datetime(rec.appointment_date)< now:
                    raise ValidationError("The appointment date must be greater or equal to the current date!")
    
    @api.constrains('waiting_date')
    def _check_waiting_date(self):
        for rec in self:
            if rec.waiting_date:
                if str2datetime(rec.waiting_date) > str2datetime(rec.appointment_date):
                    raise ValidationError("The waiting date can not be greater to the appointment date!")
    
    @api.constrains('attention_date')
    def _check_attention_date(self):
        for rec in self:
            if rec.attention_date and rec.waiting_date:
                if str2datetime(rec.waiting_date) > str2datetime(rec.attention_date):
                    raise ValidationError("The waiting date can not be greater to the attention date!")

    def send_email_template(self, template_name):
        salesorder_tpl = self.env['email.template'].search([('name','=',template_name)])
        if len(salesorder_tpl)>0:
            self.env['email.template'].send_mail(salesorder_tpl[0],id,False)

    def update_state(self, state):
        for rec in self:
            rec.write({'state':state})
            if (state == 'scheduled' and rec.rescheduled):
                rec.send_email_template('Template Mail Medical Appointment Rescheduled')
            elif state == 'scheduled':
                rec.send_email_template('Template Mail Medical Appointment Scheduled')
            elif state == 'annulled':
                rec.send_email_template('Template Mail Medical Appointment Annulled')
        return True

    def validate_appointment_date_annul(self):
        today = date.today()
        for rec in self:
            if rec.appointment_date:
                if ((today - str2date(rec.appointment_date))+timedelta(days=1)).days > 4:
                    return True
        return False

    def reevaluate_workflow(self):
        wf_service = netsvc.LocalService("workflow")
        if len(self) == 0:
            self.search(['|',('state','=','scheduled'),('state','=','waiting')])
        for rec in self:
            wf_service.trg_write(rec.env.users, 'medical.appointment', rec.id, rec.env.cr)

    def waiting(self):
        vals ={'state':'waiting'}
        today = datetime.today()
        for rec in self:        
            if rec['state'] != 'in_attention':
                if rec['postpone']:
                    if not rec['waiting_date']:
                        raise ValidationError("You must enter the wating date!")
                else:
                    vals.update({'waiting_date': today})
            self.write(vals)
        return True

    def in_attention(self):
        vals ={'state':'in_attention'}
        today = datetime.today()
        for rec in self.read(['postpone','state','employee_id','waiting_date','attention_date']):    
            if rec['state'] != 'attended': 
                if rec['postpone']:
                    if not rec['attention_date']:
                        raise ValidationError("You must enter the attention date!")
                else:
                    vals.update({'attention_date': today})
                         
                staff = self.env['staff'].search([('user_id','=',rec.env.users)])
                if len(staff)>0:
                    vals.update({'doctor': staff[0]})
            self.write(vals)
            return True

    def get_categories(self):
        self.env.cr.execute("SELECT DISTINCT category \ FROM type_medical_appointment")
        category_list = [category[0] for category in self.env.cr.fetchall()]
        res={}
        for category in category_list:
            res.update({category:0})
        return res

    def calculate_statistics(self, user_type, period=None):
        res=[]
        if period:
            self.env.cr.execute("SELECT b.category, d.name as disease_type, a.employee_management, a.employee_management_code \
                        FROM medical_appointment a \
                           LEFT JOIN type_medical_appointment b \
                           ON a.type_medical_appointmet_id = b.id \
                           LEFT JOIN patient_disease c \
                           ON a.id = c.medical_appointment_id \
                           LEFT JOIN type_disease d \
                           ON c.type_disease_id = d.id \
                        WHERE a.state = 'attended' AND \
                             a.attention_date BETWEEN '"+period['lower_date']+"' AND '"+period['top_date']+"'")
 
            cont_dict = Counter(self.env.cr.fetchall())
            for key in cont_dict.keys():
                res.append({'period_id':period['id'],'user_type':'doctor','category':key[0], 'type_disease':key[1], 'management':key[2], 'management_code':key[3], 'quantity': cont_dict[key]})
        return res
    
    def calculate_attentions_by_category(self, period=None):
        res={}
        if period:
            res= self.get_categories()
            self.env.cr.execute("SELECT a.id, b.category \
                        FROM medical_appointment a JOIN type_medical_appointment b \
                            ON a.type_medical_appointmet_id = b.id \
                        WHERE a.state = 'attended' AND \
                              a.attention_date BETWEEN '"+period['lower_date']+"' AND '"+period['top_date']+"'")
            
            for rec in self.env.cr.fetchall():
                res[rec[1]] = res[rec[1]]+1
                return res

    def calculate_attentions_by_disease_type(self, period=None):
        res={}
        if period:
            where = ''
            domain = ''
            for element in domain:
                where = 'AND '+element[0]+element[1]+element[2]
                where = eval(self.env.context['domain']) if self.env.context['domain'] else None
                self.env.cr.execute("SELECT a.id, b.category, d.name as disease_type \
                        FROM medical_appointment a JOIN type_medical_appointment b \
                            ON a.type_medical_appointmet_id = b.id \
                            JOIN patient_disease c \
                            ON a.id = c.medical_appointment_id \
                            JOIN type_disease d \
                            ON c.type_disease_id = d.id \
                        WHERE a.state = 'attended' AND \
                              a.attention_date BETWEEN '"+period['lower_date']+"' AND '"+period['top_date']+"'")
            res = self.get_categories()
            for rec in self.env.cr.fetchall():
                if rec[1] in res.keys():
                    if not res[rec[1]]:
                        res[rec[1]] = {rec[2]:1}
                    else:
                        if rec[2] in res[rec[1]].keys():
                            res[rec[1]][rec[2]] = res[rec[1]][rec[2]]+1
                        else:
                            res[rec[1]].update({rec[2]:1})
                else:
                    res.update({[rec[1]]:{rec[2]:1}}) 
        return res