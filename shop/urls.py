from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^$', views.GoodsListView.as_view()),
    url(r'^goods/$', views.Goodsdetails_view.as_view()),
]