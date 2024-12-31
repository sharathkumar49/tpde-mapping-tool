
from standard.variables import Variables
from .models import ReportTemplates
from django.apps import apps
from django.template.defaulttags import register

def report_template_create_parser(request):
    """
    Parses the request data to create a new report template.

    Args:
        request (HttpRequest): The HTTP request object containing POST data.

    Returns:
        dict: A dictionary containing the parsed data for creating a report template.
    """
    params = request.POST.dict()
    data = {
        "FeedID_id": params.get("feed_id"),
        "FeedCategoryID_id": params.get("feed_category_id"),
        "TemplateHeaders": params.get("template_headers"),
        "ReportHeaders": params.get("report_headers"),
        "ValidationType": params.get("ValidationType")
    }
    return data

def report_template_update_parser(request):
    """
    Parses the request data to update an existing report template.

    Args:
        request (HttpRequest): The HTTP request object containing POST data.

    Returns:
        dict: A dictionary containing the parsed data for updating a report template.
    """
    params = request.POST.dict()
    data = {
        "FeedID": int(params.get("feed_id")),
        "FeedCategoryID": int(params.get("feed_category_id")),
        "TemplateHeaders": params.get("template_headers"),
        "ReportHeaders": params.get("report_headers"),
        "ValidationType": params.get("ValidationType"),
        "Active": params.get("status")
    }
    return data

def get_model_name(request, validation_type=None):
    """
    Retrieves the model name based on the validation type.

    Args:
        request (HttpRequest): The HTTP request object containing POST data.
        validation_type (str, optional): The validation type. Defaults to None.

    Returns:
        Model: The Django model corresponding to the validation type.
    """
    if not validation_type:
        params = request.POST.dict()
        report_obj = ReportTemplates.objects.filter(FeedID=int(params['FeedID']), FeedCategoryID=int(params['FeedCategoryID']))
        print(report_obj[0].ValidationType)
        validation_type = report_obj[0].ValidationType
    table_name = Variables().validation_modals[validation_type]
    Model = apps.get_model('batches', table_name)
    return Model

def get_report_details(request, feed_id, feed_category_id):
    """
    Retrieves the details of a report template.

    Args:
        request (HttpRequest): The HTTP request object.
        feed_id (int): The ID of the feed.
        feed_category_id (int): The ID of the feed category.

    Returns:
        dict: A dictionary containing the report details, or False if not found.
    """
    report_obj = ReportTemplates.objects.get(FeedID=feed_id, FeedCategoryID=feed_category_id)
    if report_obj:
        return {'feed_name': report_obj.FeedID.Name, 'feed_category_name': report_obj.FeedCategoryID.Name, 'validation_type': report_obj.ValidationType, 'headers': report_obj.TemplateHeaders, 'report_headers': report_obj.ReportHeaders}
    return False
    


@register.filter
def get_item(dictionary, key):
    """
    Retrieves an item from a dictionary by key.

    Args:
        dictionary (dict): The dictionary to retrieve the item from.
        key: The key of the item to retrieve.

    Returns:
        The value associated with the key in the dictionary.
    """
    return dictionary.get(key)
