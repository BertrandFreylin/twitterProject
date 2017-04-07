from django.conf.urls import url
from matcher import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^get_tweet_ratio/', views.get_tweet_ratio, name='get_tweet_ratio'),
    url(r'^get_popular_heroes/', views.get_popular_heroes, name='get_popular_heroes'),
    url(r'^get_support_heroes/', views.get_support_heroes, name='get_support_heroes'),
    url(r'^get_support_heroes_by_hero/', views.get_support_heroes_by_hero, name='get_support_heroes'),
    url(r'^get_countries_heroes/', views.get_countries_heroes, name='get_countries_heroes'),
    url(r'^get_fav_heroes_by_country/', views.get_fav_heroes_by_country, name='get_fav_heroes_by_country'),
    url(r'^get_fav_rt_hero/', views.get_fav_rt_hero, name='get_fav_rt_hero'),
]
