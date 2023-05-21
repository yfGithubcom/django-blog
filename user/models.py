from django.db import models
from django.contrib.auth.models import User
# 引入内置信号
from django.db.models.signals import post_save
# 信号接收
from django.dispatch import receiver


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='userprofile')
    phone = models.CharField(verbose_name='手机号', max_length=20, blank=True)
    email = models.EmailField(verbose_name='邮箱', blank=True)
    avatar = models.ImageField(verbose_name='头像', upload_to='avatar/%Y%m%d/', blank=True)  # ImageField不存储图片本身
    biography = models.TextField(verbose_name='个人简介', max_length=100, blank=True)

    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()
