from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('reg/', views.RegistrationView.as_view(), name='reg'),
    path('profile/<int:pk>', login_required(views.profile), name='profile'),
    path('', login_required(views.MainListView.as_view()), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('book/<int:pk>', login_required(views.book), name='book'),
    path('book/create/', views.BookCreateView.as_view(), name='addBook'),
    path('book/<int:pk>/update', views.BookUpdateView.as_view(), name='updateBook'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(), name='deleteBook'),
    path('author/create/', views.AuthorCreateView.as_view(), name='addAuthor'),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name='updateAuthor'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='deleteAuthor'),

]
