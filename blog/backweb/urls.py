
from django.conf.urls import url

from backweb import views

urlpatterns = [
    # 首页
    url(r'^index/', views.index, name='index'),
    # 登陆
    url(r'^login/', views.login, name='login'),
    # 添加用户
    url(r'^add_user', views.add_user, name='add_user'),
    # 注销
    url(r'^logout/', views.logout, name='logout'),
    # 修改密码
    url(r'^update_pwd/(\d+)', views.update_pwd, name='update_pwd'),
    # 管理用户
    url(r'^manage_admin/', views.manage_admin, name='manage_admin'),
    # 后台系统首页
    url(r'^article/', views.article, name='article'),
    # 增加文章
    url(r'^add_article/', views.add_article, name='add_article'),
    # 修改文章
    url(r'^update_article/(\d+)/', views.update_article, name='update_article'),
    # 删除文章
    url(r'^delete_article/(\d+)/', views.delete_article, name='delete_article'),
    # 删除全部文章
    url(r'^delete_all/', views.delete_all, name='delete_all'),
    # 评论首页
    url(r'^comment/', views.comment, name='comment'),
    # 添加评论
    url(r'^add_comment/', views.add_comment, name='add_comment'),
]
