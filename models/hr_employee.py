import json

import requests as requests
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    gitlab_user = fields.Char()
    gitlab_keyword = fields.Char()
    gitlab_company = fields.Char()

    gitlab_html = fields.Html(
        string='html field',
        required=False)

    """ List a project’s groups
    Get a list of ancestor groups for this project. 
    GET /projects/:id/groups   
    curl https://gitlab.example.com/api/v4/projects"""

    # https://gitlab.com/api/v4/aleph-engineering for example
    @staticmethod
    def do_get_projects_by_groups():
        username = 'Quesada87'
        token = 'zTeQqdG9LLAGahSW5e9Y'
        repos_url = "https://gitlab.com/api/v4/projects/19264544/issues?assignee_username=%s" % username

        gh_session = requests.Session()
        gh_session.auth(username, token)
        # get the list of repos belonging to me
        response_url = gh_session.get(repos_url, headers={'PRIVATE-TOKEN': token})
        repos = json.loads(response_url.text)

        # print the repo names
        for repo in repos:
            print(repo["iid"])

    # GET /users/:user_id/projects
    """https://gitlab.com/api/v4/groups/aleph-engineering/issues?assignee_username=Quesada87"""
    """https://gitlab.com/api/v4/projects/odoo-personalization/issues?assignee_username=Quesada87"""

    def do_get_repositories_list(self):
        username = 'Quesada87'
        token = 'zTeQqdG9LLAGahSW5e9Y'
        repos_url = 'https://gitlab.com/api/v4/groups/aleph-engineering/issues?assignee_username=Quesada87'

        # create a re-usable session object with the user creds in-built
        gh_session = requests.Session()
        gh_session.auth = (username, token)

        # get the list of repos belonging to me
        repos = json.loads(gh_session.get(repos_url).text)

        # print the repo names
        for repo in repos:
            print(repo['name'])
        # make more requests using "gh_session" to create repos, list issues, etc.


