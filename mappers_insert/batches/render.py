import csv
from django.http import Http404, HttpResponse, JsonResponse
from masters.serializers import FeedCategory, Feeds, FeedCategoryListSerializer, FeedListSerializer
from django.shortcuts import render, redirect
from .views import DataValidation, BatchRecordSearchAPI, Headers, BatchUpdateAPIview
from django.contrib.auth.decorators import login_required
from .function import report_template_create_parser, report_template_update_parser, get_report_details
import random
from django.conf import settings 
import json
from standard.function import get_feed_categories, get_feeds, Error
from standard.variables import Variables
from .serializers import ReportTemplateCreateSerializer, BatchListSerializer, FeedCategoryListSerializer, FeedListSerializer, ReportTemplateListSerializer, NTAccountListSerializer, MappersListSerializer
from .models import ReportTemplates, NTAccountMapping, PrivateiAccMasterMapping, Batches
import os
from masters.decorator import create_exception_log
from .function import get_model_name
import pandas as pd

class GetMasters:
    """
    A class to get master data for feeds and categories.
    """
    
    @staticmethod
    def get_feed(self):
        """
        Get active feeds.

        Args:
            self: The request object.

        Returns:
            Serialized data of active feeds.
        """
        feeds = Feeds.objects.filter(Active=1)
        return FeedListSerializer(feeds, many=True).data
    
    @staticmethod
    def get_category(self):
        """
        Get active categories.

        Args:
            self: The request object.

        Returns:
            Serialized data of active categories.
        """
        categories = FeedCategory.objects.filter(Active=True)
        return FeedCategoryListSerializer(categories, many=True).data

validation_class = DataValidation()    

@login_required(login_url="/batches/validate/user/")
def data_upload_view(request):
    """
    Render the data upload view.

    Args:
        request: The request object.

    Returns:
        Rendered HTML page for data upload.
    """
    try:
        feeds = GetMasters.get_feed(request)
        categories = GetMasters.get_category(request)
        return render(request, 'DataUpload.html', {
            'screen_type': 'create_view',
            'feed': feeds,
            'category': categories
        })
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def data_insert_view(request):
    """
    Render the data insert view.

    Args:
        request: The request object.

    Returns:
        Rendered HTML page for data insert.
    """
    try:
        feeds = GetMasters.get_feed(request)
        categories = GetMasters.get_category(request)
        return render(request, 'DataInsert.html', {
            'screen_type': 'create_view',
            'feed': feeds,
            'category': categories
        })
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def batch_update_search_view(request):
    """
    Render the batch update search view.

    Args:
        request: The request object.

    Returns:
        Rendered HTML page for batch update search.
    """
    try:
        feeds = GetMasters.get_feed(request)
        categories = GetMasters.get_category(request)
        return render(request, 'BatchUpdate.html', {
            'screen_type': 'search_view',
            'feed': feeds,
            'category': categories
        })
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def record_search(request):
    """
    Perform record search and render the results.

    Args:
        request: The request object.

    Returns:
        Rendered HTML page with search results.
    """
    try:
        response = BatchRecordSearchAPI().post(request)
        print (response)
        if response.status_code == 200:
            data = response.data
            return render(request, 'BatchUpdate.html', {'screen_type': 'bulk_update', 'data': data})
        return render(request, 'BatchUpdate.html', {'screen_type':"search_view"})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def template_list_view(request):
    """
    Render the template list view with filters.

    Args:
        request: The request object.

    Returns:
        Rendered HTML page with template list.
    """
    try:
        params = request.POST.dict()
        feed_id = params.get("feed_id")
        feed_category_id = params.get("feed_category_id")
        
        # Filter based on feed_id and feed_category_id
        filters = {}
        if feed_id:
            filters['FeedID_id'] = feed_id
        if feed_category_id:
            filters['FeedCategoryID_id'] = feed_category_id
        
        template_obj = ReportTemplates.objects.filter(Active=1, **filters)
        templates = ReportTemplateListSerializer(template_obj, many=True).data
        
        feeds = GetMasters.get_feed(request)
        categories = GetMasters.get_category(request)
        return render(request, "CSVTemplates.html", context={
            "templates": templates, 
            "feeds": feeds, 
            "categories": categories, 
            'feed_id': feed_id, 
            'feed_category_id': feed_category_id
        })
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def template_create_view(request):
    """
    Render the template create view.

    Args:
        request: The request object.

    Returns:
        Rendered HTML page for template creation.
    """
    try:
        feeds = GetMasters.get_feed(request)
        categories = GetMasters.get_category(request)
        validation_types = ReportTemplates.validation_type
        return render(request, "CSVTemplates.html", context={
            "screen_type": "create_view", 
            "feeds": feeds, 
            "categories": categories, 
            "validation_types": validation_types,
            'range': range(20)
        })
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})


