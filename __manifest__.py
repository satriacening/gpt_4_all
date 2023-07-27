# -*- coding: utf-8 -*-

{
    'name': 'GPT4All Integration',
    'version': '1.0.0',
    'license': 'AGPL-3',
    'summary': 'Odoo ChatGPT Integration',
    'description': 'GPT4All is an alternative to chatGPT. GPT4All is free and does not require api_key. Allows the application to leverage the capabilities of the GPT language model to generate human-like responses, providing a more natural and intuitive user experience',
    'author': 'Satria Putra',
    'website': 'https://github.com/satriacening',
    'depends': ['base', 'base_setup', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_channel_data.xml',
        'data/user_partner_data.xml',
    ],
    'external_dependencies': {'python': ['gpt4all']},
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
