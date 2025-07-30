from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

# sso/PwdResetEmail/apps.py
class PwdResetEmailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PwdResetEmail'

