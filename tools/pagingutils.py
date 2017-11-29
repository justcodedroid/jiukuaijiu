#分页使用
from django.core.paginator import Paginator


#分页返回多个对象
class MultiObjectReturned(object):
    per_page = 12  #每页多少个数据
    objects = None  #提供一个集合对象
    object_name = 'objects'
    def get_page(self,page_num ='1'):
        paginator = Paginator(self.objects,self.per_page)
        page = paginator.page(page_num)
        page_num = int(page_num)
        #判断是否越界
        if page_num < 1 : page_num = 1
        if page_num > paginator.num_pages : page_num = paginator.num_pages

        #分页显示计算
        left = 2
        right = 2

        if page_num <=2:
            start = 1
            end = left+right+1
        if page_num > left:
            start = page_num-left
            end = page_num+right

        if end > paginator.num_pages:
            min1 = end-paginator.num_pages
            end = paginator.num_pages
            start -= min1
            if start<1:
                start = 1
        return {'page':page,'page_range':range(start,end+1),self.object_name:page.object_list}