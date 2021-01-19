from django.conf.urls import url
from django.urls import include

from rest_framework.routers import DefaultRouter
from . import views


routerAPI = DefaultRouter()
routerAPI.register(r'deals', views.DealsViewSet, basename='deals')


app_name = 'deals'
urlpatterns = [
    url(r'^api/', include(routerAPI.urls)),
]
