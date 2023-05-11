from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Article(models.Model):
    author = models.ForeignKey(verbose_name='作者', to=User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=100)
    body = models.TextField(verbose_name='正文')
    created = models.DateTimeField(verbose_name='文章创建时间', default=timezone.now)
    updated = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    total_visit = models.PositiveIntegerField(verbose_name='浏览量', default=0)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created', '-updated', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.pk])
