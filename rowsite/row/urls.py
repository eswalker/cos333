from django.conf.urls import patterns, url
from row import views

urlpatterns = patterns('',
    url(r'^$', views.athlete_index, name='index'),
    url(r'^athletes/$', views.athlete_index, name='athlete_index'),
    url(r'^athlete/(?P<athlete_id>\d+)/$', views.athlete_detail, name='athlete_detail'),
    url(r'^athlete/add/', views.athlete_add, name='athlete_add'),
    url(r'^practice/(?P<practice_id>\d+)/$', views.practice_detail, name='practice_detail'),
    url(r'^practices/$', views.practice_index, name='practice_index'),
    url(r'^practice/add/', views.practice_add, name='practice_add'),
)