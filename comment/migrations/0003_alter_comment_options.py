# Generated by Django 4.1.6 on 2023-05-23 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_alter_comment_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created'], 'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
    ]
