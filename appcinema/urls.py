from django.conf.urls import include, url
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from appcinema.api.views import MovieDetailView, add_tentative_seat, booking_create_view, confirm_booking, \
    BookingHistoryView

admin.autodiscover()


urlpatterns = [
    url(r'^api/', include('appcinema.api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^movies/$', TemplateView.as_view(template_name='movies.html')),
    url(r'^movies/(?P<pk>[0-9]+)/$', login_required(MovieDetailView.as_view())),
    url(r'^movies/update/(?P<movie_pk>[0-9]+)/(?P<seat_id>[0-9]+)/$', add_tentative_seat, name='movie-update'),
    url(r'^create_booking/$', booking_create_view, name='create_booking'),
    url(r'^confirm_booking/$', confirm_booking, name='confirm_booking'),
    url(r'^history/', login_required(BookingHistoryView.as_view()), name='booking_history'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
]

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += [
        url(r'^(?P<path>favicon\..*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], serve, dict(insecure=True)),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
