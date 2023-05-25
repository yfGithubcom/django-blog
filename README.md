# django-blog
### 一个简易的博客系统，使用django框架，实现用户注册，登录，注销和个人信息修改，及文章的增删改查和评论功能，同时对权限进行限制，保证文章只能被作者删除和修改，发表文章和评论需要先登录等。

数据库默认sqlite

使用前你需要pip install的有

pygmentize（这个可以不用下载，样式已经保存到static里了）

markdown

taggit

ckeditor

mdeditor


sql里注册的超级管理员账号：root，密码：root

邮箱找回密码得先开启邮箱的smpt，

然后到user/views.py里找到verif_with_mail()

把注释的username（邮箱名）和password（邮箱密钥）补上即可
