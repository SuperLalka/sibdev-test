from django.conf.urls import url

from . import views


app_name = 'deals'
urlpatterns = [
    url(r'^deals/', views.DealsViewAPI.as_view(), name='deals'),

]
