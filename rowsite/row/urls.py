from django.conf.urls import patterns, url
from row import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^athlete/(?P<athleteId>\d+)/$', views.detail, name='athlete_detail'),
    url(r'^athlete/new/', views.new, name='athlete_new'),
)
