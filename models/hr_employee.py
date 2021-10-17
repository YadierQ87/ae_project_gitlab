from odoo import fields, models, api
import requests
import json


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
    def do_get_projects_by_groups(self):
        pass

    # GET /users/:user_id/projects
    """https://gitlab.com/api/v4/groups/aleph-engineering/issues?assignee_username=Quesada87"""
    def do_get_repositories_list(self):
        username = 'Quesada87'
        token = ''
        repos_url = 'https://github.com/YadierQ87?tab=repositories'

        # create a re-usable session object with the user creds in-built
        gh_session = requests.Session()
        gh_session.auth = (username, token)

        # get the list of repos belonging to me
        repos = json.loads(gh_session.get(repos_url).text)

        # print the repo names
        for repo in repos:
            print(repo['name'])
        # make more requests using "gh_session" to create repos, list issues, etc.


