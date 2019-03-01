from django.shortcuts import render
from mhuser.models import NormalUser, DoctorUser
from .models import Device


# Create your views here.
def device(request, device_id):
    device = Device.objects.get(pk=device_id)
    if request.user.is_authenticated:
        try:
            if request.user.usertype == 'normal':
                profile = NormalUser.objects.get(user=request.user)
            else:
                profile = DoctorUser.objects.get(user=request.user)
        except ValueError:
            profile.avatar = NormalUser.objects.get(user_id=3).avatar
        return render(request, 'device/device.html', {'profile': profile, 'device': device})
    return render(request, 'device/device.html', {'device': device})


def devices(request):
    devices = Device.objects.all()
    if request.user.is_authenticated:
        try:
            if request.user.usertype == 'normal':
                profile = NormalUser.objects.get(user=request.user)
            else:
                profile = DoctorUser.objects.get(user=request.user)
        except BaseException:
            profile.avatar = NormalUser.objects.get(user_id=3).avatar
        return render(request, 'device/devices.html', {'profile': profile, 'devices': devices})
    return render(request, 'device/devices.html', {'devices': devices})
