from django.shortcuts import render
from .models import MhUser, Match, NormalUser, DoctorUser, HeartData, OxygenData, TemData, PressureData
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
from explain.views import getexplainlist
import threading
from django.contrib.auth.hashers import make_password, check_password

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
                                                       usertype=user.cleaned_data['user_type'],
                                                       mypassword = user.cleaned_data['user_password']) # 兼容android
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
    return HttpResponseRedirect('/myhealth')


@csrf_exempt
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/myhealth')
    else:
        return HttpResponseRedirect('/myhealth')


def doctors(request):
    doctors = DoctorUser.objects.all()
    if request.user.is_authenticated:
        try:
            if request.user.usertype == 'normal':
                profile = NormalUser.objects.get(user=request.user)
            else:
                profile = DoctorUser.objects.get(user=request.user)
        except ValueError:
            profile.avatar = NormalUser.objects.get(user_id=3).avatar
        notice = request.user.notifications.unread()
        context = {'notices': notice, 'profile': profile, 'doctors':doctors}
        return render(request, 'mhuser/doctors.html', context)
    context = {'doctors': doctors}
    return render(request, 'mhuser/doctors.html', context)


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
    return render(request, 'mhuser/profile.html', {'profile': profile})


def is_perm(doctor, user, charged):
    try:
        Match.objects.get(doctor=doctor, normaluser=user, charged=charged)
        return 1
    except Match.DoesNotExist:
        return 0


@login_required
def heartbeat(request, user_id):
    if request.method == "GET":
        ck = CKEditorForm()
        # 当前用户是医生
        if request.user.usertype == 'doctor':
            # 获取用户信息
            try:
                profile = DoctorUser.objects.get(user=request.user)
            except ValueError:
                profile.avatar = NormalUser.objects.get(user_id=3).avatar
            # 检查是否有权限查看
            if is_perm(DoctorUser.objects.get(user=request.user), NormalUser.objects.get(pk=user_id), 'heartbeat'):
                data = HeartData.objects.filter(own=NormalUser.objects.get(pk=user_id))
                try:
                    explains = getexplainlist(request, user_id, 'heartbeat')
                    explain_count = len(explains)
                    context = {'ck': ck, 'profile': profile, 'data': data,
                               'owner': MhUser.objects.get(pk=user_id).username,
                               'explains': explains, 'explain_count': explain_count,
                               'type': 'heartbeat'}
                except TypeError:
                    context = {'ck': ck, 'profile': profile, 'data': data,
                               'owner': MhUser.objects.get(pk=user_id).username,
                               'explains': None, 'explain_count': 0,
                               'type': 'heartbeat'}
                return render(request, 'mhuser/heartbeat.html', context)
            else:  # 无权限查看
                return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
        # 当前用户是普通用户
        elif request.user.usertype == 'normal':
            # 获取用户信息
            try:
                profile = NormalUser.objects.get(user=request.user)
            except ValueError:
                profile.avatar = NormalUser.objects.get(user_id=3).avatar
            data = HeartData.objects.filter(own=NormalUser.objects.get(user=request.user))
            try:
                explains = getexplainlist(request, user_id, 'heartbeat')
                explain_count = len(explains)
                context = {'ck': ck, 'profile': profile, 'data': data,
                           'owner': MhUser.objects.get(pk=user_id).username,
                           'explains': explains, 'explain_count': explain_count,
                           'type': 'heartbeat'}
            except TypeError:
                context = {'ck': ck, 'profile': profile, 'data': data,
                           'owner': MhUser.objects.get(pk=user_id).username,
                           'explains': None, 'explain_count': 0,
                           'type': 'heartbeat'}
            return render(request, 'mhuser/heartbeat.html', context)


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
    context = {'profile': profile, 'unread': unread, 'page_range': range(page_id, page_id + 4), 'page_id': page_id}
    return render(request, 'mhuser/notification.html', context)


@login_required
def noti(request, noti_id):
    curr_user = request.user
    unread = Notification.objects.get(id=noti_id)
    try:
        if request.user.usertype == 'normal':
            profile = NormalUser.objects.get(user=request.user)

        else:
            profile = DoctorUser.objects.get(user=request.user)

    except ValueError:
        profile.avatar = NormalUser.objects.get(user_id=3).avatar
    context = {'profile': profile, 'unread': unread}
    unread.mark_as_read()
    return render(request, 'mhuser/noti.html', context)


@login_required
def myclient(request):
    curr_user = request.user
    # 用户个人信息获取
    try:
        profile = DoctorUser.objects.get(user=request.user)
    except ValueError:  # 设置默认头像
        profile.avatar = NormalUser.objects.get(user_id=3).avatar

    # 通过match表找到我的客户
    match = Match.objects.filter(doctor=DoctorUser.objects.get(user=curr_user))
    return render(request, 'mhuser/myclient.html', {'profile': profile, 'match': match})


