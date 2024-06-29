# __manifest__.py
{
    'name': 'Todo Collaboration',
    'version': '1.0',
    'summary': 'Real-time multi-user collaboration todo list application',
    'category': 'Productivity',
    'author': 'Your Name',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_task_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
