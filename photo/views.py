import json
import os
import pika


from django.conf.global_settings import SECRET_KEY
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection
from notifications.signals import notify

from .forms import *
import hashlib
from .models import *
from django.core.cache import cache
from .utils import task
from .utils.utils import code, get_redis, gencaptcha, val_captcha, hot_add

message = ''
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='register_list')


def login_check(func):
    def wrapper(req):
        if req.session.get('is_login'):
            return func(req)
        else:
            return redirect('/')  # 用于记录访问历史页面，便于登录后跳转

    return wrapper

def register(request):
    if request.method == 'GET':
        global message
        global channel
        u = UserInfoForm()
        captcha = gencaptcha()
        dic = {
            'u':u,
            'message':message,
            'captcha':captcha,
        }
        return render(request, 'register111.html',dic)
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        password += SECRET_KEY
        passhash = hashlib.sha256(password.encode()).hexdigest()
        sex = request.POST.get('sex')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        phonecode = request.POST.get('phonecode')
        cache.set(phone, phonecode, 60)
        p_c = cache.get(phone)
        if p_c == phonecode:
            UserInfo.objects.create(username=user, password=passhash, sex=sex, email=email, phone=phone,
                                    phonecode=p_c)
            channel.basic_publish(exchange='',routing_key='register_list',body=user)
            connection.close()
        else:
            return HttpResponse('验证码错误')
        return redirect('/')

def refresh_captcha(request):
    return HttpResponse(json.dumps(gencaptcha()), content_type='application/json')

def register_code(request):
    if request.method == 'POST':
        global message
        phone = request.POST.get('phone')
        if not val_captcha(request.POST.get('captcha'),request.POST.get('hashkey')):
            message = '验证码错误'
            return redirect('/register/')
        if cache.has_key(phone):
            message = '请稍后重新发送'
            return redirect('/register/')
        phonecode = code()
        print(phone,phonecode)

        task.send_sms_task.apply_async(args=[phone, phonecode])
        task.add.apply_async(args=[3,7])
        cache.set(phone, phonecode, 60)
        print(cache.get(phone))
        message = '短信验证码已发送'
        print(message)
        return redirect('/register/')

def login(request):
    if request.method == 'GET':
        u = UserInfoForm()
        if request.session.get('is_login'):
            return redirect('/index/')
        else:
            return render(request, 'login.html', locals())
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:
            try:
                user = UserInfo.objects.get(username=username)
            except:
                return redirect('/register/')
            print(username, hashlib.sha256(password.encode()).hexdigest())
            if user.password == hashlib.sha256(password.encode()).hexdigest():
                request.session['is_login'] = True
                request.session['username'] = user.username
                request.session['id'] = user.id
                request.session.set_expiry(60 * 60)
                return redirect('/')

@login_check
def logout(request):
    request.session.flush()
    return redirect('/')

@login_check
def index(request):
    username = request.session.get('username')
    r = get_redis()
    userid = request.session.get('id')
    r_id = '%s_like_times' % userid
    times = r.get(r_id)
    if not times:
        times = r.set(r_id, 0)
        r.expire(r_id, 60 * 2)
    times = int(times)
    photo = Photo.objects.filter(delete=False).all().order_by('showtimes','uploadtime')
    a = 0
    r_pic = '%s_showed_pic_id'%userid
    while r.sismember(r_pic,photo[a].id):
        a += 1
    r.sadd(r_pic,photo[a].id)
    r.expire(r_pic,60)
    print(a)
    print(r.smembers(r_pic))
    photos = [photo[a], photo[a+3]]
    id_list = [photo[a].id,photo[a+3].id]
    Photo.objects.filter(id__in=id_list).update(showtimes=F('showtimes')+1)
    ranks = rankboard(request)
    return render(request, 'index.html', locals())
result = None

@login_check
def ownspace(request):
    if result:
        # print(result)
        result.forget()
    username = request.session.get('username')
    photos = Photo.objects.filter(owner__username=username, delete=False)
    for photo in photos:
        if not photo.thumbimage:
            print('D:/Image/'+str(photo.image))
            task.thumb_made.apply_async(args=['D:/Image/'+str(photo.image),])
            photo.thumbimage='_thumb.'.join(str(photo.image).rsplit('.'))
            photo.save()
    return render(request, 'ownspace.html', locals())

