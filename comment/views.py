from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from article.models import Article
from .forms import CommentForm
from .models import Comment


# Create your views here.

@login_required(login_url='/user/login/')
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


@login_required(login_url='/user/login/')
def delete_comment(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    is_commenter = True if request.user.pk == comment.user.pk else False
    is_author = True if request.user.pk == article.author.pk else False

    if is_commenter or is_author:
        comment.delete()

        # article.total_comment -= 1
        comments = Comment.objects.filter(article_id=article_pk)
        article.total_comment = comments.count()
        article.save(update_fields=['total_comment'])

        return redirect(article)
    return HttpResponse('no authentication')
