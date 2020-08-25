from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

from api import services


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # importing model classes
        from api.services import receivers

        # registering signals with the model's string label
        post_save.connect(receivers.count_answers, sender='api.Answer')
        post_save.connect(receivers.count_comments, sender='api.Comment')
        post_save.connect(receivers.count_rating, sender='api.Review')

        post_delete.connect(receivers.count_answers, sender='api.Answer')
        post_delete.connect(receivers.count_comments, sender='api.Comment')
        post_delete.connect(receivers.count_rating, sender='api.Review')
