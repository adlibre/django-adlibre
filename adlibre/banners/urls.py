from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^banner_list/$', 'views.banner_list', name='banner_list'),
)