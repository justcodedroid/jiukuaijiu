from django.shortcuts import render
from django.views import View
# Create your views here.
from django.http.response import HttpResponse

class IndexView(View):
    def get(self,request):
        return HttpResponse('通用的')