from django.db import models
from tools.md5encryption import md5

# Create your models here.
class User(models.Model):
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=64)
    #注册用户
    @staticmethod
    def registeruser(account,password,*args,**kwargs):
        try:
            User.objects.get(account=account)  #是否查询到该用户
            return '该用户已存在'
        except Exception:
            return User.objects.create(account=account,password=password) #返回该对象

    @staticmethod
    def login(account,password,time,*args,**kwargs):
        try:
            user = User.objects.get(account=account)
            md5_password = md5(user.password+time)
            if md5_password == password:
                return user
            else:
                return '密码错误'
        except Exception:
            return '该用户不存在'
    @staticmethod
    def exit(request,account,*args,**kwargs):
        if request.session.get('user',""):
            #{'user':'admin'}
            del request.session['user']

class Address(models.Model):
    province=models.CharField (max_length=10)
    city=models.CharField (max_length=10)
    area=models.CharField (max_length=10)
    details=models.CharField (max_length=520)
    name=models.CharField (max_length=20)
    phone=models.CharField (max_length=11)
    user=models.ForeignKey (User)
    #是否删除
    isdelete=models.BooleanField (default=False)
    # 默认收货地址
    isprimary=models.BooleanField (default=False)

    #创建收获地址
    def add_address(self,name,phone,province,city,area,details,user):
        if self.objects.all().count()>5:
            return None
        return self.objects.create(name=name,phone=phone,province=province,city=city,area=area,details=details,user=user)
    #获取所有收获地址
    @staticmethod
    def get_all_addr(user):
        return Address.objects.filter(user__account=user)

class UserCartItems(models.Model):
    key = models.CharField(max_length=20,unique=True)
    goodsid = models.CharField(max_length=20)
    colorid = models.CharField(max_length=20)
    sizeid = models.CharField(max_length=20)
    count = models.CharField(max_length=20)
    user = models.ForeignKey(User)