@login_required
def oxygen(request, user_id):
    if request.method == "GET":
        ck = CKEditorForm()
        # 当前用户是医生
        if request.user.usertype == 'doctor':
            # 获取用户信息
            try:
                profile = DoctorUser.objects.get(user=request.user)
            except ValueError:
                profile.avatar = NormalUser.objects.get(user_id=3).avatar
            # 检查是否有权限查看
            if is_perm(DoctorUser.objects.get(user=request.user), NormalUser.objects.get(pk=user_id), 'oxygen'):
                data = OxygenData.objects.filter(own=NormalUser.objects.get(pk=user_id))
                explains = getexplainlist(request, user_id, 'oxygen')
                explain_count = len(explains)
                context = {'ck': ck, 'profile': profile,'data': data,
                           'owner': MhUser.objects.get(pk=user_id).username,
                           'explains': explains, 'explain_count':explain_count,
                           'type': 'oxygen'}
                return render(request, 'mhuser/oxygen.html', context)
            else:  # 无权限查看
                return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
        # 当前用户是普通用户
        elif request.user.usertype == 'normal':
            # 获取用户信息
            try:
                profile = NormalUser.objects.get(user=request.user)
            except ValueError:
                profile.avatar = NormalUser.objects.get(user_id=3).avatar
            data = OxygenData.objects.filter(own=NormalUser.objects.get(user=request.user))
            explains = getexplainlist(request, user_id, 'oxygen')
            explain_count = len(explains)
            context = {'ck': ck, 'profile': profile, 'data': data,
                       'owner': MhUser.objects.get(pk=user_id).username,
                       'explains': explains, 'explain_count':explain_count,
                       'type': 'oxygen'}
            return render(request, 'mhuser/oxygen.html', context)


@login_required
def tem(request, user_id):
    if request.method == "GET":
        ck = CKEditorForm()
        # 当前用户是医生
        if request.user.usertype == 'doctor':
            # 获取用户信息
            try:
                profile = DoctorUser.objects.get(user=request.user)
            except ValueError:
                profile.avatar = NormalUser.objects.get(user_id=3).avatar
            # 检查是否有权限查看
            if is_perm(DoctorUser.objects.get(user=request.user), NormalUser.objects.get(pk=user_id), 'tem'):
                # data = TemData.objects.filter(own=NormalUser.objects.get(pk=user_id))
                explains = getexplainlist(request, user_id, 'tem')
                explain_count = len(explains)
                context = {'ck': ck, 'profile': profile,
                           'owner': MhUser.objects.get(pk=user_id).username,
                           'explains': explains, 'explain_count': explain_count,
                           'type':'tem'}
                return render(request, 'mhuser/tem.html', context)
            else:  # 无权限查看
                return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
        # 当前用户是普通用户
        elif request.user.usertype == 'normal':
            # 获取用户信息
            try:
                profile = NormalUser.objects.get(user=request.user)
            except ValueError:
                profile.avatar = NormalUser.objects.get(user_id=3).avatar
            # data = TemData.objects.filter(own=NormalUser.objects.get(user=request.user))
            explains = getexplainlist(request, user_id, 'tem')
            explain_count = len(explains)
            context = {'ck': ck, 'profile': profile,
                       'owner': MhUser.objects.get(pk=user_id).username,
                       'explains': explains, 'explain_count': explain_count,
                       'type':'tem'}
            return render(request, 'mhuser/tem.html', context)


@login_required
def pressure(request, user_id):
    normal_user = NormalUser.objects.get(pk=user_id)
    if request.method == "GET":
        ck = CKEditorForm()
        # 当前用户是医生
        if request.user.usertype == 'doctor':
            # 获取用户信息
            try:
                profile = DoctorUser.objects.get(user=request.user)
            except ValueError:
                profile.avatar = NormalUser.objects.get(user_id=3).avatar
            # 检查是否有权限查看
            if is_perm(DoctorUser.objects.get(user=request.user), normal_user, 'pressure'):
                data = PressureData.objects.filter(own=NormalUser.objects.get(pk=user_id))
                explains = getexplainlist(request, user_id, 'pressure')
                explain_count = len(explains)
                context = {'ck': ck, 'profile': profile, 'data': data,
                           'owner': MhUser.objects.get(pk=user_id).username,
                           'explains': explains, 'explain_count': explain_count,
                           'type': 'pressure'}
                return render(request, 'mhuser/pressure.html', context)
            else:  # 无权限查看
                return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
        # 当前用户是普通用户
        elif request.user.usertype == 'normal':
            # 获取用户信息
            try:
                profile = NormalUser.objects.get(user=request.user)
            except ValueError:
                profile.avatar = NormalUser.objects.get(user_id=3).avatar
            data = PressureData.objects.filter(own=NormalUser.objects.get(user=request.user))
            explains = getexplainlist(request, user_id, 'pressure')
            explain_count = len(explains)
            context = {'ck': ck, 'profile': profile, 'data': data,
                       'owner': MhUser.objects.get(pk=user_id).username,
                       'explains': explains, 'explain_count': explain_count,
                       'type': 'pressure'}
            return render(request, 'mhuser/pressure.html', context)


def ajax_pressure(request):
    data = PressureData.objects.all()
    d = []
    for i in range(0, len(data)):
        d.append(data[i].value)
        d.append(',')
    return HttpResponse(d)


def ajax_tem(request):
    data = TemData.objects.all()
    d = []
    for i in range(0, len(data)):
        d.append(data[i].value)
        d.append(',')
    return HttpResponse(d)

