from django.contrib.auth import get_user_model
from django.db import models

from reviews.validators import check_year, validate_score

User = get_user_model()


class GenreCategoryBaseModel(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='name')
    slug = models.SlugField(verbose_name='slug', unique=True, max_length=50)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class ReviewCommentBaseModel(models.Model):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Основной текст для публикации'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        help_text='Дата сохраняется автоматически'
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.text


class Genre(GenreCategoryBaseModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)


class Category(GenreCategoryBaseModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        help_text='Название произведения',
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Дата издания', help_text='Дата издания произведения',
        validators=[check_year]
    )
    description = models.TextField(
        verbose_name='Краткое описание',
        blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Категория, к которой относится произведение',
        on_delete=models.SET_NULL,
        related_name="title",
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры произведения',
        help_text='Жанры, к которым относится произведение'
    )

    class Meta:
        verbose_name = 'Произведениe'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name

    def rating(self):
        return self.reviews.all().aggregate(
            models.Avg('score')
        )['score__avg']


class Review(ReviewCommentBaseModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв',
        help_text='Отзыв к выбранному произведению'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        help_text='Автор сохраняется автоматически'
    )
    score = models.PositiveSmallIntegerField(
        validators=[validate_score],
        verbose_name='Рейтинг',
        help_text='Рейтинг, присвоенный произведению'
    )

    class Meta:
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='Unique_review_from_author_for_title'
            ),
        )
        verbose_name = 'Отзыв к произведению'
        verbose_name_plural = 'Отзывы к произведениям'


class Comment(ReviewCommentBaseModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
        help_text='Комментарий к выбранному отзыву'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Автор сохраняется автоматически'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзывам'
