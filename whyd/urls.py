"""whyd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from api import views

from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'playlists', views.PlaylistViewSet, 'playlists')
router.register(r'follows', views.FollowViewSet, 'follows')
router.register(r'likes', views.LikeViewSet, 'likes')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^me/', views.current_user),
    url(r'^stream/', views.StreamList.as_view()),

    # GET, UPDATE, DELETE tracks
    url(r'^tracks/(?P<pk>\d+)/', views.TrackView.as_view(), name='track'),

    # GET tracks
    url(r'^tracks/', views.ListTrackView.as_view(), name='tracks'),

    # POST, GET tracks from playlist
    url(r'^playlists/(?P<playlist_id>\d+)/tracks/', views.ListPlaylistTracksView.as_view(), name='playlist-tracks'),

    # DELETE track from playlist
    url(r'^playlists/(?P<playlist_id>\d+)/tracks/(?P<track_id>\d+)', views.DeletePlaylistTrackView.as_view(), name='delete-playlist-tracks'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),

#    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
]
