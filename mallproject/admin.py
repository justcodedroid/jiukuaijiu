from django.contrib import admin
from mallproject.models import *
# Register your models here.



#注册表
admin.site.register(ShopCategory)
admin.site.register(ShopColor)
admin.site.register(ShopGoods)
admin.site.register(ShopGoodsdetails)
admin.site.register(ShopOrder)
admin.site.register(ShopSize)
admin.site.register(ShopStore)
admin.site.register(ShopStoreSize)
admin.site.register(ShopUser)