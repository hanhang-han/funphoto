import random

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.db.models import F
from django_redis import get_redis_connection

from photo.models import Photo, UserInfo


def code():
    a = ''
    for x in range(4):
        a += str(random.randint(0, 9))
    return a

import redis

def get_redis():
    """
    获取 Redis 的连接
    """
    pool = get_redis_connection('default').connection_pool
    r = redis.Redis(connection_pool=pool)
    return r

def gencaptcha():
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    cap = {'hashkey': hashkey, 'image_url': image_url}
    return cap

def val_captcha(captchastr,captchakey):
    if captchastr.lower() == CaptchaStore.objects.get(hashkey=captchakey).response:
        return True
    else:return False

def hot_add(request,userid,photoid):
    user_weight = request.session.get('weight')
    if not user_weight:
        user_weight_f = UserInfo.objects.filter(id=userid).values('weight')
        print(user_weight_f)
        print(user_weight_f[0]['weight'])
        user_weight = user_weight_f[0]['weight']/100
        request.session['weight'] = user_weight
    Photo.objects.filter(id=photoid).update(hot = F('hot') + user_weight)
    return 'done'