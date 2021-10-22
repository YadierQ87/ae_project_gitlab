# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
import json

import requests as requests
from odoo import models

TYPE = [('gitlab', 'GitLab')]


class GitlabConnection(models.Model):

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
                data = f'Id:{info_group["id"]} Name:{info_group["name"]}'
                return dict(group=data)
            else:
                return dict(message='404 Group Not Found')
        else:
            return dict(message='500 Error')

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
            else:
                return dict(message='404 Project Not Found')
        else:
            return dict(message='500 Error')

    # GET /projects/:id/issues?assignee_username=Quesada87  filter by name
    def get_issues_by_username(self, project_id="", username=""):
        if project_id == "" or username == "":
            return dict(message='500 Error')
        else:
            url_username = f'{self.api_url}projects/{project_id}/issues?assignee_username={username}'
            issues = self.get_response_url(url_username)
            if isinstance(issues, list) and len(issues) > 0:
                return self._list_issues(issues)
            else:
                return dict(message='404 Resource Not Found')
