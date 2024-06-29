# models/todo_task.py
from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.exceptions import AccessError


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task'
    _inherit = ['mail.thread.cc',
                'mail.thread.blacklist',
                'mail.thread.phone',
                'mail.activity.mixin',
                'utm.mixin',
                'format.address.mixin',
                'mail.tracking.duration.mixin',
                ]
    _primary_email = 'email_from'
    _track_duration_field = 'stage_id'

    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean('Active', default=True, tracking=True)
    due_date = fields.Date(string='Due Date')
    assignee_ids = fields.Many2many('res.users', string='Assignee')
    priority = fields.Selection(
        [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        string='Priority', default='medium'
    )
    # status = fields.Selection(
    #     [('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')],
    #     string='Status', default='todo'
    # )
    comments = fields.One2many('todo.comment', 'task_id', string='Comments')
    stage_id = fields.Many2one(
        'todo.task.stage', string='Stage', index=True, tracking=True, readonly=False, store=True,
        compute='_compute_stage_id', group_expand='_read_group_stage_ids',
        copy=False, ondelete='restrict')
    email_from = fields.Char(
        'Email', tracking=40, index='trigram',
        compute='_compute_email_from', inverse='_inverse_email_from', readonly=False, store=True)

    @api.depends('assignee_ids.email')
    def _compute_email_from(self):
        for lead in self:
            if lead.assignee_ids.email:
                lead.email_from = lead.assignee_ids.email

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.depends('stage_id')
    def _compute_stage_id(self):
        for todo_task in self:
            if not todo_task.stage_id:
                new_stage = self.env['todo.task.stage'].search(domain=[('fold', '=', False)])
                todo_task.stage_id = new_stage.id


class TodoComment(models.Model):
    _name = 'todo.comment'
    _description = 'Todo Task Comment'

    content = fields.Text(string='Comment', required=True)
    task_id = fields.Many2one('todo.task', string='Task')
    user_id = fields.Many2one('res.users', string='User')
