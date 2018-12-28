
from django.conf.urls import url

from web import views

urlpatterns = [
    # 首页
    url(r'^index/', views.index, name='index'),
    # 博客内容
    url(r'^info/(\d+)', views.info, name='info'),
]
