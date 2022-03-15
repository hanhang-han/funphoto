from django.conf.global_settings import SECRET_KEY
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import *
import hashlib
from .models import *
# Create your views here.
from .utils.celery_app.task import send_sms_task
from .utils.utils import code
def register(request):
    if request.method == 'GET':
        u = UserInfoForm()
        return render(request,'register.html',locals())
    if request.method == 'POST':
        u = UserInfoForm(request.POST)
        if u.is_valid():
            user = request.POST.get('username')
            password = request.POST.get('password')
            password += SECRET_KEY
            passhash = hashlib.sha256(password.encode()).hexdigest()
            sex = request.POST.get('sex')
            age = request.POST.get('age')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            UserInfo.objects.create(username=user,password=passhash,sex=sex,age=age,email=email,phone=phone)

            # UserInfo.objects.create(username=u.cleaned_data.get('username'),sex=u.sex,password=passhash,age=u.age,email=u.email,phone=u.phone)
        else:
            return HttpResponse('错误')
        return render(request,'register.html',locals())



def register_code(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        phone_code = code()
        send_sms_task.add.apply_async(args=[mobile,phone_code])
        try:
            check_code = UserInfo.objects.get(phone=mobile)
            check_code.phone_code = phone_code
            check_code.save()
        except:
            print(phone_code, mobile, 1111111111)
            check_code = UserInfo(phone_code=phone_code, phone=mobile)
            check_code.save()
        return JsonResponse({'data': '验证码发送成功'})