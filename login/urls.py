from login import views

from django.conf.urls import url

urlpatterns = [
    url(r'^login.html/$',views.loginListView.as_view()),
    url(r'^$',views.loginView.as_view()),
]