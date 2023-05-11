from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm, PwdResetForm, UserProfileForm
from .models import UserProfile


# Create your views here.

def user_login(request):
    if request.method == 'GET':
        form = UserLoginForm()
        data = {'form': form}
        return render(request, 'user/login.html', data)
    form = UserLoginForm(data=request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)  # 将用户数据保存在 session 中
            return redirect('article:article_list')
        form.add_error('password', '用户名不存在或密码错误')
        return render(request, 'user/login.html', {'form': form})
    return HttpResponse('内容不合法')


def user_logout(request):
    logout(request)  # session.clear()
    return redirect('article:article_list')


def user_register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        data = {'form': form}
        return render(request, 'user/register.html', data)
    form = UserRegisterForm(data=request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        data = form.cleaned_data
        user.set_password(data['password_confirm'])
        user.save()
        # 注册完成后返回博客列表页
        login(request, user)
        return redirect('article:article_list')
    return render(request, 'user/register.html', {'form': form})


@login_required(login_url='/user/login/')
def user_delete(request, pk):
    if request.method == 'POST':
        user = User.objects.filter(pk=pk).first()
        if request.user == user:  # 登录用户和待销号用户相同
            logout(request)
            user.delete()
            return redirect('article:article_list')
        else:
            return HttpResponse('无权限注销')
    return HttpResponse('销号仅支持post请求')


@login_required(login_url='/user/login/')
def pwd_reset(request, pk):
    user = User.objects.filter(pk=pk).first()
    if request.method == 'GET':
        form = PwdResetForm(instance=user)
        data = {'form': form}
        return render(request, 'user/pwd_reset.html', data)
    form = PwdResetForm(data=request.POST, instance=user)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            pwd = form.save(commit=False)
            pwd.set_password(data['new_password_confirm'])
            pwd.save()
            return redirect('article:article_list')
        # 旧密码未通过校验
        form.add_error('password', '请输入正确的密码')
        return render(request, 'user/pwd_reset.html', {'form': form})
    # 新密码未通过校验
    # forms.py中已经设置校验，故注释掉下一行
    # form.add_error('new_password_confirm', '两次密码不一致，请重新输入')
    return render(request, 'user/pwd_reset.html', {'form': form})


@login_required(login_url='/user/login/')
def userprofile_edit(request, pk):
    user = User.objects.filter(pk=pk).first()
    userprofile = UserProfile.objects.filter(user_id=pk).first()
    if not userprofile:  # 不存在userprofile就创建
        userprofile = UserProfile.objects.create(user=user)
    if request.method == 'GET':
        form = UserProfileForm(instance=userprofile)
        data = {
            'form': form,
            'user': user,
            'userprofile': userprofile,
        }
        return render(request, 'userprofile/edit.html', data)
    # 发送请求的用户为登录用户本人
    if request.user == user:
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=userprofile)
        if form.is_valid():
            data = form.cleaned_data
            userprofile.phone = data['phone']
            if 'avatar' in request.FILES:
                userprofile.avatar = data['avatar']
            userprofile.biography = data['biography']
            form.save()
        return redirect('user:userprofile_edit', pk=pk)
    return HttpResponse('您不具有修改权限')
