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

    url(r'^profile/reset_pass/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/profile/reset_pass/done/',
         'template_name': 'myregistration/password_reset_form.html'},
        name="reset_password"),
    url(r'^profile/reset_pass/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'myregistration/password_reset_done.html'}),
    url(r'^profile/reset_pass/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/profile/reset_pass/complete/',
         'template_name': 'myregistration/password_reset_confirm.html'}),

    url(r'^', include('main.urls', namespace='main')),
)

