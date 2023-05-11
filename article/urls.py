from django.urls import path
from . import views

app_name = 'article'

# article子路由
urlpatterns = [
    path('list/', views.article_list, name='article_list'),
    path('detail/<int:pk>/', views.article_detail, name='article_detail'),
    path('create/', views.article_create, name='article_create'),
    path('delete/<int:pk>/', views.article_delete, name='article_delete'),
    path('update/<int:pk>/', views.article_update, name='article_update'),
]
