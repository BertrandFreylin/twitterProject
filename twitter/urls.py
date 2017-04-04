from django.conf.urls import url
from matcher import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
]
