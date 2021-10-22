# coding: utf-8
from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    gitlab_profile_ids = fields.One2many(
        comodel_name='gitlab.user.profile',
        inverse_name='partner_id',
        string='Gitlab_profile_id',
        required=False)
