from django.conf.urls import patterns, include, url
from django.contrib.auth import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from .views import notimplemented

admin.autodiscover()
urlpatterns = patterns('',
                url('', notimplemented, name='index'),
                url(r'^user$', notimplemented, name='index'),
)
