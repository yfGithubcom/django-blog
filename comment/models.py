from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from article.models import Article


# Create your models here.

class Comment(models.Model):
    # 被评论的文章
    article = models.ForeignKey(verbose_name='文章', to=Article,
                                on_delete=models.CASCADE, related_name='comment')
    # 评论的用户
    user = models.ForeignKey(verbose_name='用户', to=User,
                             on_delete=models.CASCADE, related_name='comment')
    content = RichTextField(verbose_name='内容')
    # 评论时间,可用 default=timezone.now() 替换 auto_now=True 或 auto_now_add=True
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', ]

    def __str__(self):
        return self.content[:20]  # 预览前20个字符
