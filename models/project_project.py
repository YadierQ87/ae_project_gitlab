from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    project_gitlab = fields.Char(
        string='Project-Id in gitlab',
        required=False)


# this is issue in Gitlab
class TaskProjects(models.Model):
    _inherit = 'project.task'

    issue_gitlab = fields.Char(
        string='Issue-Id in gitlab',
        required=False)
    assignees = fields.One2many(
        comodel_name='gitlab.user.profile',
        string='Assignees',
        required=False)
    gitlab_profile_id = fields.Many2one(
        comodel_name='gitlab.user.profile',
        string='Gitlab profile id',
        required=False)
