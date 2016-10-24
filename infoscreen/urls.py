from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.inforscreen, name="infoscreen")
]