@login_required(login_url="/batches/validate/user/")
def template_edit_view(request, template_id):
    """
    Render the template edit view.

    Args:
        request: The request object.
        template_id: The ID of the template to edit.

    Returns:
        Rendered HTML page for template editing.
    """
    try:
        feeds = GetMasters.get_feed(request)
        categories = GetMasters.get_category(request)
        template_obj = ReportTemplates.objects.filter(TemplateID=template_id).first()
        
        if template_obj:
            template_data = ReportTemplateListSerializer(template_obj)
        else:
            template_data = {}
        
        validation_types = ReportTemplates.validation_type
        return render(request, "CSVTemplates.html", context={
            "screen_type": "create_view", 
            "template": template_data.data, 
            "validation_types": validation_types, 
            "feeds": feeds, 
            "categories": categories, 
            'range': range(20)
        })
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})


@login_required(login_url="/batches/validate/user/")
def template_search(request):
    """
    Perform template search and render the results.

    Args:
        request: The request object.

    Returns:
        Rendered HTML page with search results.
    """
    try:
        params = request.POST.dict()
        feed_id = params.get("feed_id")
        feed_category_id = params.get("feed_category_id")
        
        # Similar to template_list_view, handle filters
        filters = {}
        if feed_id:
            filters['FeedID_id'] = feed_id
        if feed_category_id:
            filters['FeedCategoryID_id'] = feed_category_id
        
        template_obj = ReportTemplates.objects.filter(Active=1, **filters)
        templates = ReportTemplateListSerializer(template_obj, many=True).data
        
        feeds = GetMasters.get_feed(request)
        categories = GetMasters.get_category(request)
        return render(request, "CSVTemplates.html", context={
            "screen_type": "create_view", 
            "templates": templates, 
            "feeds": feeds, 
            "categories": categories, 
            'feed_id': feed_id, 
            'feed_category_id': feed_category_id, 
            'range': range(20)
        })
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def data_upload(request):
    """
    Handles the data upload process.

    Fetches form data, validates it, and saves it to the appropriate mapping table.
    Generates a batch number and saves the batch record.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect to the appropriate URL based on the success or failure of the operation.
    """
    try:
        print("data upload")

        # Fetch form data and related template
        feed_id = request.POST.get('FeedID')
        category_id = request.POST.get("FeedCategoryID")
        report_obj = ReportTemplates.objects.get(FeedID=int(feed_id), FeedCategoryID=int(category_id), Active=1)
        validation_type = report_obj.ValidationType

        # Choose response type based on validation type
        if validation_type in ['nt_acc_mapping']:
            response = validation_class.nt_account_mapping(request)
        else:
            response = validation_class.mappers_insert(request)
        response_data = response.data
        if len(response_data) > 0:
            # Generate batch number and save batch record
            batch_no = "MSCI" + str(random.randint(10001, 99999))
            batch_obj = Batches.objects.create(
                BatchNo=batch_no, 
                FeedID_id=int(feed_id), 
                FeedCategoryID_id=int(category_id),
                RecordCount=len(response_data),
                Configuration_id=report_obj.TemplateID
            )

            # Save data to the appropriate mapping table
            for data in response_data:
                if 'error_col' in data:
                    del data['error_col']
                data['BatchID_id'] = batch_obj.BatchID
                data['CreatedID_id'] = request.user.id
                data['UpdatedID_id'] = request.user.id
                
                # Choose mapping model dynamically
                if data.get('Error') != '':
                    if validation_type in ['nt_acc_mapping']:
                        mappers_obj = NTAccountMapping(**data)
                    else:
                        print(data)
                        mappers_obj = PrivateiAccMasterMapping(**data)
                        print(mappers_obj)
                    mappers_obj.save()

            return redirect(f"/batches/record/view/{batch_obj.BatchID}/?success=true")
        else:
            return redirect(f"/batches/data/upload/form/?success=false")
    
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def batch_list_view(request):
    """
    Displays a list of batches.

    Fetches batches with status 0 and renders them in the Batch.html template.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML page with the list of batches.
    """
    try:
        batches = Batches.objects.filter(Status=0)
        serializers = BatchListSerializer(batches, many=True)
        return render(request, 'Batch.html', {'screen_type': 'list_view', 'batches': serializers.data})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def batch_data_view(request, batch_id):
    """
    Displays the data of a specific batch.

    Fetches batch data and related mappers data based on the validation type.

    Args:
        request: The HTTP request object.
        batch_id: The ID of the batch to view.

    Returns:
        A rendered HTML page with the batch data.
    """
    try:
        batch_data = Batches.objects.prefetch_related('Configuration').get(pk=batch_id)
        batch_serializer = BatchListSerializer(batch_data)
        
        validation_type = batch_data.Configuration.ValidationType
        if validation_type == 'nt_acc_mapping':
            mappers_data = NTAccountMapping.objects.filter(BatchID=batch_id, Active=True)
            mappers_serializer = NTAccountListSerializer(mappers_data, many=True)
        else:
            mappers_data = PrivateiAccMasterMapping.objects.filter(BatchID=batch_id, Active=True)
            mappers_serializer = MappersListSerializer(mappers_data, many=True)
        
        return render(request, "Batch.html", context={"data": mappers_serializer.data, "batch": batch_serializer.data, "screen_type": "data_view"})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def record_detail_view(request, batch_id, mappers_id):
    """
    Displays the details of a specific record.

    Fetches batch and related mappers data based on the validation type.

    Args:
        request: The HTTP request object.
        batch_id: The ID of the batch.
        mappers_id: The ID of the mappers record.

    Returns:
        A rendered HTML page with the record details.
    """
    try:
        batch = Batches.objects.prefetch_related('Configuration').get(BatchID=batch_id)
        batch_serializer = BatchListSerializer(batch)
        
        validation_type = batch.Configuration.ValidationType
        if validation_type == 'nt_acc_mapping':
            mappers_data = NTAccountMapping.objects.filter(MappingID=mappers_id)
            serializer = NTAccountListSerializer(mappers_data, many=True)
        else:
            mappers_data = PrivateiAccMasterMapping.objects.filter(MappingID=mappers_id)
            serializer = MappersListSerializer(mappers_data, many=True)
        
        return render(request, "Batch.html", context={"screen_type": "detail_view", 'batch': batch_serializer.data, "data": serializer.data[0]})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def record_edit_view(request, batch_id, mappers_id):
    """
    Displays the edit view for a specific record.

    Fetches batch and related mappers data based on the validation type.

    Args:
        request: The HTTP request object.
        batch_id: The ID of the batch.
        mappers_id: The ID of the mappers record.

    Returns:
        A rendered HTML page with the record edit view.
    """
    try:
        batch = Batches.objects.prefetch_related('Configuration').get(BatchID=batch_id)
        batch_serializer = BatchListSerializer(batch)
        
        validation_type = batch.Configuration.ValidationType
        if validation_type == 'nt_acc_mapping':
            mappers_data = NTAccountMapping.objects.filter(MappingID=mappers_id)
            serializer = NTAccountListSerializer(mappers_data, many=True)
        else:
            mappers_data = PrivateiAccMasterMapping.objects.filter(MappingID=mappers_id)
            serializer = MappersListSerializer(mappers_data, many=True)
        
        return render(request, "BatchEditView.html", context={'batch': batch_serializer.data, "data": serializer.data[0]})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def record_update(request, batch_id, mappers_id):
    """
    Updates a specific record.

    Fetches the record based on the validation type and updates it with the provided data.

    Args:
        request: The HTTP request object.
        batch_id: The ID of the batch.
        mappers_id: The ID of the mappers record.

    Returns:
        A redirect to the record detail view.
    """
    try:
        params = request.POST.dict()
        del params['csrfmiddlewaretoken']
        batch_obj = Batches.objects.get(pk=batch_id)
        validation_type = batch_obj.Configuration.ValidationType
        # Using a more efficient query
        if batch_id and mappers_id:
            record = NTAccountMapping.objects.filter(MappingID=mappers_id) if validation_type=='nt_acc_mapping' else PrivateiAccMasterMapping.objects.filter(MappingID=mappers_id)
            print(record)
            if record:
                record.update(**params)
                record[0].save()
        return redirect(f"/batches/record/detail/view/{batch_id}/{mappers_id}/")
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def batch_filter(request):
    """
    Filters batches based on status.

    Fetches batches with the specified status and renders them in the Batch.html template.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML page with the filtered list of batches.
    """
    try:
        status = request.POST.get("status")
        batches = Batches.objects.filter(Status=status) if status else Batches.objects.all()
        serializers = BatchListSerializer(batches, many=True)
        return render(request, 'Batch.html', {'screen_type': 'list_view', 'batches': serializers.data, 'status': status})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def create_templates(request):
    """
    Creates new report templates.

    Fetches form data and creates a new report template if it does not already exist.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect to the template creation view or a rendered HTML page with an error message.
    """
    try:
        feed_id = request.POST.get("feed_id")
        feed_category_id = request.POST.get("feed_category_id")
        report_obj = ReportTemplates.objects.filter(FeedID_id=int(feed_id), FeedCategoryID_id=int(feed_category_id), Active=1)

        if not report_obj.exists():
            data = report_template_create_parser(request)
            report_obj = ReportTemplates(**data)
            report_obj.save()
            return redirect("/batches/csv/template/create/view/")
        
        feeds = GetMasters.get_feed(request)
        categories = GetMasters.get_category(request)
        return render(request, "CSVTemplates.html", context={"screen_type": "create_view", "feeds": feeds, "message": Variables().error_messages['unique_validation'].format(report_obj[0].FeedID.Name, report_obj[0].FeedCategoryID.Name), "categories": categories, 'range': range(20)})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})
