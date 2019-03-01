from django.shortcuts import render
from mhuser.models import NormalUser, DoctorUser


# Create your views here.
def device(request, device_id):
    try:
        if request.user.usertype == 'normal':
            profile = NormalUser.objects.get(user=request.user)
        else:
            profile = DoctorUser.objects.get(user=request.user)
    except ValueError:
        profile.avatar = NormalUser.objects.get(user_id=3).avatar
    return render(request, 'device/device.html', {'profile':profile})


def devices(request):
    try:
        if request.user.usertype == 'normal':
            profile = NormalUser.objects.get(user=request.user)
        else:
            profile = DoctorUser.objects.get(user=request.user)
    except ValueError:
        profile.avatar = NormalUser.objects.get(user_id=3).avatar
    return render(request, 'device/devices.html', {'profile':profile})
