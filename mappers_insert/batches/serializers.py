from .models import *
# Create your views here.
from rest_framework import serializers
from masters.serializers import FeedListSerializer, FeedCategoryListSerializer

class ReportTemplateListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing ReportTemplates.
    Includes nested serializers for Feed and FeedCategory.
    """
    FeedID = FeedListSerializer(required=True)
    FeedCategoryID = FeedCategoryListSerializer(required=True)
    
    class Meta:
        model = ReportTemplates
        fields = "__all__"

class BatchListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Batches.
    Includes a nested serializer for ReportTemplate and a read-only field for status display value.
    """
    status_display_value = serializers.CharField(
        source='get_Status_display', read_only=True
    )
    Configuration = ReportTemplateListSerializer(required=True)
    
    class Meta:
        model = Batches
        fields = "__all__"

class MappersListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing PrivateiAccMasterMapping.
    """
    class Meta:
        model = PrivateiAccMasterMapping
        fields = "__all__"

class NTAccountListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing NTAccountMapping.
    """
    class Meta:
        model = NTAccountMapping
        fields = "__all__"

class ReportTemplateCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating ReportTemplates.
    """
    class Meta:
        model = ReportTemplates
        fields = "__all__"

class StandardReportSerializer(serializers.ModelSerializer):
    """
    Serializer for standard reports.
    """
    class Meta:
        fields = "__all__"