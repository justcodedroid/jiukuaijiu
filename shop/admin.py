from django.contrib import admin
from shop.models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','date_joined']

admin.site.register(AuthUser,UserAdmin)
admin.site.register(ShopCategory)
admin.site.register(ShopColor)
admin.site.register(ShopGoods)
admin.site.register(ShopGoodsdetails)
admin.site.register(ShopOrder)
admin.site.register(ShopSize)
admin.site.register(ShopStore)
admin.site.register(ShopStoreSize)
admin.site.register(ShopUser)