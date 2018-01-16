from django.conf.urls import url, include

from printerqueue import views

app_name = "printerqueue"

urlpatterns=[
    url(r'^$', views.index, name="queue"),
    url(r'^all$', views.all_queues, name="all"),
    url(r'^create$', views.create, name="create"),
    url(r'^(?P<queue_id>.+)/', include([
        url(r'^view$', views.show, name="view"),
        url(r'^add$', views.add_to_queue, name="add")
    ])),
    url(r'^gettimes/(?P<queue_id>[0-9]+)/(?P<date>.*)$', views.get_times, name="get_times"),
    url(r'^getendtimes/(?P<queue_id>[0-9]+)/(?P<date>.*)/(?P<time>.*)$', views.get_end_times, name="get_end_times"),


]
