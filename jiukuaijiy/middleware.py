from django.http.response import HttpResponseRedirect
from jiukuaijiy import settings
from django.http.request import HttpRequest
import re
#验证用户是否通过正常url访问user后台
class UserAuth(object):
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request,*args, **kwargs):
        if request.path[:-1] in settings.AUTH:
            user = request.session.get('user','')
            if not user:
                return HttpResponseRedirect('/user/login')
        return self.get_response(request)
