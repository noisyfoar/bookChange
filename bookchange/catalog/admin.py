from django.contrib import admin
from .models import Book, Author, Genre, Review, BookOfMonth

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(BookOfMonth)
