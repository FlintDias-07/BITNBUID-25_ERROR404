from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from projects.models import Project, Bid

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