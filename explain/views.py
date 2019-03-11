from django.shortcuts import render
from .models import Explain
from mhuser.models import MhUser, DoctorUser, NormalUser, Match
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ExplainForm
# Create your views here.


def addexplain(request, own, type):
    if request.method == "POST":
        own_user = NormalUser.objects.get(user=MhUser.objects.get(username=own))
        explain = ExplainForm(request.POST)
        if explain.is_valid():
            context = request.POST['content']
            match = Match.objects.get(normaluser=own_user, charged=type)
            Explain(match=match, author=request.user, context=context, touserid=own_user).save()
        return HttpResponseRedirect(''.join(('/mhuser/', type, '/', str(MhUser.objects.get(username=own).id))))

def getexplainlist(request, own_id, type):
    own_user = NormalUser.objects.get(user=MhUser.objects.get(id=int(own_id)))
    try:
        match = Match.objects.get(normaluser=own_user, charged=type)
        explains = Explain.objects.filter(match=match)
        for e in explains:
            e.read = True
        return explains
    except Match.DoesNotExist:
        return HttpResponse('error')



