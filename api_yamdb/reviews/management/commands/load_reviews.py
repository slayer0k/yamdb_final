import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

CSV_PATH = 'static/data/'

CSV_FILES = {
    'user': (User, 'users.csv'),
    'category': (Category, 'category.csv'),
    'genre': (Genre, 'genre.csv'),
    'title': (Title, 'titles.csv'),
    'titlegenre': (Title.genre.through, 'genre_title.csv'),
    'review': (Review, 'review.csv'),
    'comment': (Comment, 'comments.csv'),
}

FOREIGN_KEY_FIELDS = ['title', 'author', 'review', 'genre', 'category']


class Command(BaseCommand):
    help = 'Loads data to models from .csv files'

    def add_arguments(self, parser):
        for argument in CSV_FILES:
            parser.add_argument(
                '--' + argument,
                required=False,
                action='store_true',
            )
        parser.add_argument(
            '--all',
            required=False,
            action='store_true',
        )

    def read_file(self, model, filename):
        try:
            with open(CSV_PATH + filename, encoding='utf-8') as file:
                reader = csv.DictReader(file)
                reader.fieldnames = [
                    name if name not in FOREIGN_KEY_FIELDS
                    else name + '_id' for name in reader.fieldnames
                ]
                for row in reader:
                    try:
                        model.objects.get_or_create(**row)
                    except Exception as e:
                        raise CommandError(
                            f'Ошибка при импорте данных из {filename} '
                            f'в модель {model.__name__}: {e}'
                        )
        except IOError:
            self.stdout.write(self.style.ERROR(
                f'Could not read file: {filename}'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'{filename} was successfully loaded!'
            ))

    def handle(self, *args, **options):
        if options['all']:
            for argument in CSV_FILES:
                self.read_file(*CSV_FILES[argument])
            return

        passed_arguments = (
            arg for arg in CSV_FILES.keys() if options[arg] is True
        )
        if passed_arguments:
            for argument in passed_arguments:
                self.read_file(*CSV_FILES[argument])
