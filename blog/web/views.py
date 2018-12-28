from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from backweb.models import Article, Admin, Comment

# Create your views here.


def index(request):
    # 文章目录显示
    if request.method == 'GET':
        admin = Admin.objects.all().first()
        page = int(request.GET.get('page', 1))
        article = Article.objects.filter(publish=1)
        paginator = Paginator(article, 14)
        page = paginator.page(page)
        return render(request, 'web/index.html', {'admin': admin, 'pages': page})


def info(request, id):
    # 文章内容
    if request.method == 'GET':
        article = Article.objects.filter(pk=id).first()
        comment = Comment.objects.filter(comment_article=id)
        return render(request, 'web/info.html', {'article': article, 'comments': comment})

