from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('reg/', views.RegistrationView.as_view(), name='reg'),
    path('profile/<int:pk>', login_required(views.profile), name='profile'),
    path('', login_required(views.MainListView.as_view()), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('book/<int:pk>', login_required(views.book), name='book'),
    path('book/create/', views.BookCreate.as_view(), name='addBook'),
]
