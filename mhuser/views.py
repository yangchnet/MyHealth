from .models import MhUser, Match, NormalUser, DoctorUser, \
    HeartData, OxygenData, TemData, PressureData, Chgpasswd
from .forms import Register, Login, DateForm, FindPasswdForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from comment.views import *
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from explain.views import getexplainlist
from .extract import tem_data, pres_data, oxygen_data, heart_data
from .profile import get_profile
from django.core.mail import send_mail
import random
from django.http import JsonResponse

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
                                                       mypassword=user.cleaned_data['user_password'])  # 兼容android
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
            try:
                MhUser.objects.get(username=user.cleaned_data['user_name'])
            except MhUser.DoesNotExist:
                context = {'username_ph': '用户名不存在'}
                return render(request, 'mhuser/login.html', context)

            curr_user = auth.authenticate(username=user.cleaned_data['user_name'],
                                              password=user.cleaned_data['user_password'])
            if curr_user is not None:
                login(request, curr_user)
                return HttpResponseRedirect('/myhealth')
            else:
                context = {'password_ph': '密码错误'}
                return render(request, 'mhuser/login.html', context)
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
        profile = get_profile(request.user)
        notice = request.user.notifications.unread()
        context = {'notices': notice, 'profile': profile, 'doctors': doctors}
        return render(request, 'mhuser/doctors.html', context)
    context = {'doctors': doctors}
    return render(request, 'mhuser/doctors.html', context)


def doctor(request, doctor_id):
    return render(request, 'mhuser/doctor.html')


@login_required
def profile(request):
    profile = get_profile(request.user)
    return render(request, 'mhuser/profile.html', {'profile': profile})


def is_perm(doctor, user, charged):
    try:
        Match.objects.get(doctor=doctor, normaluser=user, charged=charged)
        return 1
    except Match.DoesNotExist:
        return 0





@login_required
def notification(request, page_id):
    profile = get_profile(request.user)
    curr_user = request.user
    unread = curr_user.notifications.unread()[10 * (page_id - 1): 10 * page_id]
    context = {'profile': profile, 'unread': unread, 'page_range': range(page_id, page_id + 4), 'page_id': page_id}
    return render(request, 'mhuser/notification.html', context)


@login_required
def noti(request, noti_id):
    curr_user = request.user
    unread = Notification.objects.get(id=noti_id)
    profile = get_profile(request.user)
    context = {'profile': profile, 'unread': unread}
    unread.mark_as_read()
    return render(request, 'mhuser/noti.html', context)


@login_required
def myclient(request):
    curr_user = request.user
    # 用户个人信息获取
    profile = get_profile(request.user)

    # 通过match表找到我的客户
    match = Match.objects.filter(doctor=DoctorUser.objects.get(user=curr_user))
    return render(request, 'mhuser/myclient.html', {'profile': profile, 'match': match})


@login_required
def oxygen(request, user_id):
    ck = CKEditorForm()
    dateform = DateForm(request.POST)
    if request.method == "GET":
        # 当前用户是医生
        if request.user.usertype == 'doctor':
            # 获取用户信息
            profile = get_profile(request.user)
            # 检查是否有权限查看
            if is_perm(DoctorUser.objects.get(user=request.user), NormalUser.objects.get(pk=user_id), 'oxygen'):
                explains = getexplainlist(request, user_id, 'oxygen')
                try:
                    explain_count = len(explains)
                except TypeError:
                    explain_count = 0
                hr_data, spo2 = oxygen_data(OxygenData.objects.filter(own=NormalUser.objects.get(pk=user_id)))
                data = OxygenData.objects.filter(own=NormalUser.objects.get(pk=user_id))
                context = {'ck': ck, 'profile': profile, 'form': dateform,
                           'owner': MhUser.objects.get(pk=user_id).username,
                           'explains': explains, 'explain_count': explain_count,
                           'type': 'oxygen', 'hr_data': hr_data, 'spo2': spo2, 'data': data}
                return render(request, 'mhuser/oxygen.html', context)
            else:  # 无权限查看
                return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
        # 当前用户是普通用户
        elif request.user.usertype == 'normal':
            # 获取用户信息
            profile = get_profile(request.user)
            explains = getexplainlist(request, user_id, 'oxygen')
            try:
                explain_count = len(explains)
            except TypeError:
                explain_count = 0
            hr_data, spo2 = oxygen_data(OxygenData.objects.filter(own=NormalUser.objects.get(user=request.user)))
            data = OxygenData.objects.filter(own=NormalUser.objects.get(pk=user_id))
            context = {'ck': ck, 'profile': profile, 'form': dateform,
                       'owner': MhUser.objects.get(pk=user_id).username,
                       'explains': explains, 'explain_count': explain_count,
                       'type': 'oxygen', 'hr_data': hr_data, 'spo2': spo2, 'data': data}
            return render(request, 'mhuser/oxygen.html', context)
        else:
            return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
    elif request.method == 'POST':
        dateform = DateForm(request.POST)
        profile = get_profile(request.user)
        explains = getexplainlist(request, user_id, 'oxygen')
        try:
            explain_count = len(explains)
        except TypeError:
            explain_count = 0
        if dateform.is_valid():
            hr_data, spo2 = oxygen_data(OxygenData.objects.filter(
                own=NormalUser.objects.get(user=request.user),
                time__range=(dateform.cleaned_data['start_date'], dateform.cleaned_data['end_date'])))
            data = OxygenData.objects.filter(
                time__range=(dateform.cleaned_data['start_date'], dateform.cleaned_data['end_date']),
                own=NormalUser.objects.get(pk=user_id))
        dateform = DateForm()
        context = {'ck': ck, 'profile': profile, 'form': dateform,
                   'owner': MhUser.objects.get(pk=user_id).username,
                   'explains': explains, 'explain_count': explain_count,
                   'type': 'heartbeat', 'hr_data': hr_data, 'spo2': spo2, 'data': data}
        return render(request, 'mhuser/test.html', context)

