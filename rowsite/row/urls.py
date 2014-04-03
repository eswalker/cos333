from django.conf.urls import patterns, url
from row import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),

    url(r'^athlete/add/$', views.athlete_add, name='athlete_add'),
    url(r'^athletes/$', views.athlete_index, name='athlete_index'),
    url(r'^athlete/(?P<athlete_id>\d+)/$', views.athlete_detail, name='athlete_detail'),
    url(r'^athlete/(?P<athlete_id>\d+)/edit/$', views.athlete_edit, name='athlete_edit'),
    url(r'^athlete/(?P<id>\d+)/delete/$', views.athlete_delete, name='athlete_delete'),

    url(r'^weight/add/$', views.weight_add, name='weight_add'),
    url(r'^athlete/(?P<athlete_id>\d+)/weight/add/$', views.weight_add, name='athlete_weight_add'),
    url(r'^weight/(?P<id>\d+)/edit/$', views.weight_edit, name='weight_edit'),
    url(r'^weight/(?P<id>\d+)/delete/$', views.weight_delete, name='weight_delete'),


    url(r'^practice/add/$', views.practice_add, name='practice_add'),
    url(r'^practice/(?P<practice_id>\d+)/$', views.practice_detail, name='practice_detail'),
    url(r'^practices/$', views.practice_index, name='practice_index'),
    url(r'^practice/(?P<id>\d+)/edit/$', views.practice_edit, name='practice_edit'),
    url(r'^practice/(?P<id>\d+)/delete/$', views.practice_delete, name='practice_delete'),
    
    url(r'^result/add/$', views.result_add, name='result_add'),
    url(r'^practice/(?P<practice_id>\d+)/result/add/$', views.result_add, name='practice_result_add'),
    url(r'^athlete/(?P<athlete_id>\d+)/result/add/$', views.result_add, name='athlete_result_add'),
    url(r'^result/(?P<id>\d+)/edit/$', views.result_edit, name='result_edit'),
    url(r'^result/(?P<id>\d+)/delete/$', views.result_delete, name='result_delete'),

    url(r'^accounts/login/', views.user_login, name="login"),
    url(r'^accounts/register/', views.user_register, name="register"),
    url(r'^accounts/logout/', views.user_logout, name="logout"),

    url(r'^boats/$', views.boat_index, name='boat_index'),
    url(r'^boat/add/$', views.boat_add, name='boat_add'),
    url(r'^boat/(?P<id>\d+)/delete/$', views.boat_delete, name='boat_delete'),
)