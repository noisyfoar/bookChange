from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import datetime
from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def profile(request, pk):
    user = User.objects.get(id=pk)
    books = Book.objects.filter(owner_id=pk)
    return render(request, 'catalog/profile.html', {'user': user, 'books': books, 'book_of_month': get_book_of_month()})


class AddBookView(View):
    def get(self, request):
        return render(request, 'catalog/addBook.html', {'book_of_month': get_book_of_month()})


def get_book_of_month():
    today = datetime.datetime.now()
    return BookOfMonth.objects.get(dayOfBook__year=today.year, dayOfBook__month=today.month)


class MainListView(View):
    def get(self, request):
        books = Book.objects.exclude(owner_id=request.user.id)
        return render(request, 'catalog/main.html',
                      {'books': books, 'user.id': request.user.id, 'book_of_month': get_book_of_month()})


def book(request, pk):
    book = Book.objects.get(id=pk)
    return render(request, 'catalog/book.html', {'book': book, 'book_of_month': get_book_of_month()})


class RegistrationView(CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = "catalog/reg.html"


class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summmary', 'genre', 'image']


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(DeleteView):
    model = Book
    success_url = '/'
