from django.conf.urls import url

from printerqueue import views

urlpatterns=[
    url(r'^$', views.landing, name="queue"),

]
