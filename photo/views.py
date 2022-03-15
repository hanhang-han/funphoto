from django.conf.global_settings import SECRET_KEY
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
import hashlib
from .models import *
# Create your views here.
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