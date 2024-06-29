# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    manager_id = fields.Many2one('res.users', 'Manager')
