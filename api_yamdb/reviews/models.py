from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model()

USER_ROLES = (
    ('anon', 'Аноним'), # Скорее всего лишнее, разберемся по ходу спринта
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
    ('superuser', 'Суперюзер Django'), # Скорее всего лишнее (есть встроенные атрибуты), разберемся по ходу спринта
)

# Мысли в слух о кастомной модели для юзера
# Переопределить нужно по другому
# class UserUser(models.Model):
#     username = models.CharField(max_length=50)
#     email = models.EmailField()
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     bio = models.TextField()
#     role = models.CharField(max_length=50, choices=USER_ROLES)

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='titles'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )
    year = models.IntegerField(
        'Год публикации', db_index=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'



class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(
            fields=('author', 'title',),
            name='unique_review'
        )]


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='genre'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
