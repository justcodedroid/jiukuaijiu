from django.shortcuts import render
from django.http import HttpResponse
from view.views import *
from user.models import *
from django import forms
from tools.md5encryption import *
# Create your views here.
#负责登陆逻辑
class LoginContolView(BaseRedirctView):
    redirct_url = '/user/admin/'
    def handle(self,request,*arge,**kwargs):
        user = None
        if request.session.get('usererror',''):
            del request.session['usererror']  # 先清除session error错误信息
        try:
            user = User.login(**request.POST.dict())
            request.session['user'] = user.account
        except Exception:
            self.redirct_url='/user/login/'
            request.session['usererror'] = user
            print (request.session.get ('usererror'))

    #显示登陆页面
class UserView(BaseView):
    template_name = 'login.html'
    def get_extra_context(self,request):
        context={'usererror': request.session.get ('usererror','')}
        if request.session.get ('usererror',''):
            del request.session['usererror']  # 先清除session error错误信息
        return context


#负责注册逻辑
class RegisterContolView(BaseRedirctView):
    redirct_url = '/user/admin/'
    def handle(self,request,*args,**kwargs):
        user =None
        if request.session.get('usererror',""):
            del request.session['usererror']  #先清除session error错误信息
        #注册用户
        try:
            user = User.registeruser(**request.POST.dict())
            request.session['user'] = user.account
        except Exception:
            self.redirct_url='/user/register/'
            request.session['usererror'] = user



#显示注册页面
class RegisterView(BaseView):
    template_name = 'register.html'
    def get_extra_context(self,request):
        context={'usererror': request.session.get ('usererror','')}
        if request.session.get ('usererror',''):
            del request.session['usererror']  # 先清除session error错误信息
        return context

#用户中心
class AdminView (BaseView):
    template_name = 'user.html'
    def get_extra_context(self,request):
        #获取用户
        user = request.session.get('user','')
        return {'user':user}

class AddressForm (forms.Form):
    provinceid=forms.IntegerField (required=False)
    cityid=forms.IntegerField (required=False)
    areaid=forms.IntegerField (required=False)
    details=forms.CharField (required=False)
    name=forms.CharField (required=False)
    phone=forms.CharField (required=False)
#地址管理
class AddressView(BaseView,OperateView):
    template_name = 'address.html'
    form_cls = AddressForm
    def get_extra_context(self,request):
        default_citys=get_citys_by_id (provinces[0]['id'])
        default_areas=get_areas_by_id (default_citys[0]['id'])
        return {'provinces': provinces,'citys': default_citys,'areas': default_areas,'addr':Address.get_all_addr(request.session.get('user',''))}


    def get_province(self,request,provinceid,*args,**kwargs):
        data=[]
        citys=get_citys_by_id (str (provinceid))
        data.append (citys)
        data.append (get_areas_by_id (citys[0]['id']))
        return data


    def get_citys(self,request,cityid,*args,**kwargs):
        return get_areas_by_id (str (cityid))

    def save(self,request,name,phone,provinceid,cityid,areaid,details,*arge,**kwargs):
        user = User.objects.get(account=request.session.get('user',''))
        #存入数据库
        try:
            addr_info = {
                'name':name,
                'phone':phone,
                'province':get_province_one(provinceid),
                'city':get_city_one(provinceid,cityid),
                'area':get_area_one(cityid,areaid),
                'details':details,
                'user':user
            }
            address = Address.add_address(**addr_info)
            if address:
                return {'errorcode':200,'errormsg':''}
            else:
                return{'errorcode':-300,'errormsg':'添加地址最多不能超过5个'}
        except Exception as e:
            return {'errorcode':-100,'errormsg':"%s"%e}

#退出登陆
class ExitContolView(BaseRedirctView):
    redirct_url = '/user/login/'
    def handle(self,request,*args,**kwargs):
        User.exit(request,account=request.session.get('user',''))