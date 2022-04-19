from django.contrib.auth.forms import UserCreationForm

from django.db.models.functions import datetime
from django.shortcuts import render
from django.views import View

from .models import *
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def get_preferred_sorted_books(user, books):
    not_sorted_tuples = tuple(((b.genre.all() & user.profile.genre.all()).count(), b) for b in books)
    sorted_tuple = sorted(not_sorted_tuples, key=lambda item: item[0], reverse=True)
    return [x[1] for x in sorted_tuple]


def get_book_of_month():
    today = datetime.datetime.now()
    return BookOfMonth.objects.get(dayOfBook__year=today.year, dayOfBook__month=today.month)


def profile(request, pk):
    user = User.objects.get(id=pk)
    books = Book.objects.filter(owner_id=pk)
    prof = Profile.objects.get(user_id=pk)
    return render(request, 'catalog/profile_of_user.html',
                  {'user': user,
                   'books': books,
                   'book_of_month': get_book_of_month(),
                   'profile': prof})


class MainListView(View):
    def get(self, request):
        books = Book.objects.exclude(owner_id=request.user.id)
        return render(request, 'catalog/main.html',
                      {'books': get_preferred_sorted_books(request.user, books),
                       'user.id': request.user.id,
                       'book_of_month': get_book_of_month()})


def book(request, pk):
    book = Book.objects.get(id=pk)
    return render(request, 'catalog/book.html', {'book': book,
                                                 'book_of_month': get_book_of_month()})


class RegistrationView(CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = "catalog/reg.html"


class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'genre', 'image']
    success_url = '/book/' + str(model.id)

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'genre', 'image']
    success_url = '/book/' + str(model.id)


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


class ReviewCreateView(CreateView):
    model = Review
    fields = ['text']
    success_url = '/'

    def form_valid(self, form):
        form.instance.critic_id = self.request.user.id
        form.instance.book_id = self.kwargs['pk']
        return super().form_valid(form)


class ReviewUpdateView(UpdateView):
    model = Review
    fields = ['text']
    success_url = '/'


class ReviewDeleteView(DeleteView):
    model = Review
    success_url = '/'
