# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
import json

import requests as requests
from odoo import fields, models, api


class GitlabConnection:
    def __init__(self):
        self.token = 'zTeQqdG9LLAGahSW5e9Y'
        self.api_url = "https://gitlab.com/api/v4/"
        self.gh_session = requests.Session()

    def __del__(self):
        self.gh_session.close()

    def get_response_url(self, url):
        if isinstance(url, str) and self.api_url in url:
            response_git = self.gh_session.get(url, headers={'PRIVATE-TOKEN': self.token})
            if response_git.status_code == 404:
                return False
            elif response_git.status_code == 200:
                return json.loads(response_git.text)
        else:
            return False

    # GET /groups/:id/
    def get_info_by_group(self, group_id=""):
        if isinstance(group_id, str) and group_id != "":
            url_group = f'{self.api_url}groups/{group_id}'
            info_group = self.get_response_url(url_group)
            if isinstance(info_group, dict):
                return info_group
        return False

    @staticmethod
    def _list_issues(issues):
        list_issues = []
        for issue in issues:
            data = f'Id:{issue["iid"]} Name:{issue["title"]} weight:{issue["weight"]}'
            list_issues.append({"Issue": data})
        return list_issues

    # GET /projects/:id/issues
    def get_project_issues(self, project_id=""):
        if isinstance(project_id, str) and project_id != "":
            url_proj = f'{self.api_url}projects/{project_id}/issues'
            issues = self.get_response_url(url_proj)
            if isinstance(issues, list) and len(issues) > 0:
                return self._list_issues(issues)
        return False

    # GET /projects/:id/issues?assignee_username=Quesada87  filter by name
    def get_issues_by_username(self, project_id="", username=""):
        if project_id == "" or username == "":
            return False
        else:
            url_username = f'{self.api_url}projects/{project_id}/issues?assignee_username={username}'
            issues = self.get_response_url(url_username)
            if isinstance(issues, list) and len(issues) > 0:
                return self._list_issues(issues)
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

    @api.model
    def create(self, values):
        info_group = connection.get_info_by_group(values.get('git_id'))
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

    # GET /projects/:id/issues
    def do_actions_get_projects(self):
        projects = connection.get_project_issues(self.git_id)
        if isinstance(projects, dict):
            # create for cycle in order to create all the issues or tasks for this project
            pass


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
        string='Contact',
        required=False)


class GitlabConfig(models.Model):
    _name = "gitlab.system.config"

    name = fields.Char()
    secret_token = fields.Char(
        string='Secret_token',
        required=False)
    api_url = fields.Char(
        string='Api_url',
        required=False)
