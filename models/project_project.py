# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
import logging
from datetime import datetime

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    # Using gitlab.mixin.connection allows to get data trough the gitlab API
    _name = "project.project"
    _inherit = ["project.project", "gitlab.mixin.connection"]

    git_id = fields.Char()
    group_git_id = fields.Many2one("gitlab.group.profile")
    created_in_gitlab = fields.Boolean(default=False)
    is_sync = fields.Boolean(default=False)
    ssh_url_to_repo = fields.Char(readonly=True)
    http_url_to_repo = fields.Char(readonly=True)
    web_url = fields.Char(readonly=True)
    readme_url = fields.Char(readonly=True)
    name_with_namespace = fields.Char(readonly=True)
    path = fields.Char(readonly=True)
    path_with_namespace = fields.Char(readonly=True)
    description = fields.Char(readonly=True)
    sync_last_date = fields.Datetime(readonly=True)

    # gitlab API uses GET /projects/:id/issues to get issues by project
    def _get_issues_by_project(self):
        if self.git_id:
            base_url = self._get_gitlab_url()
            url_proj = f"{base_url}projects/{self.git_id}/issues"
            issues = self.get_response_url(url_proj)
            if isinstance(issues, list) and len(issues) > 0:
                return issues
            else:
                return dict(
                    message="Project not found in Gitlab",
                )
        return False

    # gitlab API uses GET /projects/:id/ to get project's data
    def _get_info_by_project(self):
        project_id = self.git_id
        if isinstance(project_id, str) and project_id != "":
            base_url = self._get_gitlab_url()
            if isinstance(base_url, str):
                url_project = f"{base_url}projects/{project_id}"
                info_project = self.get_response_url(url_project)
                if isinstance(info_project, dict):
                    return info_project
                return False
        return False

    def make_sync_project(self, sync_project):
        # if the project exist then update
        if sync_project and isinstance(sync_project, dict):
            self.name = sync_project["name"]
            self.name_with_namespace = sync_project["name_with_namespace"]
            self.git_id = sync_project["id"]
            self.web_url = sync_project["web_url"]
            self.readme_url = sync_project["readme_url"]
            self.ssh_url_to_repo = sync_project["ssh_url_to_repo"]
            self.http_url_to_repo = sync_project["http_url_to_repo"]
            self.description = sync_project["description"]
            self.path = sync_project["path"]
            self.path_with_namespace = sync_project["path_with_namespace"]
            self.created_in_gitlab = True
            self.is_sync = True
            self.sync_last_date = datetime.now()
        else:
            return dict(
                message="Error sync! Project not found",
            )

    def action_sync_project_data(self):
        """Allows to sync data for the project obtained by gitlab api"""

        sync_project = self._get_info_by_project()
        self.make_sync_project(sync_project)
        self.action_sync_issues_list()  # run sync method for update the issues

    def create_or_update_issue(self, obj_sync):
        ProjectTask = self.env["project.task"]
        find_task = ProjectTask.search(
            [("git_id", "=", obj_sync["id"])]
        )  # if exist then update
        data_sync = {
            "git_id": obj_sync["id"],
            "iid_gitlab": obj_sync["iid"],
            "project_git_id": obj_sync["project_id"],
            "name": obj_sync["title"],
            "description": obj_sync["description"],
            "state": obj_sync["state"],
            "confidential": obj_sync["confidential"],
            "issue_type": obj_sync["issue_type"],
            "labels": obj_sync["labels"],
            "milestone": obj_sync["milestone"],
            "weight": obj_sync["weight"],
            "has_tasks": obj_sync["has_tasks"],
            "human_time_estimate": obj_sync["time_stats"]["human_time_estimate"],
            "human_total_time_spent": obj_sync["time_stats"]["human_total_time_spent"],
            "is_sync": True,
            "created_in_gitlab": True,
            "sync_last_date": datetime.now(),
        }
        if find_task:
            find_task.update(data_sync)
        else:
            new_task = ProjectTask.create(data_sync)
            self.task_ids |= new_task

    def make_sync_issues(self, sync_issues):
        if sync_issues and len(sync_issues) > 0:  # if the projects has issues
            for obj_sync in sync_issues:
                if "id" in obj_sync:
                    self.create_or_update_issue(obj_sync)
                    _logger.info("id object_info %s " % obj_sync["id"])
                else:
                    _logger.info("message request %s " % obj_sync)
        else:
            return dict(
                message="Error sync! List not found",
            )

    def action_sync_issues_list(self):
        sync_issues = self._get_issues_by_project()
        self.make_sync_issues(sync_issues)
