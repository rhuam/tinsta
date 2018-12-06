from django.conf.urls import url,include
from . import views
from rest_framework import routers



urlpatterns = [
    url(r'^$', views.index),
    url(
        r'^api/v1/users_fb/([a-zA-Z0-9]+)$',
        views.get_user_fb,
        name='get_user_fb'
    ),
    url(
        r'^api/v1/users_fb/$',
        views.post_login_facebook_tinder,
        name='post_login_facebook_tinder'
    ),
    url(
        r'^api/v1/users_insta/([a-zA-Z0-9]+)$',
        views.get_user_instagram,
        name='get_user_instagram'
    ),
    url(
        r'^api/v1/users_insta/$',
        views.post_login_instagram,
        name='post_login_instagram'
    ),
    url(
        # r'^api/v1/follow_insta/([a-zA-Z0-9_.+-]+)/([a-zA-Z0-9_.+-]+)$',
        r'^api/v1/follow_insta/$',
        views.post_follow_instagram,
        name='post_follow_instagram'
    ),
    url(
        r'^api/v1/dislike_tinder/$',
        views.post_dislike_tinder,
        name='post_dislike_tinder'
    ),
    url(
        r'^api/v1/users_tinder/([a-zA-Z0-9]+)$',
        views.post_update_tinder,
        name='post_update_tinder'
    ),
    url(
        r'^api/v1/users_people/([a-zA-Z0-9+_\-]+)$',
        views.get_user_people,
        name='get_user_people'
    )
]
