from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^process$', views.process),
    url(r'^quotes$', views.quotes),
    url(r'^favquote/(?P<id>\d+)$', views.favquote),
    url(r'^user$', views.user),
    url(r'^logout$', views.logout),
]
