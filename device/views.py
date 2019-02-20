from django.shortcuts import render

# Create your views here.
def device(request, device_id):
    return render(request, 'device/device.html')

def devices(request):
    return render(request, 'device/devices.html')
