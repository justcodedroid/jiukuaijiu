from django.shortcuts import render
from view.views import *
from  tools.sessionhandle import *
from django import forms
# Create your views here.

#负责数据清洗
class MyForm(forms.Form):
    goodsid = forms.IntegerField()
    colorid = forms.IntegerField()
    sizeid = forms.IntegerField()
    count = forms.IntegerField(required=False)
    def clean(self):
        super(MyForm,self).clean()
        data = self.cleaned_data #清洗好的数据
        try:
            count = data['count']
            if count <0:
                self.errors['count'] = ['商品数量不能小于0']
        except:
            pass

#负责逻辑处理
class CartView(BaseRedirctView):
    redirct_url = '/cart/cart.html'
    #处理session
    def handle(self,request,*args,**kwargs):
        #创建一个session管理器 将session对象传进去
        cart_manager = isUserOrSession(request.session)
        #添加session
        cart_manager.add_cart_item(**request.POST.dict())


#负责显示
class CartListView(BaseView,OperateView):
    template_name = 'cart.html'
    form_cls = MyForm
    def get_extra_context(self,request):
        cart_manager = isUserOrSession(request.session)
        return {'cartItems':cart_manager.get_all_cart_items()}

    #处理ajax
    #添加数量
    def add(self,request,goodsid,colorid,sizeid,count,*args,**kwargs):
        request.session.modified = True
        cart_manager = isUserOrSession(request.session)
        try:
            cart_manager.add_cart_item(goodsid=goodsid, colorid=colorid, sizeid=sizeid, count=count)
            return {'errorcode':200,'errormsg':""}
        except Exception as e:
            return {'errorcode':-100,'errormsg':'%s'%e}
            # 处理ajax
    #删除数量
    def delete(self,request,goodsid,colorid,sizeid,count,*args,**kwargs):
        request.session.modified=True
        cart_manager=isUserOrSession (request.session)
        count = -1
        try:
            cart_manager.add_cart_item (goodsid=goodsid,colorid=colorid,sizeid=sizeid,count=count)
            return {'errorcode': 200,'errormsg': ""}
        except Exception as e:
            return {'errorcode': -100,'errormsg': '%s' % e}
    #删除商品项
    def delete_items(self,request,goodsid,colorid,sizeid,*args,**kwargs):
        request.session.modified =True
        cart_manager=isUserOrSession (request.session)
        try:
            cart_manager.del_cart_item (goodsid=goodsid,colorid=colorid,sizeid=sizeid)
            return {'errorcode': 200,'errormsg': ""}
        except Exception as e:
            return {'errorcode': -100,'errormsg': '%s' % e}