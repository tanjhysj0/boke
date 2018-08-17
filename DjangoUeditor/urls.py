#coding:utf-8
from django import VERSION
if VERSION[0:2]>(1,3):
    #from django.conf.urls import patterns, url
    # from django.conf.urls import *
    from django.conf.urls import *
    #from boke.view import hello
else:
    pass
    from django.conf.urls.defaults import patterns, url


#from views import get_ueditor_controller
from DjangoUeditor.views import get_ueditor_controller
urlpatterns = [
    url(r'^controller/$', get_ueditor_controller)
]