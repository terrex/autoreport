from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<pk>.*)/$', 'autoreport.views.handle_report'),
    (r'^$', 'autoreport.views.handle_reports'),
)
