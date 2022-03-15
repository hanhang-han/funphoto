from django import forms
from captcha.fields import CaptchaField

class UserInfoForm(forms.Form):
    sex_choice = (
        ('1', '男'),
        ('2', '女')
    )
    username = forms.CharField(max_length=50, label='用户名')
    password = forms.CharField(max_length=200, label='密码')
    sex = forms.ChoiceField(choices=sex_choice,label='性别')
    age = forms.IntegerField(label='年龄')
    email = forms.EmailField(label='电子邮箱', max_length=50)
    phone = forms.IntegerField(label='电话')
    captcha = CaptchaField(label='验证码')
    phonecode = forms.IntegerField(label='短信验证码')