@login_check
def uploadphoto(request):
    global result
    if request.method == 'POST':
        userid = request.session.get('id')
        username = request.session.get('username')
        photo = request.FILES['photo']
        photoname = photo.name
        dir = "D:/Image/%s" % username
        if not os.path.exists(dir):
            os.makedirs(dir)
        image_path = "%s/%s" % (username, photoname)
        thumb_path = '_thumb.'.join(image_path.rsplit('.'))
        result = task.thumb_made.apply_async(args=[dir + '/%s' % photoname,])
        with open(dir + '/%s' % photoname, 'wb') as f:
            for content in photo.chunks():
                f.write(content)
        new_img = Photo(
            image=image_path,  # 拿到图片
            name=photoname,  # 拿到图片的名字
            downloadtimes=0,
            owner_id=userid,
            thumbimage=thumb_path
        )
        new_img.save()  # 保存图片
        return redirect('/ownspace/')
    else:
        return render(request, 'upload.html')

def delete(request, photoid):
    Photo.objects.filter(id=photoid).update(delete=True)
    return redirect('/ownspace/')

# @login_check
def like(request, photoid):
    if request.method == 'GET':
        r = get_redis()
        r_id = '%s_like_times' % request.session.get('id')
        times = r.get(r_id)
        if int(times) > 10:
            return HttpResponse('您今天点赞超过三十次，24小时后继续')
        r.incr('%s_like_times' % request.session.get('id'), 1)
        Photo.objects.filter(id=photoid).all().update(likenum=F('likenum') + 1)
        photo = Photo.objects.filter(id=photoid).first()
        user_id = request.session.get('id')
        hot_add(request,user_id,photoid)
        user = UserInfo.objects.get(id=user_id)
        reciver = UserInfo.objects.get(owner__id=photoid)
        print(type(reciver))
        notify.send(
            user,
            recipient=reciver,
            verb='点赞了',
            target=photo,
        )
        photo.liker.add(user)
        return redirect('/index/')

def mynotifications(request):
    user = UserInfo.objects.get(id = request.session['id'])
    note_read = user.notifications.read()
    note_unread = user.notifications.unread()
    return render(request,'mynotifitions.html',locals())

def change_unread(request):
    notice_id = request.GET.get('notice_id')
    if notice_id:
        user = UserInfo.objects.get(id=request.session['id'])
        user.notifications.get(id=notice_id).mark_as_read()
        return redirect("photo:mynotifications")
    else:
        user = UserInfo.objects.get(id=request.session['id'])
        user.notifications.mark_all_as_read()
        return redirect("photo:mynotifications")
def change_read(request):
    notice_id = request.GET.get('notice_id')
    if notice_id:
        user = UserInfo.objects.get(id=request.session['id'])
        user.notifications.filter(id=notice_id).mark_all_as_deleted()
        return redirect("photo:mynotifications")
    else:
        user = UserInfo.objects.get(id=request.session['id'])
        user.notifications.mark_all_as_deleted()
        return redirect("photo:mynotifications")

# @login_check
def dislike(request, photoid):
    Photo.objects.filter(id=photoid).all().update(likenum=F('likenum') - 1)
    photo = Photo.objects.filter(id=photoid).first()
    user_id = request.session.get('id')
    user = UserInfo.objects.get(id=user_id)
    photo.liker.remove(user)
    return redirect('/index/')

def mylike(request):
    user_id = request.session.get('id')
    user = UserInfo.objects.get(id=user_id)
    photos = user.liker.filter(delete=False).all()
    return render(request, 'mylike.html', locals())

def rankboard(request):
    r = get_redis()
    tops = r.zrevrange("rankboard", 0, 3, withscores=True)
    if tops:
        photos = Photo.objects.filter(id__in=[int(item[0]) for item in tops]).all()
        for photo in photos:
            print(photo.name, photo.hot)
    else:
        photos = Photo.objects.all().order_by('-hot')[:3]
        for photo in photos:
            r.zadd('rankboard', photo.id, photo.likenum)
        r.expire('rankboard', 60 * 30)
    return photos
