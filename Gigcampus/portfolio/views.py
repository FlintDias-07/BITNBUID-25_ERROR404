from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from projects.models import Project
from .models import Review

@login_required
def portfolio(request, username):
    user = get_object_or_404(User, username=username)
    
    if user.profile.role != 'freelancer':
        messages.error(request, 'Portfolio is only available for freelancers.')
        return redirect('dashboard')
    
    completed_projects = Project.objects.filter(
        bids__freelancer=user,
        bids__status='accepted',
        status='completed'
    )
    
    reviews = Review.objects.filter(freelancer=user).order_by('-created_at')
    
    context = {
        'freelancer': user,
        'completed_projects': completed_projects,
        'reviews': reviews,
    }
    
    return render(request, 'portfolio/portfolio.html', context)

@login_required
def add_review(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.user != project.posted_by or project.status != 'completed':
        messages.error(request, 'You can only review completed projects you posted.')
        return redirect('dashboard')
    
    # Check if review already exists
    if hasattr(project, 'review'):
        messages.info(request, 'You have already reviewed this project.')
        return redirect('project_detail', project_id=project.id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        feedback = request.POST.get('feedback')
        
        accepted_bid = project.bids.filter(status='accepted').first()
        if accepted_bid:
            Review.objects.create(
                project=project,
                freelancer=accepted_bid.freelancer,
                client=request.user,
                rating=rating,
                feedback=feedback
            )
            messages.success(request, 'Review added successfully!')
        
        return redirect('project_detail', project_id=project.id)
    
    return render(request, 'portfolio/add_review.html', {'project': project})