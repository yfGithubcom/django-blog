from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from article.models import Article
from .forms import CommentForm


# Create your views here.

def post_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            temp_form = form.save(commit=False)
            temp_form.article = article
            temp_form.user = request.user
            temp_form.save()

            article.total_comment += 1
            article.save(update_fields=['total_comment'])

            # redirect 参数是Model对象时，会自动调用Model对象的get_absolute_url()方法
            return redirect(article)
        else:
            return HttpResponse('内容违规')
    return HttpResponse('only accept post-method')


def delete_comment(request, article_pk):
    return HttpResponse('no authentication')
