from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('reg/', views.RegistrationView.as_view(), name='reg'),

    path('', login_required(views.MainListView.as_view()), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('book/create/', login_required(views.BookCreateView.as_view()), name='addBook'),
    path('book/<int:pk>', login_required(views.book), name='book'),
    path('book/<int:pk>/update', login_required(views.BookUpdateView.as_view()), name='updateBook'),
    path('book/<int:pk>/delete', login_required(views.BookDeleteView.as_view()), name='deleteBook'),

    path('author/create/', login_required(views.AuthorCreateView.as_view()), name='addAuthor'),
    path('author/<int:pk>/update', login_required(views.AuthorUpdateView.as_view()), name='updateAuthor'),
    path('author/<int:pk>/delete', login_required(views.AuthorDeleteView.as_view()), name='deleteAuthor'),

    path('profile/create/', login_required(views.ProfileCreateView.as_view()), name='addProfile'),
    path('profile/<int:pk>', login_required(views.profile), name='profile'),
    path('profile/<int:pk>/update', login_required(views.ProfileUpdateView.as_view()), name='updateProfile'),

    path('review/create/<int:pk>', login_required(views.ReviewCreateView.as_view()), name='addReview'),
    path('review/<int:pk>/update', login_required(views.ReviewUpdateView.as_view()), name='updateReview'),
    path('review/<int:pk>/delete', login_required(views.ReviewDeleteView.as_view()), name='deleteReview'),

]
