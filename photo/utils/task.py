# from photo.utils.celery_app import app
from .yunpian import YunPian
from PIL import Image

API_KEY='srdwqewqe'

import time
from celery import Celery

broker = 'redis://127.0.0.1:6379'
backend = 'redis://127.0.0.1:6379/0'

app = Celery('my_task', broker=broker, backend=backend)

@app.task(name='add')
def add(x, y):
    time.sleep(5)     # 模拟耗时操作
    return x + y


@app.task(name='send_sms_task')
def send_sms_task(phone_code,mobile):
    a = YunPian(API_KEY)
    a.send_sms(phone_code, mobile)
    return 'finished'
@app.task(name='thumb_made')
def thumb_made(image_url):
    im = Image.open(image_url)
    im.thumbnail((200,100))
    thumb_url ='_thumb.'.join(image_url.rsplit('.'))
    im.save(thumb_url)
    return 'finsihed'