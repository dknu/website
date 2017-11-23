from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import re

from .models import Profile, Skill, Group
from .forms import ProfileModelFormUser, ProfileModelFormMember, ProfileModelFormAdmin


def members(request):
    profiles = Profile.objects.exclude(group__isnull=True)
    if request.method == 'POST':
        text = request.POST['searchBar'].lower()
        tokens = re.split('; |, |  |\n', text)
        result_profiles = []

        for token in tokens:
            first_name_results = User.objects.filter(first_name__icontains=token)
            last_name_results = User.objects.filter(last_name__icontains=token)
            skill_results = Skill.objects.filter(title__icontains=token)
            group_results = Group.objects.filter(title__icontains=token)

        for profile in profiles:
            if profile.user in first_name_results or profile.user in last_name_results:
                result_profiles.append(profile)
            for skill in profile.skills.all():
                if skill in skill_results and profile not in result_profiles:
                    result_profiles.append(profile)
            for group in profile.group.all():
                if group in group_results and profile not in result_profiles:
                    result_profiles.append(profile)
        return render(request, "members.html", context={"profiles": result_profiles})

    return render(request, "members.html", context={"profiles": profiles})


def skill(request, skill_title):
    skill = Skill.objects.get(title=skill_title)
    profiles = Profile.objects.filter(skills__title__icontains=skill_title, group__isnull=False)
    context = {'skill': skill, 'profiles': profiles}
    return render(request, 'skill.html', context)


"""
def group(request):
    context = {'group': request.path.split("/")[-1]}
    return render(request, "group.html", context)
"""


def profile(request, profileID):
    try:
        profile = Profile.objects.get(user_id=profileID)
        profile.update()
        return render(request, 'profile.html', {'profile': profile, 'user': request.user})
    except Profile.DoesNotExist:
        return render(request, '404.html')


def edit_profile(request):
    return edit_profile_id(request, request.user.id)


def edit_profile_id(request, profileID):
    try:
        user = request.user
        profile = Profile.objects.get(user_id=profileID)
        if user != profile.user and not user.is_superuser:
            return redirect('/members/profile/' + str(profileID))
        if user.is_superuser:
            form = ProfileModelFormAdmin(request.POST or None, request.FILES or None, instance=profile)
        elif Profile.objects.filter(user=user, group__isnull=False):
            form = ProfileModelFormMember(request.POST or None, request.FILES or None, instance=profile)
        else:
            form = ProfileModelFormUser(request.POST or None, request.FILES or None, instance=profile)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('/members/profile/' + str(profileID))
        return render(request, 'edit_profile.html', {'form': form, 'profile': profile})
    except Profile.DoesNotExist:
        return render(request, '404.html')
