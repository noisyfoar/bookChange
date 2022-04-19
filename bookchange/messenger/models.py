from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
# noinspection PyUnresolvedReferences
from catalog.models import Book


# Во-первых чаты могут быть двух видов. Первый - это личная беседа двух человек. Второй вид - это коллективый чат. Реализован только диалог, чат будет потом но кирпичик уже сделан
class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = ((DIALOG, 'Dialog'), (CHAT, 'Chat'))

    type = models.CharField('Тип', max_length=1, choices=CHAT_TYPE_CHOICES, default=DIALOG)

    members = models.ManyToManyField(User)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    trade_owner = models.BooleanField(default=False)
    trade_customer = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def get_absolute_url(self):
        return reverse('messenger-message', args=[str(self.id)])

    def __str__(self):
        # noinspection PyUnresolvedReferences
        return str(self.id)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField("Message")
    pub_date = models.DateTimeField("Date", default=timezone.now)
    is_readed = models.BooleanField("Прочитано", default=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['pub_date']

    def __str__(self):
        return self.message
