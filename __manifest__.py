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
        "views/crm_social_profile.xml",
        "views/crm_customer_template.xml",
    ],
    "demo": [],
}
