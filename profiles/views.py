from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from itertools import chain
from .models import UserProfile, Connection, Company
from .forms import UserProfileForm, JobForm

# Create your views here.

@login_required
def view_profile(request, user_id):
    """ Display the user's profile. """
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)
    jobs = profile.jobs.all().order_by('start_date')
    
    is_self = user_id == str(request.user.id)
    is_connected = False
    
    if not is_self:
        logged_in_profile = get_object_or_404(UserProfile, user=request.user)
        is_connected = Connection.connection_exists(profile, logged_in_profile)
        
    connections_from = Connection.objects.filter(from_user=profile).select_related('to_user')
    connections_to = Connection.objects.filter(to_user=profile).select_related('from_user')

    profiles_from = [connection.to_user for connection in connections_from]
    profiles_to = [connection.from_user for connection in connections_to]

    all_connected_profiles = list(set(chain(profiles_from, profiles_to)))
    
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'is_self': is_self,
        'is_connected': is_connected,
        'jobs': jobs,
        'connections': all_connected_profiles,
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
    

@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, id=request.user.id)
            profile = get_object_or_404(UserProfile, user=user)
            
            job = form.save(commit=False)
            company_name = form.cleaned_data.get('company_name')
            company, created = Company.objects.get_or_create(name=company_name)
            job.company = company
            job.user = profile
            job.save()

            return redirect('profile', user_id=profile.id)  # Change 'user_profile' to your actual profile URL name
    else:
        form = JobForm()

    return render(request, 'profiles/add_job.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect, render
from .models import Job
from .forms import JobForm  # Import your JobForm

@login_required
def edit_job(request, id):
    job = get_object_or_404(Job, id=id)
    user = get_object_or_404(User, id=request.user.id)
    profile = get_object_or_404(UserProfile, user=user)
    
    if job.user.id == profile.id:
        if request.method == 'POST':
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                company_name = form.cleaned_data.get('company_name')
                company, created = Company.objects.get_or_create(name=company_name)
                
                job = form.save(commit=False)
                job.company = company
                job.save()

                return redirect('profile', user_id=profile.id)  # Redirect to the user's profile page after editing the job
        else:
           # Retrieve the related company name for the job being edited
            initial_company_name = job.company.name if job.company else ''

            # Populate the form with the job instance data and initial company name
            form = JobForm(instance=job, initial={'company_name': initial_company_name})

        return render(request, 'profiles/edit_job.html', {'form': form, 'job': job})
    else:
        return redirect('home')
    
    
@login_required
def delete_job(request, id):
    job = get_object_or_404(Job, id=id)
    user = get_object_or_404(User, id=request.user.id)
    profile = get_object_or_404(UserProfile, user=user)
    
    if job.user.id == profile.id:
        job.delete()
        return redirect('profile', user_id=profile.id)  # Redirect to the user's profile page after editing the job
    else:
        return redirect('home')
