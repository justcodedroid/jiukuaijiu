from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.http.request import QueryDict
from django.views import View
from django.shortcuts import render

# 渲染,准备阶段
class BaseView(View):
    template_name = None
    def get(self,request,*args,**kwargs):
        # 新的知识点 hasattr getattr delattr setattr
        # hasattr(对象,方法) 进行判断
        # 判断当前对象有没有prepare
        if hasattr(self,'prepare'):
            getattr(self,'prepare')(request,*args,**kwargs)
        # 判断是否用了 获取cookie
        if hasattr(self,'handle_request_cookie'):
            getattr(self,'handle_request_cookie')(request,*args,**kwargs)

        response = render(request, self.template_name, self.get_context(request))
        # 添加cookie使用的
        if hasattr(self,'handle_response_cookie'):
            getattr(self,'handle_response_cookie')(response,*args,**kwargs)
        return response
    def get_context(self,request):

        context = {}
        context.update(self.get_extra_context(request))
        return context


    def get_extra_context(self,request):
        return {}

# 处理所有的重定向问题.
class BaseRedirect(View):
    # rediect url default None
    redirect_url = None
    def dispatch(self, request, *args, **kwargs):
        # 判断 是否需要重定向
        if hasattr(self,'handler'):
            getattr(self,'handler')(request,*args,**kwargs)
        # 风决定叶落的方向,而我确定你要走的路,不管对错.
        return HttpResponseRedirect(self.redirect_url)

class OperateView(View):
    form_cls = None
    def post(self,request,*args,**kwargs):
        form = self.form_cls(request.POST.dict())
        if form.is_valid():
            handler = request.POST.get('type','')
            if hasattr(self,handler):
                return JsonResponse(getattr(self,handler)(request,**form.cleaned_data))
            else:
                return HttpResponseBadRequest('type没有传递')
        else:
            return JsonResponse({'errorcode':-300,'errormsg':form.errors})
















