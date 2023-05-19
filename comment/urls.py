from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('post/<int:article_pk>/', views.post_comment, name='post_comment'),
    path('delete/<int:article_pk>/', views.delete_comment, name='delete_comment'),
]
