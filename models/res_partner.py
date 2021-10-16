# coding: utf-8
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    sex = fields.Selection(
        string='Sexo',
        selection=[('M', 'M'),
                   ('F', 'F'),
                   ('Other', 'Other')],
        required=False, )
    given_name = fields.Char(
        string='Given name',
        required=False)
    email_work = fields.Char(
        string='Email Work',
        required=False)
    phone_work = fields.Char(
        string='Phone Work',
        required=False)
    mobile_work = fields.Char(
        string='Phone Work',
        required=False)
    # social networks
    whatsapp = fields.Char(
        string='Whatsapp',
        required=False)
    telegram = fields.Char(
        string='telegram',
        required=False)
    linkedin = fields.Char(
        string='linkedin',
        required=False)
    github = fields.Char(
        string='github',
        required=False)
    other_social = fields.Char(
        string='Other Social',
        required=False)
    salary = fields.Float(
        string='Salary',
        required=False)
    ministery = fields.Many2one(
        comodel_name='sp.talent.ministery.name',
        string='Ministery',
        required=False)
    # educational title
    educational_title_ids = fields.One2many(
        comodel_name='sp.talent.educational.title',
        inverse_name='partner_id',
        string='Educational_title_ids',
        required=False)
    docent_category_id = fields.Many2one(
        comodel_name='sp.talent.category.name',
        string='',
        required=False)
    # service list
    service_ids = fields.One2many(
        comodel_name='sp.talent.service.list',
        inverse_name='partner_id',
        string='List of Services',
        required=False)
    # language list
    language_ids = fields.One2many(
        comodel_name='sp.talent.language.list',
        inverse_name='partner_id',
        string='Language List',
        required=False)
    # specialization areas
    specialty_ids = fields.Many2many(
        comodel_name='sp.talent.specialty.name',
        string='Specialties')
