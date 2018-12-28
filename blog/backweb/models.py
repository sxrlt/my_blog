from django.db import models

# Create your models here.


class Admin(models.Model):
    user = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=20)
    sex = models.BooleanField(default=1)
    userpassword = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    mail = models.EmailField(max_length=20)

    class Meta:
        db_table = 'admin'


class Article(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=150)
    content = models.TextField()
    icon = models.ImageField(upload_to='article', null=True)
    keywords = models.CharField(max_length=10)
    blogger = models.CharField(max_length=10, null=True)
    publish = models.BooleanField(default=1)
    Publisher = models.ForeignKey(Admin, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article'


class Comment(models.Model):
    content = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    comment_article = models.ForeignKey(Article, null=True)
    comment_admin = models.ForeignKey(Admin, null=True)

    class Meta:
        db_table = 'comment'
