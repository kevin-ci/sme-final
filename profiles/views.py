from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm

# Create your views here.


@login_required
def view_profile(request, user_id):
    """ Display the user's profile. """
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)
    is_self = True if user_id == str(request.user.id) else False
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'is_self': is_self,
    }

    return render(request, template, context)


@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Your profile has been updated!')
            return redirect(reverse('profile', args=[request.user.id]))
        # else:
            # messages.error(request, ('Profile update failed.'))
    else:
        form = UserProfileForm(instance=profile)

    template = 'profiles/edit_profile.html'
    context = {
        'form': form,
        'profile': profile,
    }

    return render(request, template, context)


def view_profiles(request):
    profiles = UserProfile.objects.all()
    template = 'profiles/view_profiles.html'
    context = {
        'profiles': profiles,
    }

    return render(request, template, context)
