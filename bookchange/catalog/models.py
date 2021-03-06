from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class Author(models.Model):
    first_name = models.CharField(max_length=100,verbose_name='Имя автора')
    last_name = models.CharField(max_length=100,verbose_name='Фамилия автора')

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name']


class Book(models.Model):
    title = models.CharField('Название книги', max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name='Автор книги')
    summary = models.TextField('Краткое описание', max_length=1000, default=' ', blank=True)
    genre = models.ManyToManyField(Genre, blank=True, verbose_name='Жанры книги')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='img/books/default.webp', upload_to='img/books', blank=True,
                              verbose_name='Фотография книги')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # noinspection PyUnresolvedReferences
        return reverse('book', kwargs={'pk': str(self.id)})

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']


class Review(models.Model):
    critic = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    text = models.TextField('Рецензия', max_length=1000)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['book']


class BookOfMonth(models.Model):
    title = models.CharField('Название книги', max_length=50)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField('Краткое описание', max_length=1000,
                               default=' ')
    dayOfBook = models.DateField('Месяц книги')

    image = models.ImageField(upload_to='images/booksOfMonth')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга месяца'
        verbose_name_plural = 'Книги месяца'
        ordering = ['dayOfBook']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='img/profiles/default.jpg', upload_to='img/profiles', blank=True,
                              verbose_name='Ваш аватар')
    genre = models.ManyToManyField(Genre, blank=True, verbose_name='Любимые жанры',
                                   help_text="Удерживайте “Control“ (или “Command“ на Mac), чтобы выбрать несколько значений.")

    def get_absolute_url(self):
        # noinspection PyUnresolvedReferences
        return reverse('profile', kwargs={'pk': str(self.id)})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # noinspection PyUnresolvedReferences
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
