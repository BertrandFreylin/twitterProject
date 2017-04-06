from django.conf.urls import url
from matcher import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^get_tweet_ratio/', views.get_tweet_ratio, name='get_tweet_ratio'),
    url(r'^get_popular_heroes/', views.get_popular_heroes, name='get_popular_heroes'),
]
