from django.shortcuts import render
from django.views import View
from mallproject.models import *
from django.core.paginator import Paginator
# Create your views here.
#商城基类
class MallBase (View):
    #访问的页面
    template = None
    context = {}
    #上下文
    def get_context (self,request,*args,**kwargs):
        return self.context
    def get(self,request,*args,**kwargs):
        return render(request,self.template,self.get_context(request))
    def post(self,request,*args,**kwargs):
        return render (request,self.template,self.get_context(request))
#用于分页
class Multi_object_return(MallBase):
    def page(self,object,num='1',per_page=12):
        '''
            :param object:  
            :param num: 
            :param per_page: 
            :return:             
            object:传入一个要查询的对象集合
            num:要查询的第一页内容 默认为第一页
            per_page:每一页显示的内容数 默认为12
        '''''
        num = int(num)
        paginator = Paginator(object,per_page=per_page)
        page = paginator.page(num)

        #判断是否越界
        if num <1:
            num = 1
        elif num >paginator.num_pages:
            num = paginator.num_pages

        left = 2
        right = 2

        if num <=left:
            start = 1            #起始1
            end = left+right+1   #结束5
        if num >left:
            start = num-left
            end = num+right

        if end > paginator.num_pages:
            min1 = end-paginator.num_pages
            end = paginator.num_pages
            start -= min1
            if start<1:
                start = 1
            self.context['page'] = page
            self.context['range'] = range(start,end+1)
        return self.context



class Mall_view (Multi_object_return):
    template = 'index.html'
    #显示商城类别
    def show_navigation(self,request):
        return ShopCategory.objects.order_by('id').all()
    #显示商品
    def show_goods(self,request,category):
        return ShopCategory.objects.get(id = category).shopgoods_set.order_by('id').all()
    #重写父类方法
    def get_context(self,request,*args,**kwargs):
        #获得类别
        category=request.GET.get ('category',1)
        self.context['category_id'] = int(category)
        self.context['category'] = self.show_navigation(request)
        self.context['goods'] = self.show_goods(request,category)

        return self.page(self.context['goods'],per_page=1)
