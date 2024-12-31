from django.shortcuts import render
from django.views.generic.list import ListView
from .models import *
from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from .function import *


class FeedListAPIView(generics.ListAPIView):
    """
    API view to retrieve list of feeds.
    """
    serializer_class = FeedListSerializer
    model = serializer_class.Meta.model
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Name']
    paginate_by = 5

    def get_queryset(self):
        """
        Override the default queryset to filter active feeds.
        """
        self.pagination_class.page_size = 100
        queryset = self.model.objects.filter(Active=True)
        return queryset


class FeedCreateAPIView(APIView):
    """
    API view to create a new feed.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new feed.
        """
        feed_data = format_feed_data(request)
        serializers = FeedCreateSerializer(data=feed_data)
        valid = serializers.is_valid()
        if valid:
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FeedEditAPIView(APIView):
    """
    API view to edit an existing feed.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to edit an existing feed.
        """
        feed_id = request.data.get('feed_id')
        feed_obj = Feeds.objects.filter(FeedID=int(feed_id))
        feed_data = format_feed_data(request)
        feed_serializer = FeedCreateSerializer(feed_obj[0], data=feed_data)
        if feed_serializer.is_valid():
            feed_serializer.save()
            print(feed_serializer.data)
        return Response(data=feed_serializer.data, status=status.HTTP_200_OK)


class FeedCategoryListAPIView(generics.ListAPIView):
    """
    API view to retrieve list of feed categories.
    """
    serializer_class = FeedCategoryListSerializer
    model = serializer_class.Meta.model
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Name', 'Description']
    paginate_by = 5

    def get_queryset(self):
        """
        Override the default queryset to filter active feed categories.
        """
        self.pagination_class.page_size = 100
        queryset = self.model.objects.filter(Active=True)
        return queryset


class FeedCategoryCreateAPIView(APIView):
    """
    API view to create a new feed category.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new feed category.
        """
        feed_data = format_feed_category_data(request)
        serializers = FeedCategoryCreateSerializer(data=feed_data)
        valid = serializers.is_valid()
        if valid:
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FeedCategoryEditAPIView(APIView):
    """
    API view to edit an existing feed category.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to edit an existing feed category.
        """
        category_id = request.data.get('category_id')
        category_obj = FeedCategory.objects.filter(FeedCategoryID=int(category_id))
        category_data = format_feed_category_data(request)
        category_serializer = FeedCategoryCreateSerializer(category_obj[0], data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            print(category_serializer.data)
        return Response(data=category_serializer.data, status=status.HTTP_200_OK)