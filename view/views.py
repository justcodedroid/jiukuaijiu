from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect,HttpResponse
from django.http.response import JsonResponse,HttpResponseBadRequest
#商城基类
class BaseView(View):
    template_name = None  #模板名称
    history = []  #浏览记录
    goods_history=[] #浏览记录详情
    #get请求
    def get(self,request,*args,**kwargs):
        #准备阶段
        if hasattr(self,'prepare'):
            getattr(self,'prepare')(request,*args,**kwargs)
        if hasattr(self,'Cookies'):
            getattr(self,'Cookies')(request,*args,**kwargs)
        response=render (request,self.template_name,self.__context (request))
        if hasattr(self,'set_Cookies'):
            getattr(self,'set_Cookies')(response,*args,**kwargs)
        return response
    #返回的上下文
    def __context(self,request):
        self.user = request.session.get('user','')
        context = {'user':self.user}
        context.update(self.get_extra_context(request))
        return context
    #更新上下文
    def get_extra_context(self,request):
        return {}

#处理重定向  业务逻辑
class BaseRedirctView(View):
    redirct_url = None
    def dispatch(self, request, *args, **kwargs):
        #处理业务逻辑
        if hasattr(self,'handle'):
            getattr(self,'handle')(request,*args,**kwargs)
        #重写方法 不管是get还是post 都重定向到该界面
        return HttpResponseRedirect(self.redirct_url)

#负责ajax处理 处理post请求
class OperateView(View):
    form_cls = None
    def post(self,request,*args,**kwargs):
        post_json = request.POST.dict()
        del post_json['csrfmiddlewaretoken']
        if self.form_cls:
            form = self.form_cls(post_json)
            if form.is_valid():  #判断数据是否为整数
                handle = request.POST.get('type','')
                if hasattr(self,handle):
                    return JsonResponse(getattr(self,handle)(request,**form.cleaned_data),safe=False)
                else:
                    return HttpResponseBadRequest('type没有传递')
            else:
                return JsonResponse({'errorcode':-300,'errormsg':form.errors})
        else:
            if hasattr(self,'post_handle'):
                return HttpResponse(getattr(self,'post_handle')(request,**post_json))