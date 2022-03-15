from celery import Celery

from photo.utils.celery_app import celeryconfig

app = Celery('demo')
app.config_from_object(celeryconfig)