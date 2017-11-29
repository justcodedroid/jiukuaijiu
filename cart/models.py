from django.db import models
from mallproject.models import *
# Create your models here.

class CartItem(models.Model):
    #购物车对象
    goodsid = models.IntegerField()
    colorid = models.IntegerField()
    sizeid = models.IntegerField()
    count = models.IntegerField()

    def goods(self):
        return ShopGoods.objects.get(id=self.goodsid)
    def color(self):
        return ShopColor.objects.get(id=self.colorid)
    def size(self):
        return ShopSize.objects.get(id=self.sizeid)
    #价钱
    def all_price(self):
        return self.goods().gprice *(int(self.count))
