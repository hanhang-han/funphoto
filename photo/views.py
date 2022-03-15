from django.conf.global_settings import SECRET_KEY
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
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
        user = request.POST.get('username')
        password = request.POST.get('password')
        password += SECRET_KEY
        passhash = hashlib.sha256(password.encode()).hexdigest()
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        phonecode = request.POST.get('phonecode')
        conn = get_redis_connection('default')
        cache.set(phone, phonecode, 60)
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
        cache.set(phone,phonecode,60)
        return JsonResponse({'data': '验证码发送成功'})

def login(request):
    if request.method == 'GET':
        u = UserInfoForm()
        return render(request,'login.html',locals())
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:  # 确保用户名和密码都不为空
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = UserInfo.objects.get(username=username)
            except:
                return redirect('/register/')
            if user.password == hashlib.sha256(password.encode()).hexdigest():
                return redirect('/index/')
    return redirect('/register/')