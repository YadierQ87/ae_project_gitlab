# coding: utf-8
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

	def test_get_response_url(self):
		self.assertFalse(self.connection.get_response_url("blank_url"))
		self.assertFalse(self.connection.get_response_url(""))
		self.assertIsInstance(self.connection.get_response_url(_TEST_URL), list)

	def test_get_info_by_group(self):
		self.assertEqual(group._get_info_by_group(""), False)
		self.assertEqual(group._get_info_by_group("25488"), False)
		self.assertIsInstance(group._get_info_by_group("1386105"), dict)

	def test_action_sync_group_gitlab(self):
		test_group = self.env['gitlab.group.profile'].create(
			{
				'name': 'Some Client Test',
				'linkedin_account': 'https://linkedin.com/in/someClient-237872',
			}
		)
		pass

	def test_get_project_issues(self):
		self.assertEqual(self.connection.get_project_issues(""), False)
		self.assertEqual(self.connection.get_project_issues("TR79342"), False)
		self.assertIsInstance(self.connection.get_project_issues("19264544"), list)

	def test_get_issues_by_username(self):
		self.assertEqual(self.connection.get_issues_by_username("", ""), False)
		self.assertEqual(self.connection.get_issues_by_username("19264544", "Polo56"), False)
		self.assertEqual(self.connection.get_issues_by_username("19268020", "Quesada87"), False)
		self.assertIsInstance(self.connection.get_issues_by_username("19264544", "Quesada87"), list)
