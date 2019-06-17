from .models import MhUser, Match, NormalUser, DoctorUser, HeartData, OxygenData, TemData, PressureData
import json
import datetime

def tem_data(queryset):
    result = []
    for q in queryset.reverse():
        r = []
        r.append(str(q.time))
        r.append(q.tem_value)
        result.append(r)
    return json.dumps(result)

def pres_data(queryset):
    bpss_result = []
    bpsz_result = []
    for q in queryset.reverse():
        bpss_r = []
        bpss_r.append(str(q.time))
        bpss_r.append(q.bpss_value)
        bpss_result.append(bpss_r)

        bpsz_r = []
        bpsz_r.append(str(q.time))
        bpsz_r.append(q.bpsz_value)
        bpsz_result.append(bpsz_r)

    return json.dumps(bpss_result), json.dumps(bpsz_result)


def oxygen_data(quertset):
    hr_result = []
    spo2_result = []
    for q in quertset.reverse():
        hr_r = []
        hr_r.append(str(q.time))
        hr_r.append(q.hr_value)
        hr_result.append(hr_r)


        spo2_r = []
        spo2_r.append(str(q.time))
        spo2_r.append(q.spo2)
        spo2_result.append(spo2_r)

    return json.dumps(hr_result), json.dumps(spo2_result)

def heart_data(quertset):
    s_result = []
    for q in quertset.reverse():
    # for q in quertset:
        s_r = []
        s_r.append(str(q.time))
        s_r.append(q.s_value)
        s_result.append(s_r)

    return json.dumps(s_result)

