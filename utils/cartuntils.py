from cart.models import *
# 欢迎来到session加工厂
# 仓库模型开始构建?
class CartManager(object):
    # 功能开始规划
    # 添加功能,以及需要材料
    def add_cart_item(self,goodsid,colorid,sizeid,count,*args,**kwargs):
        pass
    # 删除功能,以及需要的材料
    def delete_cart_item(self,goodsid,colorid,sizeid,count,*args,**kwargs):
        pass
    # 材料处理
    def get_all_cart_items(self,*args,**kwargs):
        pass

# session 车间开始创建 依赖主仓库
class SessionCartManager(CartManager):
    # 原始材料预处理
    def __init__(self,session):
        self.session = session

    # 材料开始处理
    def add_cart_item(self,goodsid,colorid,sizeid,count,*args,**kwargs):
        # 材料不符合工厂规定,需要清洗
        count = int(count)
        # 获取主材料: 没有材料,工厂不启动
        cart = self.session.get('cart',[])
        # 获得产标号
        # 产标号,需要产标机处理,当前没有产标机,需要建设产标机,
        key = self.__gen_key(goodsid,colorid,sizeid)

        # 得到所有材料,判断当前标号是否生产,生产了,则不需要刻模板,添加生产数即可,没有则刻模板,生产
        # 判断是否生产,需要检验中心的支持,当前没有检验中心,需要建设.
        if self.is_exist(cart,key):
            # 有,则不需要设计模板,直接增加生产量就可以,
            cartitime = self.get_cart_item(cart,key)
            # 增加生产量
            cartitime.count += count
        # 没有在工厂得到当前标号,需要建设模板,需要model生产模板,
        else:
            cart.append({key:CartItem(goodsid=goodsid,colorid=colorid,sizeid=sizeid,count=count)})
        # 生产完成,存到仓库
        self.session['cart'] = cart
    # 异常情况,产品销毁
    def delete_cart_item(self,goodsid,colorid,sizeid,count,*args,**kwargs):
        # 资金困难暂时无法建设销毁中心
        pass
    # 库存详情
    def get_all_cart_items(self,*args,**kwargs):
        # 获取当前中心仓库
        cart = self.session.get('cart')
        # 判断是否为空
        if cart  == None:
            return cart == None
        else:
            # 查看所有库存,生成报表
            cartitems = []
            for cartitem in cart:
                cartitems.extend(cartitem.values())
            return cartitems
    # 生产车间建设:
    def get_cart_item(self,cart,key):
        for cartitiem in cart:
            if list(cartitiem.keys())[0] == key:
                return cartitiem[key]
        return None


    # 检验中心建设 需要标号,以及所属的产品中心.
    def is_exist(self,cart,key):
        # 初始值,默认为无
        isExist = False
        # 从所有当前产品中心下的标号中检索
        for cartitem in cart:
            if list(cartitem.keys())[0] == key:
                isExist = True
                break
        return  isExist


    # 产标机,生产标号
    def __gen_key(self,goodsid,colorid,sizeid):
        return goodsid+':'+colorid+':'+sizeid































