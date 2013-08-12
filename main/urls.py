from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from main import views

urlpatterns = patterns('',
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^list/(?P<page>\d+)/', views.list_events, name='list_page'),
    url(r'^list/$', views.list_events_one, name='list_events'),
    url(r'^event/(?P<pk>\d+)/', views.EventView.as_view(), name='event_detail'),
    url(r'^userevent/(?P<pk>\d+)/$', views.userevent_detail, name='userevent_detail'),
    url(r'^userevent/(?P<pk>\d+)/delete/', views.delete_userevent, name='userevent_delete'),
    url(r'^organization/(?P<pk>\d+)/', views.organization_detail, name='organization_detail'),
    url(r'^track/', views.track_events, name='track'),
    url(r'^profile/change_loc/$', views.change_location, name='change_loc'),
    url(r'^profile/change_pass/$', views.change_password, name='change_password'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^$', views.home, name='home'),
)
