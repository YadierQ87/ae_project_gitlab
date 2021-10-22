from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    create_in_gitlab = fields.Boolean(default=False)
    project_gitlab_id = fields.Many2one(
        comodel_name='gitlab.project.profile',
        string='Project in Gitlab',
        required=False)
    is_sync = fields.Boolean(default=False)
    sync_last_date = fields.Datetime()
    gitlab_id = fields.Char(related='project_gitlab_id.git_id')


# this is issue in Gitlab
class TaskProjects(models.Model):
    _inherit = 'project.task'

    is_sync = fields.Boolean(default=False)  # change to True when it is sync with gitlab
    sync_last_date = fields.Datetime()  # it is compute when task sync with gitlab
    id_gitlab = fields.Char(string='Issue-id in gitlab')
    iid_gitlab = fields.Char(string='Issue-iid in gitlab')
    _sql_constraints = [
        ('project_task_gitlab_unique',
         'UNIQUE (is_sync, id_gitlab, iid_gitlab)',
         'id_gitlab must be unique!')]
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
    confidential = fields.Char()
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

    def action_sync_task_gitlab(self):
        # todo sync from gitlab
        pass
