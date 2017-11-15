# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    cname = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'shop_category'
        # 排序
        ordering = ['id']
    def __str__(self):
        return u'%s'%self.cname

class Goods(models.Model):
    gname = models.CharField(max_length=255)
    gdesc = models.CharField(max_length=1024, blank=True, null=True)
    gprice = models.DecimalField(max_digits=10, decimal_places=2)
    goldprice = models.DecimalField(max_digits=10, decimal_places=2)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryId_id')

    # 商品图片处理
    def img(self):
        return self.store_set.first().color.value
    # 商品展示页图片
    def colors(self):
        stores = self.store_set.all()
        colors = []
        for store in stores:
            # 去重
            color = store.color
            if color not in colors:
                colors.append(color)
        return colors
    # 大小样式
    # def sizes(self):
    #     stores = self.store_set.all()
    #     sizes = []
    #     for store in stores:
    #         # 去重
    #         size = store.size
    #         if size not in sizes:
    #             sizes.append(size)
    #     return sizes
    class Meta:
        managed = False
        db_table = 'shop_goods'
        ordering = ['id']
    def __str__(self):
        return u'%s'%(self.gname)


class Goodsdetails(models.Model):
    value = models.ImageField()
    goodsid = models.ForeignKey(Goods, models.DO_NOTHING, db_column='goodsId_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shop_goodsdetails'
        ordering = ['id']
    def __str__(self):
        return u"%s"%self.goodsid


class Color(models.Model):
    name = models.CharField(max_length=20)
    value = models.ImageField(upload_to='color')

    class Meta:
        managed = False
        db_table = 'shop_color'
    def __str__(self):
        return u'%s'%self.name




# class Order(models.Model):
#     id = models.CharField(primary_key=True, max_length=32)
#     desc = models.IntegerField()
#     created = models.DateTimeField()
#     content = models.TextField()
#     user = models.ForeignKey('User', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'shop_order'


class Size(models.Model):
    value = models.CharField(max_length=255)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'shop_size'
    def __str__(self):
        return u'%s'%self.name


# 库存表
class Store(models.Model):
    count = models.IntegerField()
    color = models.ForeignKey(Color, models.DO_NOTHING)
    goods = models.ForeignKey(Goods, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_store'
    def __str__(self):
        return u'%s'%self.goods.gname

class StoreSize(models.Model):
    store = models.ForeignKey(Store, models.DO_NOTHING)
    size = models.ForeignKey(Size, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_store_size'
        unique_together = (('store', 'size'),)
#
#
# class User(models.Model):
#     user = models.CharField(max_length=254)
#     password = models.CharField(max_length=255)
#
#     class Meta:
#         managed = False
#         db_table = 'shop_user'

