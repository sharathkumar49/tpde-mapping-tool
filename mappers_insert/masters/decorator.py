
from functools import wraps
from .models import UserLog
from datetime import datetime
import random



def create_exception_log(request, exception, login=False):
    ref_no = "REF" + str(random.randint(10001, 99999))
    method = request.method
    if method == "GET":
        params = request.GET.dict()
    else:
        params = request.POST.dict()
    if login:
        params['password'] = "******"
    log = UserLog.objects.create(LogType="Exception", LogMessage=str(exception), LogIP=request.META.get('REMOTE_ADDR'), RequestURL=request.META.get('PATH_INFO'), RequestData=str(params), ResponseData=str(exception), User = request.user, ReferenceID=ref_no)
    log.save()
    return ref_no
