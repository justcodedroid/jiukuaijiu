# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models

#商店类别表
class ShopCategory(models.Model):
    cname = models.CharField(unique=True, max_length=255)
    def __str__(self):
        return r"%s"%self.cname
    class Meta:
        managed = False
        db_table = 'shop_category'
        verbose_name = '商品类别表'

#商店颜色表
class ShopColor(models.Model):
    name = models.CharField(max_length=20)
    value = models.ImageField(upload_to='color/')
    def __str__(self):
        return r"%s"%self.name
    class Meta:
        managed = False
        db_table = 'shop_color'
        verbose_name = '商品颜色'

#商店商品表
class ShopGoods(models.Model):
    gname = models.CharField(max_length=255)
    gdesc = models.CharField(max_length=1024, blank=True, null=True)
    gprice = models.DecimalField(max_digits=10, decimal_places=2)
    goldprice = models.DecimalField(max_digits=10, decimal_places=2)
    categoryid = models.ForeignKey(ShopCategory, models.DO_NOTHING, db_column='categoryId_id')  # Field name made lowercase.
    #获取一张图片用于展示
    def img(self):
        #获取第一张图片
        return self.shopstore_set.first().color.value
    # 商品详情
    def get_deatils(self):
        goodsdetails=self.shopgoodsdetails_set.all ()
        details=[]
        for i in goodsdetails:
            details.append (i.value)
        return details
    #获得该商品所有颜色
    def get_color(self):
        store=self.shopstore_set.all ()
        colors = []
        for color in store:
            colors.append({"color_id":color.color.id,"color_value":color.color.value})
        return colors
    #获得该商品所有尺码
    def get_size(self):
        store = self.shopstore_set.all()
        sizes = []
        for size in store:
            size_1 = size.shopstoresize_set.all()
            for i in size_1:
                temp = {'id':i.size.id,'size_name':i.size.value}
                if temp not in sizes:
                    sizes.append({'id':i.size.id,'size_name':i.size.value})
        return sizes
    def __str__(self):
        return r"%s"%self.gname
    class Meta:
        managed = False
        db_table = 'shop_goods'
        verbose_name='商品'

#商品展示图片
class ShopGoodsdetails(models.Model):
    value = models.CharField(max_length=100)
    goodsid = models.ForeignKey(ShopGoods, models.DO_NOTHING, db_column='goodsId_id')  # Field name made lowercase.
    def __str__(self):
        return r"%s"%self.value
    class Meta:
        managed = False
        db_table = 'shop_goodsdetails'
        verbose_name='商品展示图片'


#商品订单表
class ShopOrder(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    desc = models.IntegerField()
    created = models.DateTimeField()
    content = models.TextField()
    user = models.ForeignKey('ShopUser', models.DO_NOTHING)
    def __str__(self):
        return u'%s'%self.user
    class Meta:
        managed = False
        db_table = 'shop_order'
        verbose_name = '商品订单'

#尺码表
class ShopSize(models.Model):
    value = models.CharField(max_length=255)
    name = models.CharField(max_length=20)

    def __str__(self):
        return u'%s'%self.name
    class Meta:
        managed = False
        db_table = 'shop_size'
        verbose_name = '尺码表'

#购物商店
class ShopStore(models.Model):
    count = models.IntegerField()
    color = models.ForeignKey(ShopColor, models.DO_NOTHING)
    goods = models.ForeignKey(ShopGoods, models.DO_NOTHING)
    def __str__(self):
        return u'%s'%self.color
    class Meta:
        managed = False
        db_table = 'shop_store'
        verbose_name = '购物商店'

#商品尺寸表
class ShopStoreSize(models.Model):
    store = models.ForeignKey(ShopStore, models.DO_NOTHING)
    size = models.ForeignKey(ShopSize, models.DO_NOTHING)
    def __str__(self):
        return u'%s'%self.id
    class Meta:
        managed = False
        db_table = 'shop_store_size'
        unique_together = (('store', 'size'),)
        verbose_name = '商品尺寸表'

#用户表
class ShopUser(models.Model):
    user = models.CharField(max_length=254)
    password = models.CharField(max_length=255)
    def __str__(self):
        return u'%s'%self.user

    class Meta:
        managed = False
        db_table = 'shop_user'
        verbose_name = '用户表'

#用户商品表
class UserGoods(models.Model):
    goodsid = models.IntegerField()
    colorid = models.IntegerField()
    sizeid = models.IntegerField()
    count = models.IntegerField()
    user = models.ForeignKey(ShopUser)