@login_required(login_url="/batches/validate/user/")
def template_edit(request, template_id):
    """
    Edit an existing report template.

    Args:
        request (HttpRequest): The HTTP request object.
        template_id (int): The ID of the template to edit.

    Returns:
        HttpResponse: The rendered template edit page or a redirect to the template list page.
    """
    try:
        feeds = GetMasters.get_feed(request)
        categories = GetMasters.get_category(request)
        template_obj = ReportTemplates.objects.filter(TemplateID=template_id)
        print(template_obj[0].FeedID.Name)
        data = report_template_update_parser(request)
        obj_count = len(ReportTemplates.objects.filter(FeedID_id=int(data['FeedID']), FeedCategoryID_id=int(data['FeedCategoryID']), Active=1))
        if int(data['Active']) == 1:
            if obj_count > 1:
                return render(request, "CSVTemplates.html", context={"screen_type": "create_view", "template": ReportTemplateListSerializer(template_obj).data[0], "message": Variables().error_messages['unique_validation'].format(template_obj[0].FeedID.Name, template_obj[0].FeedCategoryID.Name), "feeds": feeds, "categories": categories, 'range': range(20)})
        serializer = ReportTemplateCreateSerializer(template_obj, data=data)
        if serializer.is_valid():
            template_obj.update(**data)
            template_obj[0].save()
            return redirect("/batches/csv/template/list/?update=True")
        errors = Error().parse(serializer.errors)
        return render(request, "CSVTemplates.html", context={"screen_type": "create_view", "template": serializer.data, "feeds": feeds, "categories": categories, "error": errors})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})


