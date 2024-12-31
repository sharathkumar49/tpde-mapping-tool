from django.contrib import admin
from django.urls import path, include
from .render import *
from .views import *

urlpatterns = [
    # Feed endpoints
    path("feed/list/", feed_list_view,name="feed_list_view"),
    path("feed/create/form/", feed_create_view, name="feed_create_view"),
    path("feed/create/", create_feed, name="create_feed"),
    path("feed/edit/<int:pk>", feed_edit_view, name="feed_edit_view"),

    # Feed Category endpoints
    path("feed/category/list/", feed_category_list_view, name="feed_category_list_view"),
    path("feed/category/create/form/", feed_category_create_view, name="feed_category_create_view"),
    path("feed/category/create/", create_feed_category, name="feed_category_create"),
    path("feed/category/edit/<int:pk>", feed_category_edit_view, name="feed_edit_view"),

    # user endpoints
    path("user/list/", user_list_view,name="user_list_view"),
    path("user/create/form/", user_create_view, name="user_create_view"),
    path("user/create/", create_user, name="create_feed"),
    path("user/profile/", user_profile_view, name="user_profile_view"),
    path("user/edit/view/<int:user_id>/", user_edit_view, name="user_edit_view"),
    path("user/edit/<int:user_id>/", user_edit, name="user_edit"),

    # Rest API's

    # Feed
    path("api/feed/list", FeedListAPIView.as_view(),name="feed_list_api"),
    path("api/feed/category/list", FeedCategoryListAPIView.as_view(), name="feed_category_list_api")
]
