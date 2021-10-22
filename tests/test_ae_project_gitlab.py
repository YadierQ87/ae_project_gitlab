# coding: utf-8
from models import GitlabConnection
from odoo.tests.common import TransactionCase


# using TDD class For testing purposes
# group-ID:1386105       aleph-engineering
# group-ID:7991569       odoo-personalization
# project-Id:19264544    odoo-aleph-ce-personalization
# username:Quesada87     Yadier Abel


class TestGitlabConnection(TransactionCase):

	def __init__(self, *args, **kwargs):
		super(TestGitlabConnection, self).__init__(*args, **kwargs)
		self.connection = GitlabConnection()
		self.test_url = "https://gitlab.com/api/v4/projects/"

	def test_get_response_url(self):
		self.assertFalse(self.connection.get_response_url("blank_url"))
		self.assertFalse(self.connection.get_response_url(""))
		self.assertIsInstance(self.connection.get_response_url(self.test_url), list)

	def test_get_info_by_group(self):
		self.assertEqual(self.connection.get_info_by_group(""), {"message": "500 Error"})
		self.assertEqual(self.connection.get_info_by_group("25488"), {"message": "404 Group Not Found"})
		self.assertIsInstance(self.connection.get_info_by_group("1386105"), dict)

	def test_get_project_issues(self):
		self.assertEqual(self.connection.get_project_issues(""), {"message": "500 Error"})
		self.assertEqual(self.connection.get_project_issues("TR79342"), {"message": "404 Project Not Found"})
		self.assertIsInstance(self.connection.get_project_issues("19264544"), list)

	def test_get_issues_by_username(self):
		self.assertEqual(self.connection.get_issues_by_username("", ""), {"message": "500 Error"})
		self.assertEqual(self.connection.get_issues_by_username("19264544", "Polo56"),
						 {"message": "404 Resource Not Found"})
		self.assertEqual(self.connection.get_issues_by_username("19268020", "Quesada87"),
						 {"message": "404 Resource Not Found"})
		self.assertIsInstance(self.connection.get_issues_by_username("19264544", "Quesada87"), list)
