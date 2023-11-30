from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import UserProfile, Connection
from .forms import UserProfileForm

# Create your views here.


@login_required
def view_profile(request, user_id):
    """ Display the user's profile. """
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)
    
    is_self = user_id == str(request.user.id)
    is_connected = False
    
    if not is_self:
        logged_in_profile = get_object_or_404(UserProfile, user=request.user)
        is_connected = Connection.connection_exists(profile, logged_in_profile)

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'is_self': is_self,
        'is_connected': is_connected,
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

@login_required
def add_connection(request, id):
    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(UserProfile, user=user)
    logged_in_profile = get_object_or_404(UserProfile, user=request.user)

    connection = Connection(from_user=logged_in_profile, to_user=profile)
    
    try:
        connection.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'failure', 'error_message': str(e)})

    
@login_required
def remove_connection(request, id):
    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(UserProfile, user=user)
    logged_in_profile = get_object_or_404(UserProfile, user=request.user)

    connection = Connection.get_connection(logged_in_profile, profile)

    try:
        connection.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'failure', 'error_message': str(e)})