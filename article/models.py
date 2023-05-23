from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from mdeditor.fields import MDTextField


# Create your models here.

class ArticleColumn(models.Model):  # 文章专栏
    title = models.CharField(verbose_name='专栏名称', max_length=60, blank=True)
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '专栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Article(models.Model):
    author = models.ForeignKey(verbose_name='作者', to=User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=100)
    # detail = models.CharField(verbose_name='摘要', max_length=100)
    body = MDTextField(verbose_name='正文')
    created = models.DateTimeField(verbose_name='文章创建时间', default=timezone.now)
    updated = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    total_visit = models.PositiveIntegerField(verbose_name='浏览量', default=0)
    total_comment = models.PositiveIntegerField(verbose_name='评论条数', default=0)
    column = models.ForeignKey(
        verbose_name='专栏', to=ArticleColumn,
        null=True, blank=True, default='',
        on_delete=models.CASCADE, related_name='article'
    )
    tags = TaggableManager(verbose_name='标签', blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created', '-updated', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.pk])
