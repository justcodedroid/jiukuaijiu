# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

    def __str__(self):
        return u'%s'%(self.username)


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ShopCategory(models.Model):
    cname = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'shop_category'


class ShopColor(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'shop_color'


class ShopGoods(models.Model):
    gname = models.CharField(max_length=255)
    gdesc = models.CharField(max_length=1024, blank=True, null=True)
    gprice = models.DecimalField(max_digits=10, decimal_places=2)
    goldprice = models.DecimalField(max_digits=10, decimal_places=2)
    categoryid = models.ForeignKey(ShopCategory, models.DO_NOTHING, db_column='categoryId_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shop_goods'


class ShopGoodsdetails(models.Model):
    value = models.CharField(max_length=100)
    goodsid = models.ForeignKey(ShopGoods, models.DO_NOTHING, db_column='goodsId_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shop_goodsdetails'


class ShopOrder(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    desc = models.IntegerField()
    created = models.DateTimeField()
    content = models.TextField()
    user = models.ForeignKey('ShopUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_order'


class ShopSize(models.Model):
    value = models.CharField(max_length=255)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'shop_size'


class ShopStore(models.Model):
    count = models.IntegerField()
    color = models.ForeignKey(ShopColor, models.DO_NOTHING)
    goods = models.ForeignKey(ShopGoods, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_store'


class ShopStoreSize(models.Model):
    store = models.ForeignKey(ShopStore, models.DO_NOTHING)
    size = models.ForeignKey(ShopSize, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_store_size'
        unique_together = (('store', 'size'),)


class ShopUser(models.Model):
    user = models.CharField(max_length=254)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'shop_user'
