# -*- coding: utf-8 -*-
{
    'name' : 'Medical Management',
    'version' : '1.0.0',
    'author' : 'Eduardo Tirado, Diana Rojas',
    'category' : 'Medical',
    'description' : """ Medical Management """,
    "depends" : ['base', 'resource', 'hr'],
	'data' : ['views/views.xml',
              'views/menu.xml',
              'workflow/medical_appointment_wkf.xml',
              ],
	'active': True,
    'installable': True	
}