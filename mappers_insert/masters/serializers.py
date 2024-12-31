from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for User model. Serializes all fields of the User model.
    """

    class Meta:
        model = User
        fields = "__all__"

class LogGETSerializer(serializers.ModelSerializer):
    """
    Serializer for UserLog model. Serializes all fields of the UserLog model.
    Includes nested UserListSerializer for the User field.
    """
    User = UserListSerializer(required=True)
   
    class Meta:
        model = UserLog
        fields = "__all__"

class UserProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model. Serializes all fields of the UserProfile model.
    Includes nested UserListSerializer for the User field and a read-only role_display_value field.
    """
    User = UserListSerializer(required=True)
    role_display_value = serializers.CharField(
        source='get_Role_display', read_only=True
    )
    
    class Meta:
        model = UserProfile
        fields = "__all__"

class FeedCategoryListSerializer(serializers.ModelSerializer):
    """
    Serializer for FeedCategory model. Serializes all fields of the FeedCategory model.
    """

    class Meta:
        model = FeedCategory
        fields = "__all__"

class FeedListSerializer(serializers.ModelSerializer):
    """
    Serializer for Feeds model. Serializes all fields of the Feeds model.
    """
    
    class Meta:
        model = Feeds
        fields="__all__"

class FeedCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Feeds. Serializes all fields of the Feeds model.
    Includes custom validation for the Name field.
    """

    def validate(self, attrs):
        """
        Custom validation method that prints the attributes and calls the superclass validate method.
        """
        print(attrs, "attrs")
        return super().validate(attrs)

    class Meta:
        model = Feeds
        fields= "__all__"
        extra_kwargs = {
                "Name":{
                    "required": True,
                    "error_messages":{
                        "blank": "Feed Name should not be blank.",
                        "required": "Feed Name should not be blank."
                    }
                }
            }

class FeedCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating FeedCategory. Serializes all fields of the FeedCategory model.
    Includes custom validation for the Name field.
    """

    def validate(self, attrs):
        """
        Custom validation method that prints the attributes and calls the superclass validate method.
        """
        print(attrs, "attrs")
        return super().validate(attrs)

    class Meta:
        model = FeedCategory
        fields= "__all__"
        extra_kwargs = {
                "Name":{
                    "required": True,
                    "error_messages":{
                        "blank": "Feed Name should not be blank.",
                        "required": "Feed Name should not be blank."
                    }
                },
            }