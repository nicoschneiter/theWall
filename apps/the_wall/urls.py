from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index),
        url(r'^register/$', views.register),
        url(r'^login/$', views.login),
        url(r'^wall/$', views.wall),
        url(r'^wall/delete/$', views.delete),
        url(r'^wall/delete_comment/$', views.delete_comment),
        url(r'^create/$', views.create, name='create'),
        url(r'^create_comment/$', views.create_comment, name='create_comment'),
        url(r'^wall/logout/$', views.logout),
        ]