@login_required
def heartbeat(request, user_id):
    ck = CKEditorForm()
    dateform = DateForm(request.POST)
    if request.method == "GET":
        # 当前用户是医生
        if request.user.usertype == 'doctor':
            # 获取用户信息
            profile = get_profile(request.user)
            # 检查是否有权限查看
            if is_perm(DoctorUser.objects.get(user=request.user), NormalUser.objects.get(pk=user_id), 'heartbeat'):
                explains = getexplainlist(request, user_id, 'heartbeat')
                try:
                    explain_count = len(explains)
                except TypeError:
                    explain_count = 0
                s_data = heart_data(HeartData.objects.filter(own=NormalUser.objects.get(pk=user_id)))
                data = HeartData.objects.filter(own=NormalUser.objects.get(pk=user_id))
                context = {'ck': ck, 'profile': profile, 'form': dateform,
                           'owner': MhUser.objects.get(pk=user_id).username,
                           'explains': explains, 'explain_count': explain_count,
                           'type': 'heartbeat', 's_data': s_data, 'data': data}
                return render(request, 'mhuser/heartbeat.html', context)
            else:  # 无权限查看
                return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
        # 当前用户是普通用户
        elif request.user.usertype == 'normal':
            # 获取用户信息
            profile = get_profile(request.user)
            explains = getexplainlist(request, user_id, 'heartbeat')
            try:
                explain_count = len(explains)
            except TypeError:
                explain_count = 0
            data_length = len(HeartData.objects.all())
            s_data = heart_data(HeartData.objects.filter(
                own=NormalUser.objects.get(user=request.user), id__range=(data_length-500, data_length)))
            data = HeartData.objects.filter(own=NormalUser.objects.get(pk=user_id))
            context = {'ck': ck, 'profile': profile, 'form': dateform,
                       'owner': MhUser.objects.get(pk=user_id).username,
                       'explains': explains, 'explain_count': explain_count,
                       'type': 'heartbeat', 's_data': s_data, 'data': data}
            return render(request, 'mhuser/heartbeat.html', context)
        else:
            return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
    elif request.method == 'POST':  # 发出按时间查询请求
        dateform = DateForm(request.POST)
        profile = get_profile(request.user)
        explains = getexplainlist(request, user_id, 'heartbeat')
        try:
            explain_count = len(explains)
        except TypeError:
            explain_count = 0
        if dateform.is_valid():
            s_data = HeartData.objects.filter(
                time__range=(dateform.cleaned_data['start_date'], dateform.cleaned_data['end_date']),
                own=NormalUser.objects.get(pk=user_id))
            data = HeartData.objects.filter(
                time__range=(dateform.cleaned_data['start_date'], dateform.cleaned_data['end_date']),
                own=NormalUser.objects.get(pk=user_id))
        dateform = DateForm()
        context = {'ck': ck, 'profile': profile, 'form': dateform,
                   'owner': MhUser.objects.get(pk=user_id).username,
                   'explains': explains, 'explain_count': explain_count,
                   'type': 'heartbeat', 's_data': s_data, 'data': data}
        return render(request, 'mhuser/test.html', context)

