from django.conf.urls import patterns, include, url

from django.contrib import admin
from row import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rowsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', views.index, name='index'),
    url(r'^athlete/(?P<athleteId>\d+)/$', views.detail, name='athlete-detail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^athlete/new/', views.new, name='athlete_new')
)