@login_required(login_url="/batches/validate/user/")
def download_template(request, template_id):
    """
    Download a report template as a CSV file.

    Args:
        request (HttpRequest): The HTTP request object.
        template_id (int): The ID of the template to download.

    Returns:
        HttpResponse: The CSV file response or a 404 error if the file does not exist.
    """
    try:
        template_obj = ReportTemplates.objects.get(pk=template_id)
        columns = template_obj.TemplateHeaders.split(',')
        
        csv_file_path = os.path.join(settings.BASE_DIR, f'static/{template_obj.FeedID.Name}.csv')
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)

        if os.path.exists(csv_file_path):
            with open(csv_file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = f'inline; filename={os.path.basename(csv_file_path)}'
                return response
        raise Http404
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})


@login_required(login_url="/batches/validate/user/")
def validate_batch(request, batch_id):
    """
    Validate a batch of records.

    Args:
        request (HttpRequest): The HTTP request object.
        batch_id (int): The ID of the batch to validate.

    Returns:
        HttpResponse: A redirect to the batch record view page or an error page.
    """
    try:
        batch_obj = Batches.objects.get(pk=batch_id)
        validation_type = batch_obj.Configuration.ValidationType
        if validation_type == 'nt_acc_mapping':
            mappers_obj = NTAccountMapping.objects.filter(BatchID=batch_id, Active=True)
            mappers_serializer = NTAccountListSerializer(mappers_obj, many=True)
            response = DataValidation().nt_account_mapping(request, **{'batch_id': batch_id, 'data': mappers_serializer.data})
        else:
            mappers_obj = PrivateiAccMasterMapping.objects.filter(BatchID=batch_id, Active=True)
            mappers_serializer = MappersListSerializer(mappers_obj, many=True)
            response = DataValidation().mappers_insert(request, **{'batch_id': batch_id, 'data': mappers_serializer.data})
        response_data = response.data
        for data in response_data:
            if 'error_col' in data:
                del data['error_col']
            data['DuplicateEntry'] = False
            data['UpdatedID_id'] = request.user.id
            print(data)
            if data.get('MappingID') is not None and data.get('MappingID') != '':
                record = NTAccountMapping.objects.filter(MappingID=int(data.get('MappingID'))) if validation_type == 'nt_acc_mapping' else PrivateiAccMasterMapping.objects.filter(MappingID=int(data.get('MappingID')))
                print(record)
                if record:
                    record.update(**data)
                    record[0].save()

        return redirect(f"/batches/record/view/{batch_id}/?success=true&update=true")
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})


