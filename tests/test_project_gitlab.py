# coding: utf-8
from datetime import datetime

from models.project_gitlab import GitlabConnection
from models.project_gitlab import GitlabGroup
from models.project_gitlab import GitlabProject
from odoo.tests.common import TransactionCase

# using TDD class For testing purposes
# group-ID:1386105       aleph-engineering
# group-ID:7991569       odoo-personalization
# project-Id:19264544    odoo-aleph-ce-personalization
# username:Quesada87     Yadier Abel

_TEST_URL = "https://gitlab.com/api/v4/projects"

connection = GitlabConnection()
group = GitlabGroup()
project = GitlabProject()


class TestGitlabConnection(TransactionCase):

	def setUp(self, *args, **kwargs):
		super(TestGitlabConnection, self).setUp(*args, **kwargs)
		self.test_group = self.env['gitlab.group.profile'].create(
			{
				'name': "Odoo new GROUP",
				'git_id': 1245453,
				'description': "testing description",
				'sync_last_date': datetime.now(),
			}
		)
		self.test_aleph = self.env['gitlab.group.profile'].create(
			{
				'name': "Aleph",
				'git_id': 1386105,
				'description': "filled description",
				'sync_last_date': datetime.now(),
			}
		)
		self.test_project_false = self.env['gitlab.project.profile'].create(
			{
				'name': "Project False",
				'group_git_id': 7991569,
				'git_id': "7878797",
			}
		)
		self.test_project_true = self.env['gitlab.project.profile'].create(
			{
				'name': "Project odoo",
				'group_git_id': "7991569",
				'git_id': "19264544",
			}
		)
		self.test_user_true = self.env['gitlab.user.profile'].create(
			{
				'name': "Yadier Abel",
				'username': "Quesada87",
				'git_id': "870716",
			}
		)

	def test_get_response_url(self):
		self.assertFalse(self.connection.get_response_url("blank_url"))
		self.assertFalse(self.connection.get_response_url(""))
		self.assertIsInstance(self.connection.get_response_url(_TEST_URL), list)

	def test_get_info_by_group(self):
		self.assertEqual(group._get_info_by_group(""), False)
		self.assertEqual(group._get_info_by_group("25488"), False)
		self.assertIsInstance(group._get_info_by_group("1386105"), dict)

	def test_action_sync_group_gitlab(self):
		self.assertFalse(self.test_group.action_sync_group_gitlab())
		self.assertTrue(self.test_aleph.action_sync_group_gitlab())

	def test_get_project_list(self):
		self.assertEqual(self.test_group.project_git_ids(), False)
		self.assertIsInstance(self.test_aleph.project_git_ids(), dict)
		self.assertIsInstance(self.test_aleph.project_git_ids(), list)

	def test_get_project_issues(self):
		self.assertIsInstance(self.test_project_true._get_issues_by_project, list)
		self.assertIsInstance(self.test_project_true._get_issues_by_project, dict)
		self.assertEqual(self.test_project_false._get_issues_by_project, False)

	def test_get_issues_by_username(self):
		self.assertEqual(self.test_user_true._get_issues_by_username(""), False)
		self.assertEqual(self.test_user_true._get_issues_by_username("19264544"), False)
		self.assertIsInstance(self.test_user_true._get_issues_by_username("19264544"), list)
