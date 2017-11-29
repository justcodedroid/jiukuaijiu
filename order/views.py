from django.shortcuts import render
from view.views import *
from tools.sessionhandle import *
from django.db import transaction
from tools.alipay import AliPay
from jiukuaijiy.settings import BASE_DIR
import os,time,uuid
from order.models import Order
alipay = AliPay(
    appid='2016082700317781',
    app_private_key_path=os.path.join(BASE_DIR, 'keys/app_private_2048.txt'),
    alipay_public_key_path=os.path.join(BASE_DIR, 'keys/alipay_public_2048.txt'),
    return_url='http://127.0.0.1:8000/order/alipay/', #
    app_notify_url='http://www.pythoncloude.pythonanywhere.com/alipay/post'
)
# Create your views here.
#跳转
class OrderView(OperateView):
    def post_handle(self,request,cartitems):
        if request.session.get('user',''):
            request.session['cartitems'] = cartitems
            return '/order/order.html/'
        else:
            return '/user/login/'


#订单显示
class OrderListView(BaseView):
    template_name = 'order.html'
    def get_extra_context(self,request):
        user = request.session.get('user')
        "订单商品得显示及其他"
        rawcartitems = request.session.get('cartitems','')  #订单信息
        cartitems = rawcartitems.split(':')
        cartManager = isUserOrSession(request.session)
        order_items = []
        #商品列表
        for cartitem in cartitems:
            order_items.append(cartManager.get_cart_item(*cartitem.split(',')))
        #收获地址
        address = Address.objects.filter(user=User.objects.get(account=user)).first()
        #商品总金额
        price_all = 0
        for cart in order_items:
            price_all += cart.all_price()
        return {'orderitems':order_items,'address':address,'price':price_all,'raworderitems':rawcartitems}

class OrderCreatedView(BaseRedirctView):
    redirct_url = '' #要支付得url
    #事务
    transaction.atomic
    def handle(self,request):
        request.session.modified = True
        del request.session['cartitems']
        orderitems = request.GET.get('orderitems')
        orderitems = orderitems.split(':')
        cart_manager = isUserOrSession(request.session)
        price = 0
        for orderitem in orderitems:
            price+=cart_manager.get_cart_item(*orderitem.split(',')).all_price()

        for orderitem in orderitems:
            #删除
            cart_manager.del_cart_item(*orderitem.split(','))

        #创建order对象
        order = Order(
            name=request.GET.get('name'),
            phone=request.GET.get('phone'),
            payway=request.GET.get ('type'),
            orderitems=orderitems,
            user=User.objects.get(account=request.session.get ('user')),
            sign=uuid.uuid4().hex,  # 基本上不会重复（订单的唯一标示）
            order=str (time.time () * 1000)  # 很多可能会重复（标示一个人在什么时间买的东西）
            )

        #库存
        for orderitem in orderitems:
            goodsid,colorid,sizeid,count=orderitem.split(',')
            store = ShopGoods.objects.get(id=goodsid).shopstore_set.filter(color_id=colorid).first()
            store.count -=int(count)
            store.save() #保存到数据库
        #根据支付方式，生成字符界面
        param=alipay.direct_pay(out_trade_no=order.sign,subject='九块九商城',total_amount=str(price))
        url = 'https://openapi.alipaydev.com/gateway.do?'+param
        order.save() #保存订单 未支付状态
        self.redirct_url=url

#支付宝回调页面
class AliPayView(View):
    def get(self,request):
        data = request.GET.dict()
        sign = data.pop('sign')
        if alipay.verify(data,sign):
            order = Order.objects.get(sign=data['out_trade_no'])
            order.status ='待发货'
            order.trade_no=data['trade_no']
            order.save()
            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')
