from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect
from backweb.models import Admin, Article, Comment
from django.urls import reverse
from backweb.Artform import AddArtForm, UpdatePwd

# Create your views here.


def index(request):
    # 首页
    if request.method == 'GET':
        admin = request.admin
        articles = Article.objects.all()
        p = Paginator(articles, 5)
        return render(request, 'backweb/index.html', {'admin': admin, 'p': p})


def login(request):
    # 登陆
    if request.method == 'GET':
        return render(request, 'backweb/login.html')
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('userpwd')
        admin = Admin.objects.filter(user=user, userpassword=password).first()
        if admin:
            request.session['admin_id'] = admin.id
            res = HttpResponseRedirect(reverse('back:index'))
            return res
        else:
            err_name_pwd = '用户名或密码错误！'
            return render(request, 'backweb/login.html', {'err_name_pwd': err_name_pwd})


def add_user(request):
    if request.method == 'GET':
        return render(request, 'backweb/manage-user.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        user = request.POST.get('user')
        phone = request.POST.get('phone')
        mail = request.POST.get('mail')
        user_password = request.POST.get('password')
        Admin.objects.create(username=username, user=user, phone=phone, mail=mail, user_password=user_password)
        return render(request, 'backweb/manage-user.html')


def logout(request):
    # 注销
    del request.session['admin_id']
    return HttpResponseRedirect('/login/')


def update_pwd(request, id):
    if request.method == 'GET':
        return render(request, 'backweb/index.html')
    if request.method == 'POST':
        form = UpdatePwd(request.POST)
        if form.is_valid():
            admin = Admin.objects.filter(pk=id).first()
            username = form.cleaned_data['username']
            user = form.cleaned_data['user']
            phone = form.cleaned_data['phone']
            userpassword = form.cleaned_data['userpassword']
            new_one_password = form.cleaned_data['new_one_password']
            new_tow_password = form.cleaned_data['new_tow_password']
            if new_one_password == new_tow_password:
                admin.username = username
                admin.user = user
                admin.phone = phone
                admin.userpassword = userpassword
                admin.save()
            else:
                return render(request, 'backweb/index.html', {'err': '两次密码不一致'})
        else:
            return render(request, 'backweb/index.html', {'form': form})


def article(request):
    # 显示页面
    if request.method == 'GET':
        admin = request.admin
        page = int(request.GET.get('page', 1))
        articles = Article.objects.all()
        paginator = Paginator(articles, 5)
        page = paginator.page(page)
        return render(request, 'backweb/article.html', {'admin': admin, 'page': page})


def add_article(request):
    # 创建文章
    admin = request.admin
    if request.method == 'GET':
        return render(request, 'backweb/add-article.html', {'admin': admin})
    if request.method == 'POST':
        form = AddArtForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            content = form.cleaned_data['content']
            icon = form.cleaned_data['icon']
            keywords = form.cleaned_data['keywords']
            blogger = form.cleaned_data['blogger']
            publish = form.cleaned_data['publish']
            Article.objects.create(
                title=title, desc=desc, content=content, icon=icon, keywords=keywords, blogger=blogger, publish=publish
            )
            # 创建文章返回列表页面
            return HttpResponseRedirect(reverse('back:article'))
        else:
            return render(request, 'backweb/add-article.html', {'form': form, 'admin': admin})


def update_article(request, id):
    #  修改文章
    admin = request.admin
    article = Article.objects.filter(pk=id).first()
    if request.method == 'GET':
        return render(request, 'backweb/add-article.html', {'article': article, 'admin': admin})
    if request.method == 'POST':
        form = AddArtForm(request.POST, request.FILES)
        if form.is_valid():
            # 验证成功
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            content = form.cleaned_data['content']
            icon = form.cleaned_data['icon']
            keywords = form.cleaned_data['keywords']
            blogger = form.cleaned_data['blogger']
            publish = form.cleaned_data['publish']
            article.title = title
            article.desc = desc
            article.content = content
            article.blogger = blogger
            if publish:
                publish = 1
            else:
                publish = 0
            article.publish = publish
            if icon:
                article.icon = icon
            article.keywords = keywords
            article.save()
            return HttpResponseRedirect(reverse('back:article'))
        else:
            # 验证失败
            return render(request, 'backweb/add-article.html', {'form': form, 'article': article, 'admin': admin})


def delete_article(request, id):
    # 删除文章
    if request.method == 'GET':
        Article.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('back:article'))


def delete_all(request):
    # 删除全部文章
    if request.method == 'GET':
        pass


def manage_admin(request):
    # 用户管理
    admin = request.admin
    if request.method == 'GET':
        admins = Admin.objects.all()
        return render(request, 'backweb/manage-user.html', {'admin': admin, 'admins': admins})


def comment(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        comment = Comment.objects.all()
        paginator = Paginator(comment, 5)
        page = paginator.page(page)
        return render(request, 'backweb/comment.html', {'pages': page})


def add_comment(request):
    if request.method == 'GET':
        return render(request, 'backweb/comment.html')
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        id = int(request.POST.get('article_id'))
        article = Article.objects.filter(pk=id).first()
        admin = Admin.objects.filter(user=user, userpassword=password).first()
        if admin:
            content = request.POST.get('comment_text')
            Comment.objects.create(content=content, comment_admin=admin, comment_article=article)
            return HttpResponseRedirect(reverse('back:comment'))
        else:
            error = '用户名或密码错误！'
            return render(request, 'web/info.html', {'error': error})
