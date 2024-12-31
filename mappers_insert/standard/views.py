from django.shortcuts import render, redirect
import os
import json
from .variables import Variables
from pathlib import Path
# Create your views here.


def login_check(request):
    if request.user.is_authenticated:
        return True
    else:
        return redirect('/')
    


class JSON:

    def read(self, file):
        if os.path.exists(file):
            return True
        else:
            return False



def load_json():
    json_folder = Variables().jsonfilepath
    for file in Path(json_folder).glob('*.json'):
        filename = file.name.split('.')[0]
        data = json.loads(file.read_text())
        setattr(Variables, filename, data)
    return True

