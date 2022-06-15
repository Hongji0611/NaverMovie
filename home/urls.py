from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('detail/<int:id>', views.movie_detail, name='detail'),
    path('comments/<int:id>', views.comments, name='comments'),
]
