from django.shortcuts import render
from django.views import View
from mallproject.models import *
from django.core.paginator import Paginator
# Create your views here.
from tools.pagingutils import MultiObjectReturned
from view.views import BaseView

#商城类
class GoodsListView(BaseView,MultiObjectReturned):
    #所有不变的东西抽象到类成员中
    template_name = 'index.html'
    object_name = 'goods'
    category_objects = ShopCategory.objects.order_by('id').all()
    #初始化
    def prepare(self,request):
        #类别ID
        category_id = int(request.GET.get('category',1))
        self.objects = ShopCategory.objects.get(id=category_id).shopgoods_set.all()
        self.category_id = category_id

    def get_extra_context(self,request):
        page_num = request.GET.get('page',1)
        context = {'title':'商城','category_id':self.category_id,'categorys':self.category_objects}
        context.update(self.get_page(page_num))
        return context

#详情类
class DetailsView (BaseView):
    template_name = 'details.html'
    def Cookies(self,request,*args,**kwargs):
        goods_id_list = eval(request.COOKIES.get('history','[]'))
        goods_history = []   #局部列表 用于替换 全局变量的值
        for goods_id in goods_id_list:
            goods = ShopGoods.objects.get(id=goods_id)
            if goods_id != int(request.GET.get('goodsId')):
                goods_history.append({
                    'goods_id':goods_id,
                    'goods_img':goods.img(),
                    'goods_name':goods.gname,
                    'goods_price':goods.gprice,
                    'goods_goldprice':goods.goldprice
                })
        goods_history.reverse()  #最新浏览的商品最前面
        self.goods_history = goods_history
    def set_Cookies(self,response,*args,**kwargs):
        #category_id,goods_img,goods_name,goods_price,goods_goldprice
        goods_id = int(self.request.GET.get('goodsId'))
        self.history = eval(self.request.COOKIES.get('history','[]'))
        if goods_id not in self.history:
            self.history.append(int(goods_id))
        if len (self.history) > 5:
            self.history.pop(0)
            self.goods_history.pop()
        response.set_cookie('history',self.history)

    def get_extra_context(self,request):
        #商品ID
        goods_id = int(request.GET.get('goodsId'))
        # 商品详情
        goods=ShopGoods.objects.get (id=goods_id)
        #获得该商品类别id及名称
        category_id=goods.categoryid.id
        category_name = goods.categoryid.cname
        #默认库存数
        count = goods.shopstore_set.all()[0].count
        context = {'title':'详情','goods':goods,'category_id':category_id,'category_name':category_name,'count':count,'goods_history':self.goods_history[:4]}
        return context
