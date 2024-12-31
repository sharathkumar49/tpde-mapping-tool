from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from .views import *
from rest_framework.decorators import api_view, permission_classes
import requests
import json
from django.contrib.auth.decorators import login_required
from django.db import connections
from batches.models import Batches, ReportTemplates
from django.db.models import Count
from batches.serializers import BatchListSerializer
import re
from django.http import JsonResponse
from total_plan_py_common import send_email
from django.conf import settings
import random
import string
from masters.decorator import create_exception_log


def generate_password(length=12):
    """
    Generate a random password with the given length.

    Args:
        length (int): Length of the password to be generated. Default is 12.

    Returns:
        str: Generated password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def email_check(email):
    """
    Check if the given email is valid.

    Args:
        email (str): Email address to be checked.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True
    return False

def get_username_by_email(email):
    """
    Get the username associated with the given email.

    Args:
        email (str): Email address to get the username for.

    Returns:
        str: Username associated with the email if valid, otherwise the email itself.
    """
    is_valid = email_check(email)
    if is_valid:
        user = User.objects.get(email=email)
        return user.username
    return email


def login_view(request):
    """
    Render the login page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered login page.
    """
    return render(request, "Login.html")

def login_user(request):
    """
    Authenticate and log in the user.

    Args:
        request (HttpRequest): The request object containing login credentials.

    Returns:
        HttpResponse: Redirect to dashboard if successful, otherwise render login page with error message.
    """
    params = request.POST.dict()
    role = params.get("role")
    if role:
        login_username = get_username_by_email(params.get("username"))
        login_password = params.get("password")
        user = authenticate(username=login_username, password= login_password)
        print(user)
        if user:
            profile = UserProfile.objects.filter(User_id=user.id)
            login(request, user)
            create_exception_log(request, "User Logged!", login=True)
            if len(profile) > 0:
                if profile[0].FirstLogin:
                    return render(request, "Login.html", context={"screen_type": "FirstLogin"})
            return redirect ("/dashboard/")
        else:
            return render(request, "Login.html", context={"status": False, "error": "Please enter valid credentials..!"})
    else:
        return render(request, "Login.html", context={"status": False, "error": "Role is not configured properly. Please contact admin..!"})

@login_required(login_url="/batches/validate/user/")
def user_logout(request):
    """
    Log out the user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Redirect to home page.
    """
    create_exception_log(request, "User Logged out!")
    logout(request)
    print ("logout")
    return redirect("/")


@login_required(login_url="/batches/validate/user/")
def user_password_update(request):
    """
    Update the user's password.

    Args:
        request (HttpRequest): The request object containing the new password.

    Returns:
        HttpResponse: Redirect to home page if successful, otherwise render error page.
    """
    try:
        params = request.POST.dict()
        password = params.get("password")
        if password:
            user = User.objects.get(id=request.user.id)
            profile = UserProfile.objects.get(User_id=request.user.id)
            user.set_password(password)
            user.save()
            profile.FirstLogin = False
            profile.save()
        logout(request)
        return redirect("/")
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def dashboard_view(request):
    """
    Render the dashboard view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered dashboard page.
    """
    try:
        request.session['topbar'] = True
        status_records = Batches.objects.values('Status').annotate(dcount=Count('Status')).order_by()
        batches = Batches.objects.filter(Status__in=[0,1]).order_by('-BatchID')[:5]
        serializers = BatchListSerializer(batches, many=True)
        total_records = 0
        status_dict = {}
        for status in status_records:
            status_dict[status['Status']] = status["dcount"]
            total_records+=status["dcount"]
        return render(request, 'dashboard.html', context={"status": status_dict, "batches": serializers.data, "total_batches":total_records})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def batch_list_view(request):
    """
    Render the batch list view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered batch list page.
    """
    return render(request, 'Batch.html', {'screen_type':'list_view'})

@login_required(login_url="/batches/validate/user/")
def batch_create_view(request):
    """
    Render the batch create view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered batch create page.
    """
    return render(request, 'Batch.html', {'screen_type':'create_view'})


@login_required(login_url="/batches/validate/user/")
def user_list_view(request):
    """
    Render the user list view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered user list page.
    """
    try:
        user = UserProfile.objects.filter(Active=1)
        serializers = UserProfileListSerializer(user, many=True)
        print (ref)
        return render(request, 'User.html', {'screen_type':'list_view', "user": serializers.data})
    except Exception as e:
        print (e)
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def user_create_view(request):
    """
    Render the user create view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered user create page.
    """
    return render(request, 'User.html', {'screen_type':'create_view'})

@login_required(login_url="/batches/validate/user/")
def create_user(request):
    """
    Create a new user.

    Args:
        request (HttpRequest): The request object containing user data.

    Returns:
        JsonResponse: JSON response indicating success or failure.
    """
    try:
        userdata = user_create_parser(request)
        user_obj = User.objects.filter(username=userdata['user']['email'])
        if user_obj:
            return JsonResponse({"status": False, "message": "User email ID already exists..!"})
        user = User(**userdata['user'])
        password = "admin@123"
        user.set_password(password)
        user.save()
        if user:
            profile = userdata['profile']
            profile['User_id'] = user.id
            profile = UserProfile(**userdata['profile'])
            profile.save()
        # send_email(
        #     email_from=settings.EMAIL_FROM,
        #     email_address=settings.EMAIL_FROM,
        #     email_password=settings.EMAIL_PASSWORD,
        #     email_to_str=userdata['user']['email'],
        #     email_subject="One time Password",
        #     email_body=f"Your One Time Password is: {password}"
        # )
        return JsonResponse({'status': True, 'message': 'User created successfully..!'})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def user_edit_view(request, user_id):
    """
    Render the user edit view.

    Args:
        request (HttpRequest): The request object.
        user_id (int): ID of the user to be edited.

    Returns:
        HttpResponse: Rendered user edit page.
    """
    try:
        user_obj = UserProfile.objects.filter(User_id=user_id)
        serializers = UserProfileListSerializer(user_obj, many=True)
        return render(request, 'User.html', {'screen_type':'create_view', "user_profile": serializers.data[0]})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})
    
