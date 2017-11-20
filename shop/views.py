from django.http import HttpResponse

from view.views import BaseView
from utils.pageutils import MuitlObjectReturned
from shop.models import *

class GoodsListView(BaseView,MuitlObjectReturned):
    template_name = 'category.html'
    objects_name = 'goods'
    category_objects = Category.objects.all()
    # 准备
    def prepare(self,request):
        category_id = int(request.GET.get('category',Category.objects.first().id))
        self.objects = Category.objects.get(id = category_id).goods_set.all()
        self.category_id = category_id

    def get_extra_context(self,request):
        page_num = request.GET.get('page',1)
        context = {'category_id': self.category_id, 'categorys': self.category_objects}
        # context['category_id'] = self.category_id
        # context['categorys'] = self.category_objects
        context.update(self.get_objects(page_num))
        return context

class Goodsdetails_view(BaseView):

    template_name = 'goods.html'
    # 自己选的路,怎么也得敲下去
    def get_size(self,request):
        goodid = int(request.GET.get('goodid', Goods.objects.first().id))
        self.goodid = goodid
        # 得到当前商品对应的库存信息
        stores =  Store.objects.filter(goods=goodid).all()
        store_store_id = []
        sizeids = []
        # 通过库存id得到对应的样式id
        for store in stores:
            store_store_id.append(StoreSize.objects.filter(store=store.id).all())

        for store_id in store_store_id:
            for size_id in store_id:
                if size_id.size not in sizeids:
                    sizeids.append(size_id.size)
        return sizeids


    def handle_request_cookie(self,request):
        # 获得cookie
        self.historys = eval(request.COOKIES.get('historys','[]'))

    def handle_response_cookie(self,response):
        # 填写用户浏览的商品id,存贮方式[id,id,id]
        # 首先判断商品id是否存在
        if self.goodid not in self.historys:
            self.historys.append(self.goodid)

        # 浏览器只存字符,不存对象
        response.set_cookie('historys',str(self.historys))
    def get_context(self,request):
        goodid = int(request.GET.get('goodid', Goods.objects.first().id))
        self.goodid = goodid
        context = {'goods': Goods.objects.get(id = goodid),}
        context['colorid'] = Goods.colors(context['goods'])[0].id
        context['colors'] = Goods.colors(context['goods'])
        context['sizes'] = self.get_size(request)
        context['details'] = Goodsdetails.objects.filter(goodsid_id=goodid)
        recomment_goods = []
        for history_goodid in self.historys:
            recomment_goods.append(Goods.objects.get(id = history_goodid))
        context['recomment_goods'] = recomment_goods[:4]
        return context























# 0.1版本
# from django.shortcuts import render
# from django.views import View
# from shop.models import *
# # Create your views here.
# from django.http.response import HttpResponse
# # 自定义视图
# class BaseView(View):
#     # 模板默认为空
#     template_name = None
#     # context 字典
#     context = {}
#     # 返回视图
#     def get(self, request, *args, **kwargs):
#         return render(request,self.template_name,self.get_context(request))
#     # 渲染中间件
#     def get_context(self,request):
#         # 更新context
#         self.context.update(self.get_extra_context(request))
#         return self.context
#
#     def get_extra_context(self,request):
#         pass
#
# # 多页面处理
# class MulyiObjectReturned(BaseView):
#     # 模块名
#     model = None
#     # 对象名
#     objects_name = 'objects'
#     # 页面处理方法 分页 per_page 每页显示的数量,page_num 当前页 默认为第一页 objects 是要显示的对象
#     def get_objects(self,page_num = '1',per_page= 12,objects = None, *args,**kwargs):
#         # 分页
#         from django.core.paginator import Paginator
#         # 判断要处理的是什么分页
#         if objects == None:
#             paginator = Paginator(self.model.objects.all(),per_page)
#         else:
#             paginator = Paginator(objects,per_page)
#         page_num = int(page_num)
#         # 对页面进行处理
#         if page_num < 1:
#             page_num = 1
#         # paginator.num_pages 总页数
#         if page_num > paginator.num_pages:
#             page_num = paginator.num_pages
#         # 当前页的所有东西
#         page = paginator.page(page_num)
#         # 返回一个字典
#         return  {'page':page,self.objects_name:page.object_list,'page_range':paginator.page_range}
#
#
# class GoodsListView(MulyiObjectReturned):
#     template_name = 'category.html'
#     objects_name = 'goods'
#     def get_extra_context(self,request):
#         # 类别id
#         category_id = int(request.GET.get('category',Category.objects.first().id))
#         # 类的值
#         self.category_id = category_id
#         # 获取第几页 默认为1
#         page_num = request.GET.get('page',1)
#         # 调用查询页面
#         self.get_objects(page_num)
#         # 字典
#         context = {}
#         # 类别id
#         context['category_id'] = category_id
#         # 所有类别
#         context['categorys'] = Category.objects.all()
#         # 返回字典
#         return  context
#     # 重写get_objects 方法
#     def get_objects(self,page_num = '1',per_page= 12,objects = None, *args,**kwargs):
#         # 得到当前类别下的所有商品
#         objects = Category.objects.get(id=self.category_id).goods_set.all()
#         # 更新字典 作用:忘了
#         self.context.update(MulyiObjectReturned.get_objects(self,page_num,per_page,objects=objects))













































