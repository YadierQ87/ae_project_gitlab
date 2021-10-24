# coding: utf-8
{
    "name": "Gitlab Integration with odoo project",
    "summary": """
        This module allows user seen their issues and projects from gitlab with simple configuration""",
    "version": "1.0.0",
    "license": "AGPL-3",
    "author": "Yadier Abel De Quesada, Solprob",
    "website": "https://solprob.nat.cu",
    "application": False,
    "installable": True,
    "depends": ["base", "project", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/project_gitlab_views.xml",
        "views/res_user_views.xml",
    ],
    "demo": [],
}
