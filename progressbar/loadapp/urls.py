from django.conf.urls import patterns, url

urlpatterns = patterns('loadapp.views',
    url(r'^home/$', 'load_home', name = 'load_home'),
    url(r'^status/$', 'load_status', name = 'load_status'),
    url(r'^status/all/$', 'load_status_all', name = 'load_status_all'),
    url(r'^status/(?P<sid>\d+)/$', 'load_status_view', name='status_view'),
    url(r'^status/(?P<paramfile_id>\d+)/(?P<load_status>\w+)/$', 'load_status_table', name='loadstatus_table'),
    url(r'^progress/$', 'progress_bar', name = 'progress_bar'),

    )
