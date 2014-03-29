from django.conf.urls import patterns, url
from row import views

urlpatterns = patterns('',
    url(r'^$', views.athlete_index, name='index'),
    url(r'^athlete/(?P<athleteId>\d+)/$', views.athlete_detail, name='athlete_detail'),
    url(r'^athlete/new/', views.athlete_new, name='athlete_new'),
    url(r'^practice/(?P<practiceId>\d+)/$', views.practice_detail, name='practice_detail'),

)
