from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import datetime
from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def get_book_of_month():
    today = datetime.datetime.now()
    return BookOfMonth.objects.get(dayOfBook__year=today.year, dayOfBook__month=today.month)


def profile(request, pk):
    user = User.objects.get(id=pk)
    books = Book.objects.filter(owner_id=pk)
    try:
        profile = Profile.objects.get(user_id=pk)
        profile = profile.image.url
    except Profile.DoesNotExist:
        profile = "/media/img/profiles/default.jpg"

    return render(request, 'catalog/profile.html',
                  {'user': user, 'books': books, 'book_of_month': get_book_of_month(), 'profile': profile})


class AddBookView(View):
    def get(self, request):
        return render(request, 'catalog/addBook.html', {'book_of_month': get_book_of_month()})


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


class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'genre', 'image']
    success_url = '/book/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'genre', 'image']
    success_url = '/book/'


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'


class AuthorCreateView(CreateView):
    model = Author
    fields = '__all__'
    success_url = '/book/create/'


class AuthorUpdateView(UpdateView):
    model = Author
    fields = '__all__'
    success_url = '/book/'


class AuthorDeleteView(DeleteView):
    model = Author
    success_url = '/'


class ProfileCreateView(CreateView):
    model = Profile
    fields = ['image', 'genre']
    success_url = '/'


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['image', 'genre']
    success_url = '/'
