from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^AtYourService/', include('AtYourService.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^real_admin/', include(admin.site.urls)),
    url(r'^admin/', TemplateView.as_view(template_name='admin.html')),
    url(r'^humans\.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),
    url(r'^ajax/', include('ajax.urls')),
    url(r'^', include('main.urls', namespace='main')),
)
