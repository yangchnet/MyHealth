from django.shortcuts import render
from .models import MhUser, Match, NormalUser, DoctorUser
from .forms import Register, Login
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
from notifications.signals import notify
from notifications.models import Notification
# Create your views here.

def register(request):
    if request.method == 'GET':
        user = Register()
        context = {'user': user}
        return render(request, 'mhuser/register.html', {'user': user})
    if request.method == 'POST':
        user = Register(request.POST)
        if user.is_valid():
            try:
                curr_user = MhUser.objects.create_user(username=user.cleaned_data['user_name'],
                                                       email=user.cleaned_data['user_email'],
                                                       password=user.cleaned_data['user_password'],
                                                       usertype=user.cleaned_data['user_type'])
                if user.cleaned_data['user_type'] == 'normal':
                    NormalUser.objects.create(user=curr_user).save()
                elif user.cleaned_data['user_type'] == 'doctor':
                    DoctorUser.objects.create(user=curr_user).save()
                curr_user = auth.authenticate(request, username=user.cleaned_data['user_name'],
                                              password=user.cleaned_data['user_password'])
                if curr_user is not None:
                    login(request, curr_user)
                    return render(request, 'myhealth/index.html')
            except IntegrityError as e:
                context = {'user': user, 'z_placeholder': '用户名被占用'}
                return render(request, 'mhuser/register.html', context)
    return render(request, 'mhuser/register.html', {'user': user})


def user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/myhealth')
        else:
            return render(request, 'mhuser/login.html', )
    if request.method == 'POST':
        user = Login(request.POST)
        if user.is_valid():
            curr_user = auth.authenticate(username=user.cleaned_data['user_name'],
                                          password=user.cleaned_data['user_password'])
            if curr_user is not None:
                login(request, curr_user)
                return HttpResponseRedirect('/myhealth')


@csrf_exempt
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/myhealth')
    else:
        return HttpResponseRedirect('/myhealth')

def doctors(request):
    if request.user.is_authenticated:
        try:
            if request.user.usertype == 'normal':
                profile = NormalUser.objects.get(user=request.user)
            else:
                profile = DoctorUser.objects.get(user=request.user)
        except ValueError:
            profile.avatar = NormalUser.objects.get(user_id=3).avatar
        notice = request.user.notifications.unread()
        return render(request, 'mhuser/doctors.html', {'notices': notice, 'profile': profile})
    return render(request, 'mhuser/doctors.html')


def doctor(request, doctor_id):
    return render(request, 'mhuser/doctor.html')


def devices(request):
    return render(request, 'mhuser/devices.html')

@login_required
def profile(request):
    try:
        if request.user.usertype == 'normal':
            profile = NormalUser.objects.get(user=request.user)
        else:
            profile = DoctorUser.objects.get(user=request.user)
    except ValueError:
        profile.avatar = NormalUser.objects.get(user_id=3).avatar
    return render(request, 'mhuser/profile.html', {'profile':profile})

@login_required
def heartbeat(request):
    try:
        if request.user.usertype == 'normal':
            profile = NormalUser.objects.get(user=request.user)
        else:
            profile = DoctorUser.objects.get(user=request.user)
    except ValueError:
        profile.avatar = NormalUser.objects.get(user_id=3).avatar
    ck = CKEditorForm()
    return render(request, 'mhuser/heartbeat.html', {'ck': ck,'profile':profile})

@login_required
def notification(request, page_id):
    try:
        if request.user.usertype == 'normal':
            profile = NormalUser.objects.get(user=request.user)

        else:
            profile = DoctorUser.objects.get(user=request.user)

    except ValueError:
        profile.avatar = NormalUser.objects.get(user_id=3).avatar
    curr_user = request.user
    unread = curr_user.notifications.unread()[10 * (page_id - 1): 10 * page_id]
    context = {'profile':profile, 'unread':unread, 'page_range': range(page_id, page_id+4), 'page_id':page_id}
    return render(request, 'mhuser/notification.html', context)

@login_required
def noti(request, noti_id):
    curr_user = request.user
    unread = Notification.objects.get(id = noti_id)
    try:
        if request.user.usertype == 'normal':
            profile = NormalUser.objects.get(user=request.user)

        else:
            profile = DoctorUser.objects.get(user=request.user)

    except ValueError:
        profile.avatar = NormalUser.objects.get(user_id=3).avatar
    context = {'profile':profile, 'unread':unread}
    unread.mark_as_read()
    return render(request, 'mhuser/noti.html', context)

