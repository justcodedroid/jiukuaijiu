# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from  view.views import BaseView
from  utils.pageutils import MuitlObjectReturned
from goods.models import *
class GoodsListView(BaseView,MuitlObjectReturned):
    # 所有不变的东西，都放到了类的成员当中
    template_name = 'index.html'
    objects_name = 'goods'
    category_objects = Category.objects.all()

    def prepare(self,request):
        category_id = int(request.GET.get('category',Category.objects.first().id))
        self.objects=Category.objects.get(id =category_id ).goods_set.all()
        self.category_id = category_id
    def get_extra_context(self, request):
        page_num = request.GET.get('page',1)
        context = {'category_id':self.category_id,'categorys':self.category_objects}
        context.update(self.get_objects(page_num))
        return  context
