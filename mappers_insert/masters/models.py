from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class GeneralModel(models.Model):
    CreatedID = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    UpdatedID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    CreatedDate = models.DateTimeField(default=datetime.today(),null=True)
    UpdatedDate = models.DateTimeField(default=datetime.today(),null=True)
    Active = models.BooleanField(default=True)

    class Meta:
        abstract=True

class FeedCategory(GeneralModel):
    FeedCategoryID = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Description = models.TextField(null=True,blank=True)

class Feeds(GeneralModel):
    FeedID = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Description = models.TextField(null=True,blank=True)

class UserProfile(GeneralModel):
    Roles = [("admin", "ADMIN"), ('data_engineer', "DATA ENGINEER"), ("analyst", "ANALYST")]
    User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')
    Role = models.CharField(max_length=255, choices=Roles, null=True)
    FirstLogin = models.BooleanField(default=True)


class UserLog(models.Model):
    LogType = models.CharField(max_length=255)
    LogMessage = models.TextField()
    LogDate = models.DateTimeField(default=datetime.today())
    LogIP = models.CharField(max_length=255)
    ReferenceID = models.CharField(max_length=255)
    RequestURL = models.CharField(max_length=255)
    RequestData = models.CharField(max_length=255)    
    ResponseData = models.CharField(max_length=255)
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True, blank=True)






