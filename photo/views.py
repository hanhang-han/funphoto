from django.conf.global_settings import SECRET_KEY
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection

from .forms import *
import hashlib
from .models import *
from django.core.cache import cache
from .utils.celery_app.task import send_sms_task
from .utils.utils import code

def register(request):
    if request.method == 'GET':
        u = UserInfoForm()
        return render(request,'register.html',locals())
    if request.method == 'POST':
        u = UserInfoForm(request.POST)
        user = request.POST.get('username')
        password = request.POST.get('password')
        password += SECRET_KEY
        passhash = hashlib.sha256(password.encode()).hexdigest()
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        phonecode = request.POST.get('phonecode')
        p_c = cache.get(phone)
        if p_c == phonecode:
            UserInfo.objects.create(username=user,password=passhash,sex=sex,age=age,email=email,phone=phone,phonecode=p_c)
        else:
            return HttpResponse('验证码错误')
        return render(request,'register.html',locals())

def register_code(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if cache.has_key(phone):
            return JsonResponse({'data':'稍后重新发送'})
        phonecode = code()
        send_sms_task.add.apply_async(args=[phone,phonecode])
        cache.set(phone,phonecode)
        return JsonResponse({'data': '验证码发送成功'})