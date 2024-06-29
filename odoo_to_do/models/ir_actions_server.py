# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _, tools, modules
from odoo.exceptions import ValidationError
from odoo.addons.whatsapp.tools import phone_validation as wa_phone_validation

class terminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

_logger = logging.getLogger(__name__)

class ServerActions(models.Model):
    """ Add SMS option in server actions. """
    _name = 'ir.actions.server'
    _inherit = 'ir.actions.server'

    state = fields.Selection(selection_add=[
        ('whatsapp', 'Send Whatsapp Text Message'),
    ], ondelete={'whatsapp': 'cascade'})
    # Whatsapp Template
    whatsapp_template_id = fields.Many2one(comodel_name='whatsapp.template', string="Whatsapp Templates", readonly=False, store=True)
    recompute_boolean = fields.Boolean(default=False, store=False)

    def _run_action_whatsapp(self, eval_context=None, force_send_by_cron=False):
        """
        Send a Whatsapp Text Message based on the configured template.
        :param eval_context: A dictionary containing the evaluation context.
                             It should include 'records' or 'record' to represent the active record(s).
        :type eval_context: dict | None
        :return: False if the action is unsuccessful, otherwise, None.
        :rtype: bool | None
        """
        if not eval_context or 'records' not in eval_context and 'record' not in eval_context:
            return False
        
        records = eval_context.get('records') or eval_context.get('record')
        if not records:
            return False

        if self.recompute_boolean or not self.whatsapp_template_id or (not self._context.get('active_ids') and not self._context.get('active_id')) or self._is_recompute():
            return False
        
        messages_to_send = []
        message_body = self.whatsapp_template_id.body
        mobile_number = records._find_value_from_field_path(
            self.whatsapp_template_id.phone_field
        )
        formatted_number_wa = wa_phone_validation.wa_phone_format(
            records,
            number=mobile_number,
            force_format="WHATSAPP"
        )

        data = {}
        for index, rec in enumerate(self.whatsapp_template_id.variable_ids, start=1):
            placeholder = f"{{{{{index}}}}}"
            field_value = records._find_value_from_field_path(rec.field_name)
            
            # Check if the field type is HTML and convert it to char if necessary
            field_metadata = records.fields_get([rec.field_name])[rec.field_name]
            if field_metadata['type'] == 'html':
                field_value = tools.html2plaintext(field_value)

            message_body = message_body.replace(placeholder, str(field_value))
            data[index] = field_value

        _logger.info("Creating WhatsApp message for To Do List")
        body = message_body
        _logger.info(body)
        post_values = {
            'body': body,
            'message_type': 'whatsapp_message',
        }

        if hasattr(records, '_message_log'):
            message = records._message_log(**post_values)
        
        message_vals = {
            'mail_message_id': message.id,
            'mobile_number': '+' + str(formatted_number_wa),
            'mobile_number_formatted': formatted_number_wa,
            'free_text_json': {'1': 'test'},
            'wa_template_id': self.whatsapp_template_id.id,
            'wa_account_id': self.whatsapp_template_id.wa_account_id.id,
        }
        messages_to_send.append(message_vals)

        # Send WhatsApp messages after creating all attendees
        for message_vals in messages_to_send:
            message = self.env['whatsapp.message'].create(message_vals)
            message._send(force_send_by_cron=False)
            self.recompute_boolean = True
            _logger.info(
                f"WhatsApp message sent to {message_vals['mobile_number']}"
            )

        return True
