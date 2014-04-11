from django.conf.urls import patterns, url
from row import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),

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
    url(r'^piece/(?P<piece_id>\d+)/result/add/$', views.result_add, name='piece_result_add'),
    url(r'^athlete/(?P<athlete_id>\d+)/result/add/$', views.result_add, name='athlete_result_add'),
    url(r'^result/(?P<id>\d+)/edit/$', views.result_edit, name='result_edit'),
    url(r'^result/(?P<id>\d+)/delete/$', views.result_delete, name='result_delete'),

    url(r'^accounts/login/', views.user_login, name="login"),
    url(r'^accounts/register/', views.user_register, name="register"),
    url(r'^accounts/logout/', views.user_logout, name="logout"),

    url(r'^boats/$', views.boat_index, name='boat_index'),
    url(r'^boat/add/$', views.boat_add, name='boat_add'),
    url(r'^boat/(?P<id>\d+)/edit/$', views.boat_edit, name='boat_edit'),
    url(r'^boat/(?P<id>\d+)/delete/$', views.boat_delete, name='boat_delete'),

    url(r'^lineup/add/$', views.lineup_add, name='lineup_add'),
    url(r'^piece/(?P<piece_id>\d+)/lineup/add/$', views.lineup_add, name='piece_lineup_add'),
    url(r'^lineup/(?P<id>\d+)/edit/$', views.lineup_edit, name='lineup_edit'),
    url(r'^lineup/(?P<id>\d+)/delete/$', views.lineup_delete, name='lineup_delete'),

    url(r'^erg', views.erg, name='erg'),

    url(r'^denied/$', views.denied, name='denied'),



    url(r'^json/athletes/$', views.json_athletes, name='json_athletes'),
    url(r'^json/practices/$', views.json_practices, name='json_practices'),
    url(r'^json/practice/(?P<id>\d+)/lineups/$', views.json_practice_lineups, name='json_practice_lineups'),
    url(r'^json/boats/$', views.json_boats, name='json_boats'),
    url(r'^json/login/$', views.json_login, name='json_login'),

    url(r'^athletes/csv/$', views.athlete_index_csv, name='athlete_index_csv'),

    url(r'^piece/add/$', views.piece_add, name='piece_add'),
    url(r'^practice/(?P<practice_id>\d+)/piece/add/$', views.piece_add, name='practice_piece_add'),
    url(r'^piece/(?P<id>\d+)/edit/$', views.piece_edit, name='piece_edit'),
    url(r'^piece/(?P<id>\d+)/delete/$', views.piece_delete, name='piece_delete'),
    url(r'^piece/(?P<piece_id>\d+)/$', views.piece_detail, name='piece_detail'),

    url(r'^piece/(?P<piece_id>\d+)/note/add/$', views.note_add, name='piece_note_add'),
    url(r'^practice/(?P<practice_id>\d+)/note/add/$', views.note_add, name='practice_note_add'),
    url(r'^note/(?P<id>\d+)/$', views.note_detail, name='note_detail'),
    url(r'^note/(?P<id>\d+)/delete/$', views.note_delete, name='note_delete'),
    url(r'^note/(?P<id>\d+)/edit/$', views.note_edit, name='note_edit'),
)