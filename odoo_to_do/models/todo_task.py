# models/todo_task.py
from odoo import models, fields, api
from odoo.exceptions import AccessError

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task'

    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description')
    due_date = fields.Date(string='Due Date')
    assignee_id = fields.Many2one('res.users', string='Assignee')
    priority = fields.Selection(
        [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        string='Priority', default='medium'
    )
    status = fields.Selection(
        [('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')],
        string='Status', default='todo'
    )
    comments = fields.One2many('todo.comment', 'task_id', string='Comments')

class TodoComment(models.Model):
    _name = 'todo.comment'
    _description = 'Todo Task Comment'

    content = fields.Text(string='Comment', required=True)
    task_id = fields.Many2one('todo.task', string='Task')
    user_id = fields.Many2one('res.users', string='User')
