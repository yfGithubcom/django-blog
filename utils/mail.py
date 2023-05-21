import os
import django
from django.core.mail import get_connection, send_mail

"""
防止报错
django.core.exceptions.ImproperlyConfigured: 
Requested setting EMAIL_BACKEND, 
but settings are not configured. 
You must either define the environment variable DJANGO_SETTINGS_MODULE 
or call settings.configure() before accessing settings.

若仍报错
django.core.exceptions.ImproperlyConfigured: 
Requested setting LOGGING_CONFIG, 
but settings are not configured. 
You must either define the environment variable DJANGO_SETTINGS_MODULE 
or call settings.configure() before accessing settings.
需要右击该文件，选择Modify Run Configuration...
在环境变量中添加 DJANGO_SETTING_MODULE=BlogSystem.settings
记得用 ; 隔开
"""
os.environ.setdefault('DJANGO_SETTING_MODULE', 'BlogSystem.settings')
django.setup()


def custom_mail(host, username, password, subject, message, recipient_list):
    conn = get_connection(
        host=host,
        username=username,
        password=password,
    )

    if conn:
        send_mail(
            subject=subject,
            message=message,
            from_email=username,
            recipient_list=recipient_list,
            connection=conn,
            html_message=False,
        )
        return True
    return False


if __name__ == '__main__':

    try:

        # 配置你的发件邮箱
        # host = '' 如smtp.qq.com
        # username = 'your@example.com'
        # password = ''

        # 配置邮件等信息
        # subject = '标题'
        # message = '内容'
        # from_email = username
        # recipient_list = [
        #     'receiver@example.com'
        # ]

        mail = custom_mail(
            host='smtp.qq.com',
            username='',
            password='',

            subject='title',
            message='content',
            recipient_list=[
                '',
            ],
        )
        print(mail)

    except Exception as e:
        print(e)
