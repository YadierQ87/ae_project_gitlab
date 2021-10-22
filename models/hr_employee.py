from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    gitlab_user = fields.Char()
    gitlab_keyword = fields.Char()
    gitlab_company = fields.Char()
