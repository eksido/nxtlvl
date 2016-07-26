from django.conf.urls import patterns, include, url
from django.contrib.auth import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from .views import notimplemented, UsersView


admin.autodiscover()
urlpatterns = patterns('',
                       url(r'^users[/]?$', UsersView.as_view(), name='user-view'),
                       url(r'^users/(?P<user_id>[\w]+)', UsersView.as_view(), name='user-get-view'),
                       url('', notimplemented, name='index'),
)
