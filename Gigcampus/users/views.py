from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView 
from .forms import SignUpForm
from projects.models import Project, Bid
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .forms import ProfileUpdateForm, NotificationPreferencesForm, PlatformPreferencesForm
from .models import Profile


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

@login_required
def dashboard(request):
    profile = request.user.profile
    context = {'profile': profile}
    
    if profile.role == 'client':
        context['my_projects'] = Project.objects.filter(posted_by=request.user)
    else:
        context['my_bids'] = Bid.objects.filter(freelancer=request.user)
        
    return render(request, 'users/dashboard.html', context)
@login_required
def settings_view(request):
    profile = request.user.profile
    
    # Initialize forms
    profile_form = ProfileUpdateForm(instance=profile, user=request.user)
    notification_form = NotificationPreferencesForm(instance=profile)
    platform_form = PlatformPreferencesForm(instance=profile)
    password_form = PasswordChangeForm(request.user)
    
    context = {
        'profile_form': profile_form,
        'notification_form': notification_form,
        'platform_form': platform_form,
        'password_form': password_form,
    }
    
    return render(request, 'settings.html', context)

@login_required
@require_POST
def update_profile(request):
    form = ProfileUpdateForm(request.POST, instance=request.user.profile, user=request.user)
    
    if form.is_valid():
        # Update user fields
        user = request.user
        user.first_name = form.cleaned_data.get('first_name', '')
        user.last_name = form.cleaned_data.get('last_name', '')
        user.email = form.cleaned_data.get('email', '')
        user.save()
        
        # Update profile
        form.save()
        
        messages.success(request, 'Profile updated successfully!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def update_notifications(request):
    form = NotificationPreferencesForm(request.POST, instance=request.user.profile)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Notification preferences updated successfully!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def update_platform_preferences(request):
    form = PlatformPreferencesForm(request.POST, instance=request.user.profile)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Platform preferences updated successfully!')
        
        # If theme changed, return JSON response for AJAX
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({
                'success': True,
                'theme': form.cleaned_data['theme'],
                'message': 'Theme updated successfully!'
            })
    else:
        messages.error(request, 'Please correct the errors below.')
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return redirect('settings')

@login_required
@require_POST
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # Important: keeps user logged in
        messages.success(request, 'Your password was successfully updated!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
def get_user_preferences(request):
    """API endpoint to get user preferences for JavaScript"""
    profile = request.user.profile
    preferences = {
        'theme': profile.theme,
        'language': profile.language,
        'profile_public': profile.profile_public,
        'show_online_status': profile.show_online_status,
        'notifications': {
            'email_projects': profile.email_projects,
            'email_bids': profile.email_bids,
            'email_messages': profile.email_messages,
            'email_payments': profile.email_payments,
            'push_messages': profile.push_messages,
            'push_bids': profile.push_bids,
        }
    }
    return JsonResponse(preferences)


def about_view(request):
    return render(request, 'about.html')

@login_required
def analytics_view(request):
    profile = request.user.profile
    
    # Calculate analytics data
    if profile.role == 'client':
        total_projects = Project.objects.filter(posted_by=request.user).count()
        total_spent = sum(p.budget for p in Project.objects.filter(posted_by=request.user, status='completed'))
        avg_rating = 4.5  # Calculate from reviews
    else:
        total_projects = Bid.objects.filter(freelancer=request.user, status='accepted').count()
        total_spent = sum(b.amount for b in Bid.objects.filter(freelancer=request.user, status='accepted', project__status='completed'))
        avg_rating = profile.rating
    
    context = {
        'total_projects': total_projects,
        'total_earnings': total_spent,
        'avg_rating': avg_rating,
    }
    return render(request, 'analytics.html', context)

@login_required
def field_demand_view(request):
    return render(request, 'field_demand.html')

@login_required
def skills_assessment_view(request):
    return render(request, 'skills_assessment.html')

@login_required
def earnings_tracker_view(request):
    return render(request, 'earnings_tracker.html')

@login_required
def my_projects_view(request):
    projects = Project.objects.filter(posted_by=request.user)
    return render(request, 'my_projects.html', {'projects': projects})

@login_required
def my_bids_view(request):
    bids = Bid.objects.filter(freelancer=request.user)
    return render(request, 'my_bids.html', {'bids': bids})

@login_required
def messages_view(request):
    return render(request, 'messages.html')

@login_required
def activity_log_view(request):
    return render(request, 'activity_log.html')

@login_required
def help_view(request):
    return render(request, 'help.html')

@login_required
def upgrade_view(request):
    return render(request, 'upgrade.html')