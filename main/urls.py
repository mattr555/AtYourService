from django.conf.urls import patterns, url
from main import views, user_views, org_views

urlpatterns = patterns('',
    # user management
    url(r'^login/$', user_views.login_view, name='login'),
    url(r'^logout/', user_views.logout_view, name='logout'),
    url(r'^signup/', user_views.signup, name='signup'),
    url(r'^profile/change_loc/$', user_views.change_location, name='change_loc'),
    url(r'^profile/reset_pass/complete/$', user_views.finish_change_pass),
    url(r'^profile/change_pass/complete/$', user_views.finish_change_pass),
    url(r'^profile/$', user_views.user_profile, name='user_profile'),

    # organization management
    url(r'^manage/$', org_views.org_manage, name='org_manage'),
    url(r'^manage/org/(?P<pk>\d+)/$', org_views.org_edit, name='org_edit'),

    url(r'^list/(?P<page>\d+)/', views.list_events, name='list_page'),
    url(r'^list/$', views.list_events_one, name='list_events'),
    url(r'^event/(?P<pk>\d+)/', views.EventView.as_view(), name='event_detail'),
    url(r'^userevent/(?P<pk>\d+)/$', views.userevent_detail, name='userevent_detail'),
    url(r'^userevent/(?P<pk>\d+)/delete/', views.delete_userevent, name='userevent_delete'),
    url(r'^organization/(?P<pk>\d+)/', views.organization_detail, name='organization_detail'),
    url(r'^track/', views.track_events, name='track'),
    url(r'^$', views.home, name='home'),
)
