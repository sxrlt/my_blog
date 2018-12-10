
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, HttpResponseRedirect
from backweb.models import Admin
import time
import logging

log = logging.getLogger(__name__)


class LoginMiddleware(MiddlewareMixin):
    # 设置中间件
    def process_request(self, request):
        # 绑定在request上的init_time属性，表示访问的时间
        request.init_time = time.time()
        if request.path[1:4] == 'web' or request.path[1:4] == 'media':
            return None
        if request.path in ['/backweb/login/']:
            return None
        # 获取session中admin_id值
        admin_id = request.session.get('admin_id')
        if admin_id:
            admin = Admin.objects.get(pk=admin_id)
            request.admin = admin
            return None
        else:
            return HttpResponseRedirect('/backweb/login/')

    def process_response(self, request, response):
        # 请求URL访问到结束的 耗时时间
        count_time = time.time() - request.init_time
        # 获取响应状态码
        code = response.status_code
        # 获取请求地址
        path = request.path
        # 获取请求方法
        method = request.method
        # 获取响应内容
        try:
            content = response.content
        except:
            content = ''
        # 写入日志文件内容
        log_str = '%s %s %s %s %s' % (path, method, code, count_time, content)
        # 交给logger处理日志
        log.info(log_str)
        return response