@login_required
def tem(request, user_id):
    ck = CKEditorForm()
    dateform = DateForm(request.POST)
    if request.method == "GET":
        # 当前用户是医生
        if request.user.usertype == 'doctor':
            # 获取用户信息
            profile = get_profile(request.user)
            # 检查是否有权限查看
            if is_perm(DoctorUser.objects.get(user=request.user), NormalUser.objects.get(pk=user_id), 'tem'):

                explains = getexplainlist(request, user_id, 'tem')
                try:
                    explain_count = len(explains)
                except TypeError:
                    explain_count = 0
                tm_data = tem_data(TemData.objects.filter(own=NormalUser.objects.get(pk=user_id)))
                data = TemData.objects.filter(own=NormalUser.objects.get(pk=user_id))
                context = {'ck': ck, 'profile': profile,'form': dateform,
                           'owner': MhUser.objects.get(pk=user_id).username,
                           'explains': explains, 'explain_count': explain_count,
                           'type': 'tem', 'data': data, 'tm_data':tm_data}
                return render(request, 'mhuser/tem.html', context)
            else:  # 无权限查看
                return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
        # 当前用户是普通用户
        elif request.user.usertype == 'normal':
            # 获取用户信息
            profile = get_profile(request.user)
            # data = TemData.objects.filter(own=NormalUser.objects.get(user=request.user))
            explains = getexplainlist(request, user_id, 'tem')
            try:
                explain_count = len(explains)
            except TypeError:
                explain_count = 0
            tm_data = tem_data(TemData.objects.filter(own=NormalUser.objects.get(user=request.user)))
            data = TemData.objects.filter(own=NormalUser.objects.get(pk=user_id))
            context = {'ck': ck, 'profile': profile,'form': dateform,
                       'owner': MhUser.objects.get(pk=user_id).username,
                       'explains': explains, 'explain_count': explain_count,
                       'type': 'tem', 'data': data, 'tm_data':tm_data}
            return render(request, 'mhuser/tem.html', context)
    elif request.method == 'POST':
        dateform = DateForm(request.POST)
        profile = get_profile(request.user)
        explains = getexplainlist(request, user_id, 'oxygen')
        try:
            explain_count = len(explains)
        except TypeError:
            explain_count = 0
        if dateform.is_valid():
            tm_data = tem_data(TemData.objects.filter(own=NormalUser.objects.get(user=request.user),
                                                   time__range=(dateform.cleaned_data['start_date'],
                                                                dateform.cleaned_data['end_date']),))
            data = TemData.objects.filter(
                time__range=(dateform.cleaned_data['start_date'], dateform.cleaned_data['end_date']),
                own=NormalUser.objects.get(pk=user_id))
        dateform = DateForm()
        context = {'ck': ck, 'profile': profile, 'form': dateform,
                   'owner': MhUser.objects.get(pk=user_id).username,
                   'explains': explains, 'explain_count': explain_count,
                   'type': 'heartbeat', 'data': data, 'tem_data': tm_data}
        return render(request, 'mhuser/test.html', context)



