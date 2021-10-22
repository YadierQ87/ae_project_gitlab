# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
import json
from datetime import datetime

import requests as requests
from odoo import fields, models, api

_SECRET_TOKEN = 'zTeQqdG9LLAGahSW5e9Y'
_BASE_URL = "https://gitlab.com/api/v4/"

_CODE_404 = 404
_CODE_200 = 200


class GitlabConnection:
    def __init__(self):
        self.gh_session = requests.Session()

    def __del__(self):
        self.gh_session.close()

    def get_response_url(self, url):
        if isinstance(url, str) and _BASE_URL in url:
            response_git = self.gh_session.get(url, headers={'PRIVATE-TOKEN': _SECRET_TOKEN})
            if response_git.status_code == _CODE_404:
                return False
            elif response_git.status_code == _CODE_200:
                return json.loads(response_git.text)
        else:
            return False


connection = GitlabConnection()


class GitlabGroup(models.Model):
    _name = "gitlab.group.profile"
    _description = "Gitlab Group Profile Copy"

    name = fields.Char("Title")
    git_name = fields.Char("Name in Gitlab")
    git_id = fields.Char(required=True)  # Example id: 1386105
    web_url = fields.Char()
    path = fields.Char()
    description = fields.Char()
    visibility = fields.Char()
    avatar_url = fields.Char()

    def action_sync_project_gitlab(self):
        # todo sync from gitlab
        pass

    # GET /groups/:id/
    @staticmethod
    def get_info_by_group(group_id=""):
        if isinstance(group_id, str) and group_id != "":
            url_group = f'{_BASE_URL}groups/{group_id}'
            info_group = connection.get_response_url(url_group)
            if isinstance(info_group, dict):
                return info_group
        return False

    @api.model
    def create(self, values):
        info_group = self.get_info_by_group(values.get('git_id'))
        if isinstance(info_group, dict):  # if the group id exist in gitlab
            values['git_name'] = info_group['git_name']
            values['web_url'] = info_group['web_url']
            values['path'] = info_group['path']
            values['description'] = info_group['description']
            values['visibility'] = info_group['visibility']
            values['avatar_url'] = info_group['avatar_url']
            if len(info_group["projects"]) > 0:  # if the group has projects
                project = self.env["gitlab.project.profile"]
                for proj in info_group["projects"]:
                    project.create(
                        {'name': proj["name"],
                         'git_id': proj["git_id"],
                         'description': proj["description"],
                         'name_with_namespace': proj["name_with_namespace"],
                         'ssh_url_to_repo': proj["ssh_url_to_repo"],
                         'http_url_to_repo': proj["http_url_to_repo"],
                         'web_url': proj["web_url"],
                         'readme_url': proj["readme_url"],
                         'path': proj["path"],
                         'path_with_namespace': proj["path_with_namespace"], }
                    )
        return super(GitlabGroup, self).create(values)


class GitlabProject(models.Model):
    _name = "gitlab.project.profile"
    _description = "Gitlab Project Profile Copy"

    name = fields.Char("Title")
    git_id = fields.Char()  # Example id: 19264544
    ssh_url_to_repo = fields.Char()
    http_url_to_repo = fields.Char()
    web_url = fields.Char()
    readme_url = fields.Char()
    name_with_namespace = fields.Char()
    path = fields.Char()
    path_with_namespace = fields.Char()
    description = fields.Char()

    def action_sync_project_gitlab(self):
        # todo sync from gitlab
        pass

    @staticmethod
    def _create_issues_from_list(self, issues: list):
        task = self.env['project.task']
        if len(issues) > 0:
            for issue in issues:
                # todo left to add assignees_ids , author_id and project_git_id
                task.create({'id_gitlab': issue['id'],
                             'iid_gitlab': issue['iid'],
                             'name': issue['title'],
                             'description': issue['description'],
                             'state': issue['state'],
                             'labels': issue['labels'],
                             'issue_type': issue['issue_type'],
                             'confidential': issue['confidential'],
                             'date_deadline': issue['due_date'],
                             'milestone': issue['milestone'],
                             'weight': issue['weight'],
                             'task_status': issue['task_status'],
                             'human_time_estimate': issue['human_time_estimate'],
                             'human_total_time_spent': issue['human_total_time_spent'],
                             'is_sync': True,
                             'sync_last_date': datetime.now()
                             })
        return False

    # GET /projects/:id/issues
    def create_issues_by_project(self):
        if self.git_id:
            url_proj = f'{_BASE_URL}projects/{self.git_id}/issues'
            issues = self.get_response_url(url_proj)
            if isinstance(issues, list):
                self._create_issues_from_list(issues)
        return False

    # GET /projects/:id/issues?assignee_username=Quesada87  filter by name
    def create_issues_by_username(self, username=""):
        if self.git_id and username:
            url_username = f'{_BASE_URL}projects/{self.git_id}/issues?assignee_username={username}'
            issues = self.get_response_url(url_username)
            if isinstance(issues, list):
                self._create_issues_from_list(issues)
        return False


class GitlabUser(models.Model):
    _name = "gitlab.user.profile"
    _description = "Gitlab User Profile Copy"

    git_id = fields.Char()
    name = fields.Char()
    username = fields.Char()
    state = fields.Char()
    avatar_url = fields.Char()
    web_url = fields.Char()
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Contact', )


class GitlabConfig(models.Model):
    _name = "gitlab.system.config"

    name = fields.Char()
    secret_token = fields.Char(
        string='Secret_token',
        required=False)
    api_url = fields.Char(
        string='Api_url',
        required=False)
