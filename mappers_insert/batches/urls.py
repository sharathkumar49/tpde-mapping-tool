from django.contrib import admin
from django.urls import path, include
from .render import *
from .views import *
from standard.views import login_check

urlpatterns = [
    # Feed endpoints
    path("data/upload/form/", data_upload_view,name="data_upload_view"),
    path("data/upload/", data_upload, name="data_upload"),
    path("batch/list/", batch_list_view, name="batch_list_view"),
    path("batch/search/filter/", batch_filter, name="batch_filter"),
    path("validate/user/", login_check, name="login_check"),
    path("record/view/<int:batch_id>/", batch_data_view, name="batch_data_view"),
    path("record/detail/view/<int:batch_id>/<int:mappers_id>/", record_detail_view, name="record_detail_view"),
    path("record/edit/view/<int:batch_id>/<int:mappers_id>/", record_edit_view, name="record_edit_view"),
    path("record/update/<int:batch_id>/<int:mappers_id>/", record_update, name="record_update"),
    path("batch/validate/<int:batch_id>/", validate_batch, name="validate_batch"),
    path("batch/update/search/view/", batch_update_search_view, name="batch_update_search_view"),
    path("batch/record/search/", record_search, name="record_search"),
    path("batch/record/search/filter/", RecordSearchFilterAPI.as_view(), name="record_search_filter"),
    path("batch/update/view/", bulk_update_view, name="bulk_update_view"),
    path("batch/update/", batch_update, name="batch_update"),
    path("batch/record/update/", batch_record_update, name="batch_record_update"),
    path("data/insert/view/", data_insert_view, name="data_insert_view"),
    path("data/insert/", data_insert, name="data_insert"),

    


    # templates
    path("csv/template/list/", template_list_view, name="template_list_view"),
    path("csv/template/create/view/", template_create_view, name="template_create_view"),
    path("csv/template/edit/view/<int:template_id>/", template_edit_view, name="template_edit_view"),
    path("csv/template/edit/<int:template_id>/", template_edit, name="template_edit"),
    path("csv/template/create/", create_templates, name="create_templates"),
    path("csv/template/download/<int:template_id>", download_template, name="download_template"),
    # path("data/search/", report_search, name="report_search")
]
