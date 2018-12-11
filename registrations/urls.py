from django.conf.urls import url
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [

    path(r'tower_list', views.index, name='index'),
    #url(r'^(?P<ap_id>[0-9]+)/$', views.registration_data, name='reg_data'),
    url(r'reg_name/(?P<reg_name>.+)/$',views.reg_name_data, name='reg_name_data'),
    url(r'aps/(?P<loc_id>.+)/$',views.towers, name='towers'),
    url(r'ap/(?P<ap_id>.+)/$', views.registration_data, name='reg_data'),
    url(r'^queries/', views.queries),
    url(r'^customers/', views.CustomerList.as_view()),
    url(r'^problems/', views.ProblemList.as_view()),
    #url(r'towers.js$', views.towers_js),
    #url(r'aps.js$', views.aps_js),
    #url(r'registrations.js$', views.registrations_js),
    ]