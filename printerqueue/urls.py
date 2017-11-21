from django.conf.urls import url

from printerqueue import views

app_name = "printerqueue"

urlpatterns=[
    url(r'^$', views.landing, name="queue"),
    url(r'^all$', views.all_queues, name="all"),
    url(r'^create$', views.create, name="create")

]
