from catalog.models import Book, BookOfMonth
from django.db.models import Count
from django.db.models.functions import datetime
from django.shortcuts import render, redirect
from django.views import View

from .forms import MessageForm
from .models import *


def get_book_of_month():
    today = datetime.datetime.now()
    return BookOfMonth.objects.get(dayOfBook__year=today.year, dayOfBook__month=today.month)


# Для получения списка всех диалогов, в которых задействован пользователь, необходимо провести фильтрацию всех чатов
# по участникам, то есть по Many-toMany полю members. В данном случае у меня меня имеется шаблон для диалогов,
# в который я передаю авторизованного пользователя и список чатов. Активный пользователь будет нужен для корректного
# отображения прочитанных и не прочитанных сообщений в списке диалогов.
class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'messenger/dialogs.html', {'user_profile': request.user, 'chats': chats,
                                                          'book_of_month': get_book_of_month()})


# Для отображения текущего диалога и сообщений уже потребуется более сложная логика. Дело в том, что здесь доступ к
# чату осуществляется по ID, но необходимо сделать не только попытку получения диалога, но и проверить, существует ли
# в списке участников пользователь, который пытается попасть в данный чат. Если он не существует в списке участников,
# то доступ в данный чат ему запрещён. Помимо прочего в этом же представлении обрабатывается отсылка сообщений и
# пометка сообщений прочитанными.
class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None
        return render(request, 'messenger/messages.html',
                      {'user_profile': request.user, 'chat': chat, 'form': MessageForm(),
                       'book_of_month': get_book_of_month()})

    def post(self, request, chat_id):
        if 'message' in request.POST:
            form = MessageForm(data=request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.chat_id = chat_id
                message.author = request.user
                message.save()
            return redirect(reverse('messenger:dialog', kwargs={'chat_id': chat_id}))
        else:
            chat = Chat.objects.get(id=chat_id)
            book = Book.objects.get(chat=chat)
            owner = book.owner
            if owner == request.user:
                chat.trade_owner = not chat.trade_owner
            else:
                chat.trade_customer = not chat.trade_customer
            if chat.trade_customer and chat.trade_owner:
                book.owner = chat.members.exclude(id=owner.id).first()
                book.save()
                message = Message.objects.create(chat=chat, author=owner, message="Обмен произошел. Новый владелец:" + book.owner)
                message.save()
                chat.trade_owner = not chat.trade_owner
                chat.trade_customer = not chat.trade_customer
            chat.save()
            return redirect(reverse('messenger:dialog', kwargs={'chat_id': chat_id}))


# На данный момент реализован лишь один метод для начала беседы с пользователем. Необходимо перейти на страницу
# пользователя и нажать на кнопку "Написать сообщение", тогда через ссылку будет отправлен запрос, в котором будет
# создан чат или найден уже существующий чат с этим пользователем. Здесь испольуется проверка на то, является ли чат
# диалогом или беседой нескольких пользователей. Что позволяет несколько упростить поиск необходимого диалога.
class CreateDialogView(View):
    def get(self, request, user_id, book_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(
            c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create(book=Book.objects.get(id=book_id))
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('messenger:dialog', kwargs={'chat_id': chat.id}))
