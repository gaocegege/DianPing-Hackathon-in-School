__author__ = 'jingyuan'

from django.conf.urls import patterns, include, url

urlpatterns=patterns('',
    url(r'^$','wechat.views.index'),

)