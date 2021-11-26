# coding: utf-8
from datetime import datetime

from odoo import fields, models
from odoo.exceptions import ValidationError


class ResUser(models.Model):
    _name = "res.users"
    _inherit = ["res.users", "gitlab.mixin.connection"]

    git_id = fields.Char(readonly=True)
    username = fields.Char(string="Username in Gitlab")
    state_git = fields.Char(readonly=True)
    avatar_url = fields.Char(readonly=True)
    web_url = fields.Char(readonly=True)
    sync_last_date = fields.Datetime(readonly=True)

    # GET /projects/:id/issues?username=name
    @staticmethod
    def _get_issues_by_username(self, project_id=""):
        if isinstance(project_id, str) and project_id != "":
            base_url = self._get_gitlab_url()
            url_user = f"{base_url}projects/{project_id}issues?username={self.username}"
            info_issues = self.get_response_url(url_user)
            if isinstance(info_issues, list):
                return info_issues
        return False

    # GET /users?username=name
    def _get_info_by_username(self):
        base_url = self._get_gitlab_url()
        if isinstance(self.username, str) and self.username != "":
            url_user = f"{base_url}users?username={self.username}"
            info_user = self.get_response_url(url_user)
            if isinstance(info_user, list) and len(info_user) > 0:
                return info_user
            else:
                raise ValidationError("User %s not found" % self.username)
        return False

    def make_sync_user(self, sync_user):
        if sync_user and isinstance(sync_user, list):  # if the user exist the update
            data_syn = {
                "username": sync_user[0]["username"],
                "git_id": sync_user[0]["id"],
                "state_git": sync_user[0]["state"],
                "avatar_url": sync_user[0]["avatar_url"],
                "web_url": sync_user[0]["web_url"],
                "sync_last_date": datetime.now(),
            }
            self.sudo().write(data_syn)
        else:
            return dict(
                message="Error sync! User not found",
            )

    def action_sync_user_data(self):
        """Allows to sync data for the user obtained by gitlab api"""

        sync_user = self._get_info_by_username()
        self.make_sync_user(sync_user)
