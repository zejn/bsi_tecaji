from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = patterns('',
    url(r'^tecaj/$', 'bsi_tecaji.views.get_tecaj'),
    url(r'^$', lambda r: HttpResponse('<a href="/tecaj/?datum=2015-06-12&oznaka=USD">Example</a>')),
)
