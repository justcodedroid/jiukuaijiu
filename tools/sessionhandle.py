from cart.models import *
from user.models import *
from django.db import transaction
#购物车管理器
#基类
class BaseCartManager(object):
    """
    购物车基类
    add_cart_item ： 添加购物车项
    del_cart_item ： 删除购物车项
    get_all_cart_item ： 获得全部购物车项
    __get_key: 生成商品key
    """
    def add_cart_item(self,goodsid,colorid,sizeid,count,type,*args,**kwargs):
        pass
    def del_cart_item(self,goodsid,colorid,sizeid,*args,**kwargs):
        pass
    def get_all_cart_items(self,*args,**kwargs):
        pass
    #生成商品key
    def get_key(self,goodsid,colorid,sizeid):
        return "%s:%s:%s" % (goodsid,colorid,sizeid)

#总控制器 判断用户是否在线 在线使用sql存储 不在线使用session存储
def isUserOrSession(session):
    if session.get('user',''):
        return UserSqlManager(session)
    else:
        return SessionCartManager(session)

#数据库存储
class UserSqlManager(BaseCartManager):
    def __init__(self,session):
        self.session = session
    #添加到数据库
    @transaction.atomic
    def add_cart_item(self,goodsid,colorid,sizeid,count,type=None,*args,**kwargs):
        # print(goodsid,colorid,sizeid,count,type)
        #获得key
        key = self.get_key(goodsid,colorid,sizeid)
        #判断数据库是否有该数据
        try:
           userdata = UserCartItems.objects.get(key=key)
           if userdata:
               """判断是否是从详情页面过来得数据
                 如果是直接赋值
                 如果不是 是从购物车通过ajax发送得数据"""
               if type =='insert':
                   userdata.count = count
                   userdata.save()
               else:
                   count = int(userdata.count) +int(count)
                   userdata.count = count
                   userdata.save()
        except Exception as e:
            UserCartItems.objects.create(key=key,goodsid=goodsid,colorid=colorid,sizeid=sizeid,count=count,user=User.objects.get(account=self.session.get('user')))
    #删除cart项
    @transaction.atomic
    def del_cart_item(self,goodsid,colorid,sizeid,*args,**kwargs):
        #生成key
        key = self.get_key(goodsid,colorid,sizeid)
        try:
            UserCartItems.objects.get(key=key).delete()
        except Exception as e:
            pass
    #返回一个cartitem对象
    def get_cart_item(self,goodsid,colorid,sizeid,count,*args,**kwargs):
        user = self.session.get('user','')
        usercart = User.objects.get(account=user).usercartitems_set.get(goodsid=goodsid,colorid=colorid,sizeid=sizeid,count=count)
        return CartItem(goodsid=usercart.goodsid,colorid=usercart.colorid,sizeid=usercart.sizeid,count=usercart.count)
    def get_all_cart_items(self,*args,**kwargs):
        #首先获得该用户
        user = self.session.get('user')
        usercart=User.objects.get (account=user).usercartitems_set.values ('key','goodsid','colorid','sizeid','count')
        cart =[]
        for data in usercart:
            cart.append(CartItem(goodsid=data['goodsid'],colorid=data['colorid'],sizeid=data['sizeid'],count=data['count']))
        return cart
#session 购物车管理器
class SessionCartManager(BaseCartManager):

    def __init__(self,session):
        '传一个session对象'
        self.session = session
    def add_cart_item(self,goodsid,colorid,sizeid,count,type,*args,**kwargs):
        count = int(count)
        #获得session 数据 如果没有 默认为[]
        cart = self.session.get('cart',[])
        #获得商品唯一key
        key = self.get_key(goodsid,colorid,sizeid)
        #判断商品是否在session中
        if self.__is_exist(cart,key):
            #如果存在取出项目  并赋值
            cartiem = self.__get_cart_item(cart,key)
            if cartiem.count+count >=1:
                cartiem.count+=count
        else:
            cart.append({key:CartItem(goodsid=goodsid,colorid=colorid,sizeid=sizeid,count=count)})
        self.session['cart'] = cart

    def del_cart_item(self,goodsid,colorid,sizeid,*args,**kwargs):
        cart = self.session.get('cart',[])
        key = self.get_key(goodsid,colorid,sizeid)
        if self.__is_exist(cart,key):
            #[{'5:21:6': <CartItem: CartItem object>}, {'5:21:8': <CartItem: CartItem object>}]
            for data in cart:
                    for data_key in data.keys():
                        if data_key == key:
                            cart.remove(data)
                            break

#获得所有购物车项目
    def get_all_cart_items(self,*args,**kwargs):
        cart = self.session.get('cart')
        if cart == None:
            return []
        else:
            cartitems = []
            for cartitem in cart:
                cartitems.extend(cartitem.values())
            print(cartitems)
            return cartitems

    #判断数据是否存在
    def __is_exist(self,cart,key):
        # print('cart',cart,'key',key)
        #默认不存在
        isExist = False
        for cartitem in cart:
            # print(cartitem.keys())
            for cartkey in cartitem.keys():
                if cartkey ==key:
                    isExist = True
                    break
        return isExist
    #取出单个项目
    def __get_cart_item(self,cart,key):
        "session格式 [{key:value},{key:value}]"
        for cartiem in cart:
            for cartkey in cartiem.keys():
                if cartkey == key:
                    return cartiem[key]
        return None


