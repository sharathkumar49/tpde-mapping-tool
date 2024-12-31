"""
URL configuration for mappers_insert project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from masters.render import *
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Episyche Technologies",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("masters/", include('masters.urls')),
    path("batches/", include('batches.urls')),
    path("reports/", include('reports.urls')),
    path("", login_view, name='login_view'),
    # path("create/", record_create, name="record"),
    path("user/login/", login_user, name="login_user"),
    path("user/logout/", user_logout, name="user_logout"),
    path("user/password/update/", user_password_update, name="user_password_update"),
    path("dashboard/", dashboard_view, name="dashboard_view"),
    path("batches/", batch_list_view, name='batch_view'),
    path("batch/create", batch_create_view, name='batch_create_view'),
    path("feed/create", feed_create_view, name="feed_create_view"),
    path("feed_category", feed_category_list_view, name="feed_category_list_view"),
    path("feed_category/create", feed_category_create_view, name="feed_category_create_view"),
    path("csv/template/search_view", csv_template_search_view, name="csv_template_search_view"),
    
]
