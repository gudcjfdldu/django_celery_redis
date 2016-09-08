from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login_handler, name='login'),
    url(r'^signup/$', views.register, name='signup'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout_handler, name='logout'),
    url(r'^visits/(?P<userid>\d+)$', views.show_visit, name='show_visit'),
]
