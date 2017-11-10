from django.contrib import admin
from shop.models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','date_joined']

admin.site.register(AuthUser,UserAdmin)