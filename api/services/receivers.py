from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from api.models import Comment, Answer, Review, Question


@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def count_comments(sender, instance, **kwargs):
    article = instance.article
    article.recount_comment_count()


@receiver(post_save, sender=Answer)
@receiver(post_delete, sender=Answer)
def count_answers(sender, instance, **kwargs):
    # recount answers of question this answer related to
    instance.question.recount_answer_count()

    # recount answers of author this answers related to
    instance.author.recount_answer_count()


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def count_rating(sender, instance, **kwargs):
    # recount rating of user review sent to
    instance.adressee.recount_rating()


@receiver(post_save, sender=Question)
@receiver(post_delete, sender=Question)
def count_questions(sender, instance, **kwargs):
    instance.author.recount_question_count()

