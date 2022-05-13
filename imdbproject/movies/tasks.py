from django.core.mail import send_mail
from celery import shared_task
from django.core.exceptions import BadRequest


@shared_task(autoretry_for=(TimeoutError, BadRequest,))
def send_mail_celery(movie):
    send_mail(
        'A new movie is added to the system: {}'.format(movie['title']),
        'Title: {}\nDescription: {}'.format(
            movie['title'], movie['description']),
        'from@example.com',
        ['miroslav.cvijanovic@vivifyideas.com'],
        fail_silently=False,
    )
