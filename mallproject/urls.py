from django.conf.urls import url
from mallproject import views
urlpatterns = [
    url(r'^$',views.Mall_view.as_view())
]