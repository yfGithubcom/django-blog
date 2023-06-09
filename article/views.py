from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
import markdown
from .models import Article
from .forms import ArticleForm
from comment.models import Comment
from comment.forms import CommentForm
from utils.paginator import custom_paginator


# Create your views here.

def article_list(request):
    search = request.GET.get('search', '')
    order = request.GET.get('order', 'common')
    column = request.GET.get('column', '')
    tag = request.GET.get('tag', '')

    articles = Article.objects.all()

    if search:
        q = Q(title__icontains=search) | Q(body__icontains=search)
        articles = articles.filter(q)

    order_list = ['total_visit', 'total_comment']
    if order in order_list:
        if order == 'total_visit':
            articles = articles.order_by('-total_visit')
        if order == 'total_comment':
            articles = articles.order_by('-total_comment')

    if column:
        articles = articles.filter(column__title=column)

    if tag:
        articles = articles.filter(tags__name__in=[tag])  # tags__in 会按照主键找tag

    page, page_list = custom_paginator(request, queryset=articles, per_page=6)
    articles = page

    # comment_count 评论计数 待补充

    data = {
        'articles': articles,  # 匹配的文章
        'page_list': page_list,  # 分页列表
        'order': order,  # 排序参数
        'search': search,  # 查询参数
        'column': column,  # 专栏
        'tag': tag,  # 标签
    }
    return render(request, 'article/list.html', data)


def article_detail(request, pk):
    article = Article.objects.filter(pk=pk).first()

    article.total_visit += 1
    article.save(update_fields=['total_visit'])

    # article.body = markdown.markdown(
    #     text=article.body,
    #     extensions=[
    #         # 包含 缩写、表格等常用扩展
    #         'markdown.extensions.extra',
    #         # 语法高亮扩展
    #         'markdown.extensions.codehilite',
    #         # 目录拓展
    #         'markdown.extensions.toc',
    #     ]
    # )

    md = markdown.Markdown(
        extensions=[
            # # 包含 缩写、表格等常用扩展
            # 'markdown.extensions.extra',
            # # 语法高亮扩展
            # 'markdown.extensions.codehilite',
            # # 自动生成目录
            # 'markdown.extensions.toc',
            'markdown.extensions.extra',
            'markdown.extensions.abbr',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.footnotes',
            'markdown.extensions.md_in_html',
            'markdown.extensions.tables',
            'markdown.extensions.admonition',
            'markdown.extensions.codehilite',
            'markdown.extensions.legacy_attrs',
            'markdown.extensions.legacy_em',
            'markdown.extensions.meta',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
            'markdown.extensions.smarty',
            'markdown.extensions.toc',
            'markdown.extensions.wikilinks'
        ]
    )
    article.body = md.convert(article.body)
    # 约束图片大小
    article.body = article.body.replace('<img alt="" src=', '<img alt="" style="width: 80%;" src=')
    # 添加段落间隔
    article.body = article.body.replace('/></p>', '/></p></br>')

    comments = Comment.objects.filter(article_id=pk)
    comment_form = CommentForm()

    data = {
        'article': article,
        'md': md,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'article/detail.html', data)


@login_required(login_url='/user/login/')
def article_create(request):
    if request.method == 'GET':
        form = ArticleForm()
        data = {
            'form': form
        }
        return render(request, 'article/create.html', data)
    form = ArticleForm(data=request.POST)
    if form.is_valid():
        # form.save()  # form中没有作者信息，以登录用户作为文章的作者
        temp_form = form.save(commit=False)
        temp_form.author = User.objects.get(pk=request.user.pk)
        temp_form.save()
        return redirect('article:article_list')
    print(form.data)
    return HttpResponse('403 forbidden')


@login_required(login_url='/user/login/')
def article_delete(request, pk):
    if request.method == 'POST':
        article = Article.objects.filter(pk=pk).first()

        if request.user.pk != article.author.pk:  # 登录用户 不是 文章作者时
            return HttpResponse('not author,without force')

        article.delete()
        return redirect('article:article_list')
    return HttpResponse('403 forbidden')


@login_required(login_url='/user/login/')
def article_update(request, pk):
    article = Article.objects.filter(pk=pk).first()
    if request.method == 'GET':
        form = ArticleForm(instance=article)
        data = {
            'form': form
        }
        return render(request, 'article/update.html', data)

    form = ArticleForm(data=request.POST, instance=article)

    if request.user.pk != article.author.pk:  # 登录用户 不是 文章作者时
        return HttpResponse('not author,without force')

    if form.is_valid():
        form.save()
        return redirect('article:article_detail', pk=pk)
    return HttpResponse('403 forbidden')
