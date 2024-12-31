from masters.serializers import FeedCategory, Feeds, FeedCategoryListSerializer, FeedListSerializer
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
import csv
import os
from django.conf import settings 
from django.http import JsonResponse
import pandas as pd
from standard.function import *
from django.db import connections
from masters.serializers import LogGETSerializer, UserProfileListSerializer
from masters.models import UserLog
from masters.decorator import create_exception_log

@login_required(login_url="/batches/validate/user/")
def data_export_form(request):
    """
    Renders the data export form with feeds and categories.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered template with feeds and categories.
    """
    feeds = get_feeds(request)
    categories = get_feed_categories(request)
    return render(request, "ReportTemplate.html", context={"feeds": feeds, "categories": categories})

@login_required(login_url="/batches/validate/user/")
def log_search_view(request):
    """
    Renders the log search view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered log search template.
    """
    return render(request, "LogReport.html", context={'screen_type': 'search'})

@login_required(login_url="/batches/validate/user/")
def log_search(request):
    """
    Searches for logs based on reference number or email and returns the results as JSON.

    Args:
        request (HttpRequest): The request object.

    Returns:
        JsonResponse: The search results in JSON format.
        HttpResponse: The error template if an exception occurs.
    """
    try:
        params = request.POST.dict()
        reference_no = params.get('reference_no')
        email = params.get('email')
        if reference_no and not email:
            log = UserLog.objects.filter(ReferenceID=reference_no)
        elif not reference_no and email:
            log = UserLog.objects.filter(User__email=email)
        elif reference_no and email:
            log = UserLog.objects.filter(ReferenceID=reference_no, User__email=email)
        else:
            log = UserLog.objects.all()
        serializer = LogGETSerializer(log, many=True)
        print(serializer.data)
        return JsonResponse({'ref': reference_no, 'logs': serializer.data, 'screen_type': 'report'}) 
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})