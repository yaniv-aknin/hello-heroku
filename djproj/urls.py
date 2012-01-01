from django.conf import settings
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url('^$', 'django.views.generic.simple.direct_to_template', dict(template='index.html')),
    url(r'^static/(!(?P<digest>[0-9a-f]+)/)?(?P<path>.*)$', 'supstream.views.serve',
        {'document_root' : settings.STATIC_ROOT}),
)
