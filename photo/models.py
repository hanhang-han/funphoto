from django.db import models

# Create your models here.
class UserInfo(models.Model):
    sex_choice = (
        ('1','男'),
        ('2','女')
    )
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50,verbose_name='用户名')
    password = models.CharField(max_length=200,verbose_name='密码')
    sex = models.CharField(choices=sex_choice,default='男',max_length=20)
    age = models.IntegerField(verbose_name='年龄')
    email = models.EmailField(verbose_name='电子邮箱',max_length=50)
    phone = models.IntegerField(verbose_name='电话',unique=True)
    lastlogintime = models.DateTimeField(verbose_name='上次登录时间',blank=True,null=True)
    registertime = models.DateTimeField(verbose_name='注册时间',auto_now=True)
    phonecode = models.IntegerField(verbose_name='短信验证码',null=True)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name='用户表'
        verbose_name_plural='用户表'
class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(verbose_name='图片路径')
    name = models.CharField(max_length=50,verbose_name='图片名')
    owner = models.ForeignKey(UserInfo,on_delete=models.CASCADE,verbose_name='所属用户',related_name='owner')
    uploadtime = models.DateTimeField(verbose_name='上传时间', auto_now=True)
    downloadtimes = models.IntegerField(verbose_name='下载次数')
    liker = models.ManyToManyField(UserInfo,related_name='liker')
    likenum = models.IntegerField(verbose_name='赞',default=0)
    delete = models.BooleanField(verbose_name='是否删除',default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='图片表'
        verbose_name_plural='图片表'



