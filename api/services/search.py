from api.models import Question, Article, User


def get_questions(query):
    return [{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'author': {
            'id': item.author.id,
            'name': item.author.name,
            'surname': item.author.surname
        },
        'pub_date': item.pub_date,
        'answer_count': item.answer_count
    } for item in Question.objects.all().search(query=query)]


def get_articles(query):
    return [{
        'id': item.id,
        'title': item.title,
        'content': item.content,
        'pub_date': item.pub_date,
        'comment_count': item.comment_count
    } for item in Article.objects.all().search(query=query)]


def get_users(query):
    return [{
        'id': item.id,
        'name': item.name,
        'surname': item.surname,
        'rating': item.rating,
        'rank': item.rank
    } for item in User.objects.all().search(query=query)]