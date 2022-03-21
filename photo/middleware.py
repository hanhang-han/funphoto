import time

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from photo.utils.utils import get_redis


class IPCheckMiddleware(MiddlewareMixin):
    def process_request(self,request):
        ip = request.META.get("REMOTE_ADDR")
        r = get_redis()
        time_pre = r.get(ip)
        if not time_pre:
            time_pre = time.time()
            r.set(ip,time_pre,ex=60)
        else:
            time_now = time.time()
            time_check = time_now - float(time_pre)
            time_check_p="{:.2f}".format(time_check)
            r.set(ip,time_now,ex=60)
            # print(time_check_p)
            if time_check < 0.1:
                return HttpResponse('访问过于频繁')
    # def process_view(self,request,view_func,view_args,view_kwargs):
    #     print('开始处理函数')