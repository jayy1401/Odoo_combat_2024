from odoo import models, fields, api


class TodoTaskStage(models.Model):
    _name = 'todo.task.stage'
    _description = 'Todo Task Stage'

    name = fields.Char(string="Stage")
    fold = fields.Boolean(string="Fold")
    description = fields.Char(string="Description")
