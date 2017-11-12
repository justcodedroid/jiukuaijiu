from django.shortcuts import render
from django.views import View
# Create your views here.
from django.http.response import HttpResponse

# class BaseView(View):
#     template = None
#     def get(self, request, *args, **kwargs):
#         render(request,template_name=self.template,context=self.get_context())
#
#     def get_context(self):
#         return None

class IndexView(View):
    # template = 'goods.html'
    def get(self, request, *args, **kwargs):
        return render(request,'goods.html')