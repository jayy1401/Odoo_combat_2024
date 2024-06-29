# __manifest__.py
{
    'name': 'Todo Collaboration',
    'version': '1.0',
    'summary': 'Real-time multi-user collaboration todo list application',
    'category': 'Productivity',
    'author': 'Your Name',
    'depends': ['base', 'utm', 'mail', 'phone_validation'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/todo_task_views.xml',
        'views/res_users.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
