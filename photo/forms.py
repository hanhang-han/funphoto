from django import forms
from captcha.fields import CaptchaField

class UserInfoForm(forms.Form):
    sex_choice = (
        ('1', '男'),
        ('2', '女')
    )
    username = forms.CharField(max_length=50, label='用户名',required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=200, label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(choices=sex_choice,label='性别',
                            )
    age = forms.IntegerField(label='年龄',
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='电子邮箱', max_length=50,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label='电话',
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # captcha = CaptchaField(label='验证码',)
    #                        # widget=forms.TextInput(attrs={'class': 'form-control'}))
    phonecode = forms.IntegerField(label='短信验证码',
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))