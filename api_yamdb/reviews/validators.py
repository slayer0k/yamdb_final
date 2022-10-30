import datetime as dt

from django.core.exceptions import ValidationError


def check_year(value):
    if value > dt.datetime.today().year:
        raise ValidationError(
            'Год издания не может быть больше нынешнего'
        )


def validate_score(value):
    if not (0 < value < 11):
        raise ValidationError(
            'Допустимая оценка - от 1 до 10 баллов'
        )
    return value
