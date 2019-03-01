from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from comment.forms import *
from comment.views import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import random


# Create your views here.

def index(request):
    '''
    log_phd, log_url_phd
    :param request:
    :return:
    '''
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                if request.user.usertype == 'normal':
                    profile = NormalUser.objects.get(user=request.user)
                else:
                    profile = DoctorUser.objects.get(user=request.user)
            except ValueError:
                profile.avatar = NormalUser.objects.get(user_id=3).avatar
            context = {'profile':profile}
            return render(request, 'myhealth/index.html', context)
        else:
            return render(request, 'myhealth/index.html')











@csrf_exempt
def ajax_post(request):
    print('ok')
    data = random.randrange(1, 100)
    result = data['SIG'][0] + ',' + data['IBI'][0] + ',' + data['BMP'][0]
    Data(user=str(request.user), curr_time=timezone.now(), sig=data['SIG'][0], ibi=data['IBI'][0],
         bmp=data['BMP'][0]).save()
    return HttpResponse(result)



def base(request):
    return render(request, 'myhealth/base1.html')
