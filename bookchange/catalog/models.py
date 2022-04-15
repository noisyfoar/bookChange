from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(models.Model):
    genreName = models.CharField(max_length=30)

    def __str__(self):
        return self.genreName

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['genreName']


class Review(models.Model):
    critic = models.ForeignKey(User, help_text='Имя критика', on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField('Рейтинг книги', blank=True)
    text = models.TextField('Отзыв', max_length=1000)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['book']


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name']


class Book(models.Model):
    title = models.CharField('Название книги', max_length=50)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField('Краткое описание', max_length=1000, help_text="Опишите кратко книгу",
                               default=' ', blank=True)
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр(ы) книги", blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='img/books', blank=True)
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', kwargs={'pk': str(self.id)})

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']


class BookOfMonth(models.Model):
    title = models.CharField('Название книги', max_length=50)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField('Краткое описание', max_length=1000, help_text="Опишите кратко книгу",
                               default=' ')
    dayOfBook = models.DateField('Месяц книги')

    image = models.ImageField(upload_to='images/booksOfMonth')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга месяца'
        verbose_name_plural = 'Книги месяца'
        ordering = ['dayOfBook']
