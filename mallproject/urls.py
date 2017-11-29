from django.conf.urls import url
from mallproject import views
urlpatterns = [
    url(r'^$',views.GoodsListView.as_view()),
    url(r'^details/$',views.DetailsView.as_view()),
]