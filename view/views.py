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
        return render(request, self.template_name, self.get_context(request))

    def get_context(self,request):

        context = {}
        context.update(self.get_extra_context(request))
        return context


    def get_extra_context(self,request):
        return {}




















