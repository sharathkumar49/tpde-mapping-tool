from django.contrib import admin
from django.urls import path, include
from .render import *
from .views import *
from standard.views import login_check

urlpatterns = [
    # Feed endpoints
    path("data/export/form/", data_export_form,name="data_export_form"),
    path("log/report/search/view/", log_search_view,name="log_search_view"),
    path("logs/", log_search, name='log_search')
]
