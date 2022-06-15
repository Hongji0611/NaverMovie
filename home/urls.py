from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.photo_search, name='search'),
    path('detail/<int:id>', views.movie_detail, name='detail'),
]
