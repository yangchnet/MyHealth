from django.shortcuts import render
from .models import Explain
from mhuser.models import MhUser, DoctorUser, NormalUser, Match
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ExplainForm
# Create your views here.


def addexplain(request, path):
    if request.method == "POST":
        p = path.split('/')
        type = p[2]
        ownid = p[3]
        own_user = MhUser.objects.get(id=int(ownid))
        explain = ExplainForm(request.POST)
        if explain.is_valid():
            context = request.POST['content']
            match = Match.objects.get(normaluser=NormalUser.objects.get(user=own_user), charged=type)
            Explain(match=match, author=request.user, context=context, touserid=own_user).save()
        return HttpResponseRedirect(''.join(('/mhuser/', type, '/', ownid)))
    # return HttpResponseRedirect(request.path)

def getexplainlist(request):
    p = request.path.split('/')
    type = p[2]
    ownid = p[3]
    own_user = MhUser.objects.get(id=int(ownid))
    match = Match.objects.get(normaluser=NormalUser.objects.get(user=own_user), charged=type)
    explains = Explain.objects.filter(match=match)
    for e in explains:
        e.read = True
    return explains



