from photo.utils.celery_app import app
from photo.utils.yunpian import YunPian
API_KEY='srdwqewqe'

@app.task
def send_sms_task(phone_code,mobile):
    a = YunPian(API_KEY)
    a.send_sms(phone_code, mobile)