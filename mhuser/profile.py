from .models import MhUser, Match, NormalUser, DoctorUser


def get_profile(user):
    try:
        if user.usertype == 'normal':
            profile = NormalUser.objects.get(user=user)
        else:
            profile = DoctorUser.objects.get(user=user)
    except ValueError:
        profile.avatar = NormalUser.objects.get(user_id=1).avatar
    return profile