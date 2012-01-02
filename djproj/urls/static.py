from django.conf import settings
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^(!(?P<digest>[0-9a-f]+)/)?(?P<path>.*)$', 'supstream.views.serve', {'document_root' : settings.STATIC_ROOT}),
)