@login_required
def pressure(request, user_id):
    dateform = DateForm(request.POST)
    ck = CKEditorForm()
    normal_user = NormalUser.objects.get(pk=user_id)
    if request.method == "GET":

        # 当前用户是医生
        if request.user.usertype == 'doctor':
            # 获取用户信息
            profile = get_profile(request.user)
            # 检查是否有权限查看
            if is_perm(DoctorUser.objects.get(user=request.user), normal_user, 'pressure'):
                # data = PressureData.objects.filter(own=NormalUser.objects.get(pk=user_id))
                explains = getexplainlist(request, user_id, 'pressure')
                try:
                    explain_count = len(explains)
                except TypeError:
                    explain_count = 0
                data = PressureData.objects.filter(own=NormalUser.objects.get(pk=user_id))
                bpss_data, bpsz_data = pres_data(PressureData.objects.filter(own=NormalUser.objects.get(pk=user_id)))
                context = {'ck': ck, 'profile': profile,'form':dateform,
                           'owner': MhUser.objects.get(pk=user_id).username,
                           'explains': explains, 'explain_count': explain_count,
                           'type': 'pressure', 'bpss_data': bpss_data,
                           'bpsz_data': bpsz_data, 'data':data}
                return render(request, 'mhuser/pressure.html', context)
            else:  # 无权限查看
                return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
        # 当前用户是普通用户
        elif request.user.usertype == 'normal':
            # 获取用户信息
            profile = get_profile(request.user)
            # data = PressureData.objects.filter(own=NormalUser.objects.get(user=request.user))
            explains = getexplainlist(request, user_id, 'pressure')
            try:
                explain_count = len(explains)
            except TypeError:
                explain_count = 0
            data = PressureData.objects.filter(own=NormalUser.objects.get(pk=user_id))
            bpss_data, bpsz_data = pres_data(PressureData.objects.filter(own=NormalUser.objects.get(user=request.user)))
            context = {'ck': ck, 'profile': profile,'form':dateform,
                       'owner': MhUser.objects.get(pk=user_id).username,
                       'explains': explains, 'explain_count': explain_count,
                       'type': 'pressure', 'bpss_data': bpss_data,
                       'bpsz_data': bpsz_data, 'data':data}
            return render(request, 'mhuser/pressure.html', context)
        else:
            return HttpResponse('请求被拒绝，您可能没有权限访问该数据')
    elif request.method == 'POST':
        dateform = DateForm(request.POST)
        profile = get_profile(request.user)
        explains = getexplainlist(request, user_id, 'oxygen')
        try:
            explain_count = len(explains)
        except TypeError:
            explain_count = 0
        if dateform.is_valid():
            bpss_data, bpsz_data = pres_data(PressureData.objects.filter(
                own=NormalUser.objects.get(pk=user_id),
                time__range=(dateform.cleaned_data['start_date'], dateform.cleaned_data['end_date'])))
            data = PressureData.objects.filter(
                time__range=(dateform.cleaned_data['start_date'], dateform.cleaned_data['end_date']),
                own=NormalUser.objects.get(pk=user_id))
        dateform = DateForm()
        context = {'ck': ck, 'profile': profile, 'form': dateform,
                   'owner': MhUser.objects.get(pk=user_id).username,
                   'explains': explains, 'explain_count': explain_count,
                   'type': 'heartbeat', 'hr_data': bpss_data, 'bpsz_data': bpsz_data, 'data': data}
        return render(request, 'mhuser/test.html', context)


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


def test(request, user_id):
    s_data = heart_data(HeartData.objects.filter(own=NormalUser.objects.get(pk=user_id)))
    data = HeartData.objects.filter(own=NormalUser.objects.get(pk=user_id))
    if request.method == "GET":
        dateform = DateForm()
        context = {'form': dateform, 's_data': s_data, 'data': data}
        return render(request, 'mhuser/test.html', context)
    else:
        dateform = DateForm(request.POST)
        if dateform.is_valid():
            s_data = HeartData.objects.filter(
                time__range=(dateform.cleaned_data['start_date'], dateform.cleaned_data['end_date']),
                own=NormalUser.objects.get(pk=user_id))
            data = HeartData.objects.filter(
                time__range=(dateform.cleaned_data['start_date'], dateform.cleaned_data['end_date']),
                own=NormalUser.objects.get(pk=user_id))
        dateform = DateForm()
        context = {'form': dateform, 's_data': s_data, 'data': data}
        return render(request, 'mhuser/test.html', context)

@csrf_exempt
def ver_ajax(request):
    vertification = random.randint(10000, 99999)
    while True:
        try:
            Chgpasswd.objects.get(vertification=vertification)
            vertification = random.randint(10000, 99999)
        except:
            break
        # if Chgpasswd.objects.get(vertification=vertification):
        #     vertification = random.randint(10000, 99999)
        # else:
        #     break
    if request.is_ajax():
        # data = request.POST
        email = request.GET.get('email')
    Chgpasswd(email=email, vertification=vertification).save()
    send_mail(
            'Change Password',
            '您正在尝试更改MyHealth站点的密码，验证码是{0}，如果非本人操作，请忽略此信息。'.format(vertification),
            '1048887414@qq.com',
            ['{0}'.format(email)],
            fail_silently=False,
        )
    response = JsonResponse({"info": "email is successfully send"})
    return response


def forgetpassword(request):
    if request.method == 'GET':
        return render(request, 'mhuser/forgetpassword.html')
    if request.method == 'POST':
        findpasswdform = FindPasswdForm(request.POST)
        if findpasswdform.is_valid():
            vertf_get = findpasswdform.cleaned_data['verification']
            passwd_get = findpasswdform.cleaned_data['new_passwd']
            retypepasswd_get = findpasswdform.cleaned_data['retype_passwd']
            vert = Chgpasswd.objects.get(vertification=int(vertf_get))
            if vert and passwd_get == retypepasswd_get:
                email = vert.email
                user = MhUser.objects.get(email=email)
                user.set_password(passwd_get)
                user.save()
            vert.delete()
            return HttpResponseRedirect('/mhuser/login')
    return render(request, 'mhuser/forgetpassword.html')