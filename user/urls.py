from django.conf.urls import url
from user import views
urlpatterns = [
    url(r'^login/$',views.UserView.as_view()),
    url(r'^logincontol/$',views.LoginContolView.as_view()),
    url(r'^register/$',views.RegisterView.as_view()),
    url(r'^registercontol/$',views.RegisterContolView.as_view()),
    url(r'^admin/$',views.AdminView.as_view()),
    url(r'^address/$',views.AddressView.as_view()),
    url(r'^exit/$',views.ExitContolView.as_view()),
]