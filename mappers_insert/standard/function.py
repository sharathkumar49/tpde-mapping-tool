from django.contrib.auth.decorators import login_required
from masters.models import *
from masters.serializers import *


@login_required(login_url="/batches/validate/user/")
def get_feeds(request):
    feed = Feeds.objects.filter(Active=1)
    feed_serializer = FeedListSerializer(feed, many=True)
    return feed_serializer.data

@login_required(login_url="/batches/validate/user/")
def get_feed_categories(request):    
    category = FeedCategory.objects.filter(Active=True)
    category_serializer = FeedCategoryListSerializer(category, many=True)
    return category_serializer.data

@login_required(login_url="/batches/validate/user/")
def error_parser(request):    
    category = FeedCategory.objects.filter(Active=True)
    category_serializer = FeedCategoryListSerializer(category, many=True)
    return category_serializer.data

class JSON:
    def read(self, file_path):
        with open(file_path, "r") as fp:
            data = fp.readlines()
        return data
    

class Error:
    
    @staticmethod
    def parse(error):
        error_str=""
        for col, message in error.items():
            error_str += str(message[0].title())
        return error_str




