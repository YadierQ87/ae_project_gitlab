# coding: utf-8
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    gitlab_profile_ids = fields.One2many(
        comodel_name='gitlab.user.profile',
        inverse_name='partner_id',
        string='Gitlab_profile_id',
        required=False)
