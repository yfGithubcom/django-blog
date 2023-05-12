from django import forms
from . import models


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'column', 'body']  # 'author',
        widgets = {
            # 'author': forms.TextInput,
            'title': forms.TextInput,
            'body': forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'body':
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label, 'rows': '16'}
