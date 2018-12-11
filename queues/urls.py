from django.conf.urls import url
from django.urls import path
from . import views



urlpatterns = [
    #url(r'^$', views.index, name='index'),
    path('', views.index, name='index'),
    path(r'mk_list', views.mk_list, name='mk_list'),
    url(r'queue_list/(?P<device_name>.+)/$', views.queue_list, name='queue_list'),
    url(r'^(?P<queue_id>[0-9]+)/$', views.detail_queue_data, name='detail'),
    url(r'^subjects/(?P<pk>[0-9]+)/(?P<deck>[0-9]+)/$',views.queue_list,),
    url(r'^queues.js$', views.queues_js),

    ]