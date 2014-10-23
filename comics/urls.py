from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # Main site areas
    url(r'^$', 'xkcd.views.home', name='home'),
    url(r'^all_user_likes/$', 'xkcd.views.all_user_likes', name='all_user_likes'),
    url(r'^comics/$', 'xkcd.views.comics', name='comics'),
    url(r'^error/$', 'xkcd.views.error', name='error'),
    url(r'^profile/$', 'xkcd.views.profile', name='profile'),
    url(r'^random_search/$', 'xkcd.views.random_search', name='random_search'),

    # Register, log in, and logout
    url(r'^register/$', 'xkcd.views.register', name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    #Password reset
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    #Admin
    url(r'^admin/', include(admin.site.urls)),
)
