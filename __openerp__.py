# -*- coding: utf-8 -*-
{
    'name' : 'Medical Management',
    'version' : '1.0.0',
    'author' : 'Diana Rojas, Exood',
    'category' : 'Medical',
    'description' : """ Medical Management """,
    "depends" : ['base', 
                 'resource', 
                 'hr', 
                 'food_diet'],
	'data' : ['views/views.xml',
              'views/menu.xml',
              'workflow/medical_appointment_wkf.xml',
              'workflow/medical_activity_wkf.xml',
              'data/data.xml',
              ],
	'active': True,
    'installable': True	
}