@login_required(login_url="/batches/validate/user/")
def bulk_update_view(request):
    """
    Render the bulk update view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered bulk update view page.
    """
    try:
        params = request.POST.dict()
        mapping_ids_json = params.get("ids")
        columns_json = params.get("columns")
        columns = json.loads(columns_json)
        feed_id = params.get('feed_id')
        feed_category_id = params.get('feed_category_id')
        return_data = {'screen_type': 'bulk_update_view', 'columns': columns, 'ids': mapping_ids_json, 'feed_id': feed_id, 'feed_category_id': feed_category_id}
        return render(request, 'BatchUpdate.html', context=return_data)
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})


@login_required(login_url="/batches/validate/user/")
def batch_update(request):
    """
    Update a batch of records.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered batch update page or a redirect to the batch record view page.
    """
    try:
        params = request.POST.dict()
        update_type = params.get('update_type')
        if update_type == 'remove':
            response = BatchUpdateAPIview().delete(request)
            print(response.data)
            context_data = {'screen_type': 'update'}
            context_data.update(response.data)
            return render(request, 'BatchUpdate.html', context=context_data)
        mapping_ids_json = params.get("ids")
        mapping_ids = json.loads(mapping_ids_json)
        print(mapping_ids)
        feed_id = params.get('feed_id')
        feed_category_id = params.get('feed_category_id')
        report_obj = get_report_details(request, int(feed_id), int(feed_category_id))
        
        if report_obj.get('validation_type') == Variables().privateimapping:
            headers = Headers()._privateiacc_header
            data = {key: value for key, value in params.items() if key in headers}
            mappers_obj = PrivateiAccMasterMapping.objects.filter(MappingID__in=mapping_ids)
            mappers_obj.update(**data)
            for obj in mappers_obj:
                obj.save()
            serializers = MappersListSerializer(mappers_obj, many=True)
        data = serializers.data
        response_data = {'data': data, 'headers': headers, 'feed_id': feed_id, 'feed_category_id': feed_category_id}
        return render(request, 'BatchUpdate.html', context={'screen_type': 'update', 'data': response_data, 'message': 'Record updated successfully'})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})


@login_required(login_url="/batches/validate/user/")
def batch_record_update(request):
    """
    Update a batch record.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the batch record view page or an error page.
    """
    try:
        params = request.POST.dict()
        action = params.get('action')
        response = BatchUpdateAPIview().post(request)
        context_data = {'screen_type': 'data_view'}
        context_data.update(response.data)
        return redirect(f"/batches/record/view/{params.get('batch_id')}/?success=true&action=" + action)
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})


@login_required(login_url="/batches/validate/user/")
def data_insert(request):
    """
    Insert data from a CSV file into the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the batch record view page or an error page.
    """
    try:
        params = request.POST.dict()
        filename = request.FILES['data_file']
        main_df = pd.read_csv(filename, encoding_errors='ignore')
        request_data = main_df.to_dict('records')
        feed_id = int(params['FeedID'])
        category_id = int(params['FeedCategoryID'])
        model = get_model_name(request)
        headers = validation_class.get_header(request)
        report_obj = ReportTemplates.objects.get(FeedID=feed_id, FeedCategoryID=category_id, Active=1)
        batch_no = "MSCI" + str(random.randint(10001, 99999))
        batch_obj = Batches.objects.create(
            BatchNo=batch_no,
            FeedID_id=int(params['FeedID']),
            FeedCategoryID_id=int(params['FeedCategoryID']),
            RecordCount=len(request_data),
            Configuration_id=report_obj.TemplateID,
            UploadType='non-validate-upload'
        )

        # Save data to the appropriate mapping table
        for data in request_data:
            request_data = {x: data[x] for x in headers}
            request_data['DuplicateEntry'] = False
            request_data['BatchID_id'] = batch_obj.BatchID
            request_data['CreatedID_id'] = request.user.id
            request_data['UpdatedID_id'] = request.user.id
            request_data['Error'] = False
            request_data['ErrorMessages'] = {}
            # Choose mapping model dynamically
            mappers_obj = model(**request_data)
            mappers_obj.save()

        return redirect(f"/batches/record/view/{batch_obj.BatchID}/?success=true")
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

