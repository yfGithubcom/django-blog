from django import forms
from django.contrib.auth.models import User
from . import models


class MyForm(forms.Form):
    excludes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name not in self.excludes:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label
                }
            else:
                field.widget.attrs = {}


class MyModelForm(forms.ModelForm):
    readonly = []  # readonly_fields
    excludes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name in self.excludes:
                field.widget.attrs = {}
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label

        # for field in self.readonly:  # 只读不可编辑的表单字段
        #     self.fields[field].widget.attrs['readonly'] = True

        for name, field in self.fields.items():
            if name in self.readonly:
                field.widget.attrs['readonly'] = 'True'


class UserLoginForm(MyForm):
    username = forms.CharField(label='昵称', widget=forms.TextInput, required=True)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)


class UserRegisterForm(MyModelForm):
    password = forms.CharField(label='设置密码', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    class Meta:
        model = User  # 继承django自带的User字段
        fields = ['username', 'email', ]
        labels = {'username': '昵称', 'email': '邮箱'}
        widgets = {
            'username': forms.TextInput,
            'email': forms.EmailInput,
        }

    def clean_password_confirm(self):
        data = self.cleaned_data
        pwd = data.get('password')
        pwd_confirm = data.get('password_confirm')
        if pwd == pwd_confirm:
            return pwd_confirm
        else:
            raise forms.ValidationError('两次密码不一致，请重新输入')


class PwdResetForm(MyModelForm):
    readonly = ['username', ]
    new_password = forms.CharField(label='输入新密码', widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(label='确认新密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', ]
        labels = {'username': '昵称', 'password': '输入旧密码'}
        widgets = {
            'username': forms.TextInput,
            'password': forms.PasswordInput,
        }

    def clean_new_password_confirm(self):
        data = self.cleaned_data
        new_pwd = data.get('new_password')
        new_pwd_confirm = data.get('new_password_confirm')
        if new_pwd == new_pwd_confirm:
            return new_pwd_confirm
        else:
            raise forms.ValidationError('两次密码不一致，请重新输入')


class UserProfileForm(MyModelForm):
    excludes = ['avatar']
    readonly = ['user']

    class Meta:
        model = models.UserProfile
        fields = ['user', 'phone', 'email', 'avatar', 'biography', ]
        labels = {'user': 'uid', 'phone': '手机号', 'email': '邮箱', 'avatar': '更换头像', 'biography': '个人简介'}
        widgets = {
            'user': forms.TextInput,
            'phone': forms.TextInput,
            'email': forms.EmailInput,
            'avatar': forms.FileInput,
            'biography': forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for field_name in self.base_fields:
        #     field = self.base_fields[field_name]
        #     field.widget.attrs.update()


class VerifWithMailForm(MyForm):
    username = forms.CharField(label='昵称', widget=forms.TextInput, required=True)
    email = forms.CharField(label='邮箱', widget=forms.EmailInput)


class ResetWithMailForm(MyModelForm):
    readonly = ['username', 'email']
    new_password = forms.CharField(label='输入新密码', widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(label='确认新密码', widget=forms.PasswordInput)
    captcha = forms.CharField(label='邮件验证码', widget=forms.TextInput)

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': '昵称', 'email': '邮箱'}
        widgets = {
            'username': forms.TextInput,
            'email': forms.EmailInput,
        }

    def clean_new_password_confirm(self):
        data = self.cleaned_data
        new_pwd = data.get('new_password')
        new_pwd_confirm = data.get('new_password_confirm')
        if new_pwd == new_pwd_confirm:
            return new_pwd_confirm
        else:
            raise forms.ValidationError('两次密码不一致，请重新输入')
