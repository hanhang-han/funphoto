BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKED = 'redis://127.0.0.1:6379/0'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_IMPORT = (
    'celery_app.task'
)