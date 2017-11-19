from django.apps import AppConfig


class CreateyourlawsConfig(AppConfig):
    name = 'CreateYourLaws'

    def ready(self):
        from CreateYourLaws import signals
