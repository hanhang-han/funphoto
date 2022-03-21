from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register((UserInfo,Photo))
admin.site.site_header = 'funphoto后台页面'
admin.site.site_titler = 'funphoto后台页面'