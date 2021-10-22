from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    project_gitlab_id = fields.Many2one(
        comodel_name='gitlab.project.profile',
        string='Project in Gitlab',
        required=False)


# this is issue in Gitlab
class TaskProjects(models.Model):
    _inherit = 'project.task'

    id_gitlab = fields.Char(
        string='Issue-id in gitlab')
    iid_gitlab = fields.Char(
        string='Issue-iid in gitlab')
    assignees_ids = fields.One2many(
        comodel_name='gitlab.user.profile',
        string='Assignees')
    author_id = fields.Many2one(
        comodel_name='gitlab.user.profile',
        string='Author')
    project_git_id = fields.Many2one(
        comodel_name='gitlab.project.profile',
        string='Project gitlab')
    state = fields.Selection(
        string='State',
        selection=[('opened', 'opened'),
                   ('closed', 'closed'), ],
        required=False, )
    # created_at = > date_create in Odoo
    confidential = fields.Char()
    # due_date = > date_deadline in Odoo
    issue_type = fields.Selection(
        string='Issue_type',
        selection=[('issue', 'issue'),
                   ('incident', 'incident'),
                   ('test_case', 'test_case'), ],
        required=False, )
    labels = fields.Html()
    milestone = fields.Char()
    weight = fields.Char()
    has_tasks = fields.Boolean(
        string='Has_tasks',
        required=False)
    task_status = fields.Char()
    human_time_estimate = fields.Char()
    human_total_time_spent = fields.Char()
