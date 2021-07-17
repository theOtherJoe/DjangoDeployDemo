from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_reg),
    path('user/register', views.register),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('user/add_book', views.add_book),
    path('user/update_book/<int:book_id>', views.update_book),
    path('books/<int:book_id>/add_favorite', views.add_favorite),
    path('books/<int:book_id>/unfavorite', views.unfavorite),
    path('books', views.user_and_books),
    path('books/<int:book_id>', views.show_book),
]