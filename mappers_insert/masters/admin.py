from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Feeds)
admin.site.register(FeedCategory)
admin.site.register(UserProfile)
admin.site.register(UserLog)