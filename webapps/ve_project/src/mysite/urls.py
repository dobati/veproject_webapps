# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 've.views.index', name='index'),
    url(r'^about_us/$', 've.views.about_us', name='about_us'),
    url(r'^about_ve/$', 've.views.about_ve', name='about_ve'),
    url(r'^general1/$', 've.views.general1', name='general1'),
    url(r'^general2/$', 've.views.general2', name='general2'),
    url(r'^general3/$', 've.views.general3', name='general3'),
    url(r'^books1/$', 've.views.books1', name='books1'),
    url(r'^books2/$', 've.views.books2', name='books2'),
    url(r'^books3/$', 've.views.books3', name='books3'),
    url(r'^movies1/$', 've.views.movies1', name='movies1'),
    url(r'^movies2/$', 've.views.movies2', name='movies2'),
    url(r'^movies3/$', 've.views.movies3', name='movies3'),
    url(r'^legaltexts1/$', 've.views.legaltexts1', name='legaltexts1'),
    url(r'^legaltexts2/$', 've.views.legaltexts2', name='legaltexts2'),
    url(r'^legaltexts3/$', 've.views.legaltexts3', name='legaltexts3'),
    url(r'^admin/', include(admin.site.urls)),
)