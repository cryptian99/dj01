from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
#from django.conf import settings
from django.contrib import admin
#from settings import STATIC_URL, STATIC_ROOT
from premier.views import show_teams, show_club, show_player, edit_player, delete_player,\
    show_results, show_fixtures, show_team_stats

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj01.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/$', include(admin.site.urls)),
        (r'^teams/$', show_teams),
        (r'^club/(\d{1,2})/$', show_club),
        (r'^result/(\d{1,2})/$', show_results),
        (r'^fixture/(\d{1,2})/$', show_fixtures),
        (r'^teamstats/(\d{1,2})/$', show_team_stats),
        (r'^club/(\d{1,2})/view/(\d{1,2})/$', show_player),
        (r'^club/(\d{1,2})/edit/(\d{1,2})/$', edit_player),
        (r'^club/(\d{1,2})/delete/(\d{1,2})/$', delete_player),
)