@login_required(login_url="/batches/validate/user/")
def user_edit(request, user_id):
    """
    Edit an existing user.

    Args:
        request (HttpRequest): The request object containing updated user data.
        user_id (int): ID of the user to be edited.

    Returns:
        JsonResponse: JSON response indicating success or failure.
    """
    try:
        user_obj = UserProfile.objects.filter(User_id=user_id)
        userdata = user_edit_parser(request)
        print (userdata)
        user = User.objects.filter(id=user_obj[0].User.id)
        user.update(**userdata['user'])
        user[0].save()
        if user:
            profile = user_obj.update(**userdata['profile'])
            user_obj[0].save()
        return JsonResponse({'status': True, 'message': 'User updated successfully..!'})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})
    

@login_required(login_url="/batches/validate/user/")
def feed_list_view(request):
    """
    Render the feed list view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered feed list page.
    """
    try:
        feeds = Feeds.objects.filter(Active=1)
        serializers = FeedListSerializer(feeds, many=True)
        return render(request, 'Feed.html', {'screen_type':'list_view', "feeds": serializers.data})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def feed_create_view(request):
    """
    Render the feed create view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered feed create page.
    """
    try:
        feed_category = FeedCategory.objects.filter(Active=1)
        serializer = FeedCategoryListSerializer(feed_category, many=True)
        return render(request, 'Feed.html', {'screen_type':'create_view', 'category': serializer.data})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def create_feed(request):
    """
    Create a new feed.

    Args:
        request (HttpRequest): The request object containing feed data.

    Returns:
        HttpResponse: Redirect to feed list page if successful, otherwise render error page.
    """
    try:
        response = FeedCreateAPIView.as_view()(request)
        if response.status_code == 201:
            return redirect("/masters/feed/list/?success=True")
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def feed_edit_view(request, pk):
    """
    Render the feed edit view.

    Args:
        request (HttpRequest): The request object.
        pk (int): ID of the feed to be edited.

    Returns:
        HttpResponse: Rendered feed edit page.
    """
    try:
        if request.method == 'GET':
            feed_obj = Feeds.objects.filter(FeedID=pk)
            feed_serializer = FeedListSerializer(feed_obj, many=True)
            category_obj = FeedCategory.objects.filter(Active=True)
            category_serializer = FeedCategoryListSerializer(category_obj, many=True)
            return render(request, 'Feed.html', {'screen_type':'create_view', 'category': category_serializer.data, 'feed': feed_serializer.data[0]})
        else:
            response = FeedEditAPIView.as_view()(request)
            if response.status_code == 200:
                return redirect("/masters/feed/list/?update=True")
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})
      
@login_required(login_url="/batches/validate/user/")
def feed_category_list_view(request):
    """
    Render the feed category list view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered feed category list page.
    """
    try:
        feed_category = FeedCategory.objects.filter(Active=1)
        serializer = FeedCategoryListSerializer(feed_category, many=True)
        return render(request, 'FeedCategory.html', {'screen_type':'list_view', "categories": serializer.data})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def feed_category_create_view(request):
    """
    Render the feed category create view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered feed category create page.
    """
    return render(request, 'FeedCategory.html', {'screen_type':'create_view'})

@login_required(login_url="/batches/validate/user/")
def create_feed_category(request):
    """
    Create a new feed category.

    Args:
        request (HttpRequest): The request object containing feed category data.

    Returns:
        HttpResponse: Redirect to feed category list page if successful, otherwise render error page.
    """
    try:
        response = FeedCategoryCreateAPIView.as_view()(request)
        print (response.status_code)
        if response.status_code == 201:
            return redirect("/masters/feed/category/list/?success=True")
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})

@login_required(login_url="/batches/validate/user/")
def feed_category_edit_view(request, pk):
    """
    Render the feed category edit view.

    Args:
        request (HttpRequest): The request object.
        pk (int): ID of the feed category to be edited.

    Returns:
        HttpResponse: Rendered feed category edit page.
    """
    try:
        if request.method == 'GET':
            category_obj = FeedCategory.objects.filter(FeedCategoryID=pk)
            serializer = FeedCategoryListSerializer(category_obj, many=True)
            return render(request, 'FeedCategory.html', {'screen_type':'create_view', 'category': serializer.data[0]})
        else:
            response = FeedCategoryEditAPIView.as_view()(request)
            if response.status_code == 200:
                return redirect("/masters/feed/category/list/?update=True")
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})


@login_required(login_url="/batches/validate/user/")
def csv_template_search_view(request):
    """
    Render the CSV template search view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered CSV template search page.
    """
    return render(request, "CSVTemplates.html", {'screen_type':'search_view'})


@login_required(login_url="/batches/validate/user/")
def user_profile_view(request):
    """
    Render the user profile view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered user profile page.
    """
    try:
        user_id = request.user.id
        print (user_id)
        profile_data = UserProfile.objects.filter(user=user_id)
        if profile_data:
            serializer = UserProfileListSerializer(profile_data[0])
        return render(request, 'User.html', {'screen_type':'profile_view', "profile": serializer.data})
    except Exception as e:
        print(f"Error : {e}")
        ref = create_exception_log(request, e)
        return render(request, 'Error.html', {'ref': ref})
    