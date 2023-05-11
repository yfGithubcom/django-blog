from django.urls import path
from . import views

app_name = 'user'

# 用户子路由
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('pwd_reset/<int:pk>/', views.pwd_reset, name='pwd_reset'),
    path('userprofile_edit/<int:pk>/', views.userprofile_edit, name='userprofile_edit'),
]
