from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^insert$', views.insert),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_item/create$', views.create_item),
    url(r'^add_item$', views.add_item),
    url(r'^addwish/(?P<id>\d+)$', views.addwish),
    url(r'^wish_item/(?P<id>\d+)$', views.wishitems),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^logout$', views.logout)
]