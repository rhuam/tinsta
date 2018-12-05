from django.conf.urls import url
from . import views

urlpatterns = [
    # url(
    #     r'^api/v1/users_fb/(?P<pk>[0-9]+)$',
    #     views.get_delete_update_user_fb,
    #     name='get_delete_update_FB'
    # ),
    url(
        r'^api/v1/users_fb/$',
        views.get_post_user_fb,
        name='get_post_FB'
    ),
    # url(
    #     r'^api/v1/users_insta/(?P<pk>[0-9]+)$',
    #     views.get_delete_update_user_insta,
    #     name='get_delete_update_user_insta'
    # ),
    url(
        r'^api/v1/users_insta/$',
        views.get_post_user_insta,
        name='get_post_user_insta'
    ),
    # url(
    #     r'^api/v1/users_tinder/(?P<pk>[0-9]+)$',
    #     views.get_delete_update_user_tinder,
    #     name='get_delete_update_user_tinder'
    # ),
    url(
        r'^api/v1/users_tinder/$',
        views.get_post_user_tinder,
        name='get_post_user_tinder'
    ),
    url(
        r'^api/v1/users_people/(?P<token>[a-zA-Z0-9+_\-]+)$',
        views.get_post_user_people,
        name='get_post_user_people'
    ),
    # url(
    #     r'^api/v1/users_people/$',
    #     views.get_post_user_people,
    #     name='get_post_user_people'
    # ),
url(
        r'^api/v1/insta_follow/(?P<token>[a-zA-Z0-9+_\-]+)/(?P<insta_user>[a-zA-Z0-9+_\-]+)/(?P<user_follow>[a-zA-Z0-9+_\-]+)$',
        views.get_follow_user,
        name='get_follow_user'
    ),
]